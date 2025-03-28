# (c) 2014-2019 Paul Sokolovsky. MIT license.
import libraries.uasyncio.core
import uerrno
import uselect as select
import usocket as _socket
from libraries.uasyncio.core import *
import gc

gc.collect()

DEBUG = 0
log = None


def set_debug(val):
    global DEBUG, log
    DEBUG = val
    if val:
        import logging

        log = logging.getLogger("uasyncio")


class PollEventLoop(EventLoop):
    def __init__(self, runq_len=16, waitq_len=16):
        EventLoop.__init__(self, runq_len, waitq_len)
        self.poller = select.poll()

    def add_reader(self, sock, cb, *args):
        if DEBUG and __debug__:
            log.debug("add_reader%s", (sock, cb, args))
        if args:
            self.poller.register(sock, select.POLLIN, (cb, args))
        else:
            self.poller.register(sock, select.POLLIN, cb)

    def remove_reader(self, sock):
        if DEBUG and __debug__:
            log.debug("remove_reader(%s)", sock)
        self.poller.unregister(sock)

    def add_writer(self, sock, cb, *args):
        if DEBUG and __debug__:
            log.debug("add_writer%s", (sock, cb, args))
        if args:
            self.poller.register(sock, select.POLLOUT, (cb, args))
        else:
            self.poller.register(sock, select.POLLOUT, cb)

    def remove_writer(self, sock):
        if DEBUG and __debug__:
            log.debug("remove_writer(%s)", sock)
        # StreamWriter.awrite() first tries to write to a socket,
        # and if that succeeds, yield IOWrite may never be called
        # for that socket, and it will never be added to poller. So,
        # ignore such error.
        self.poller.unregister(sock, False)

    def cancel_io(self, sock):
        if DEBUG and __debug__:
            log.debug("cancel_io(%s)", sock)
        # Cancel both reader and writer
        # Don't remove, in the hope that it will be used again, though
        # this call is usually used for timeouts, and timeouts are
        # usually handled as fatal errors (but then underlying stream
        # should be closed by user).
        # Use modify() deliberately, to catch a case when we cancel
        # a socket which was never pended, what shouldn't happen.
        self.poller.modify(sock, 0)

    def wait(self, delay):
        if DEBUG and __debug__:
            log.debug("poll.wait(%d)", delay)
        # We need one-shot behavior (second arg of 1 to .poll())
        res = self.poller.ipoll(delay, 1)
        # log.debug("poll result: %s", res)
        for sock, ev, cb in res:
            if ev & (select.POLLHUP | select.POLLERR):
                # These events are returned even if not requested, and
                # are sticky, i.e. will be returned again and again.
                # If the caller doesn't do proper error handling and
                # unregistering this sock, we'll busy-loop on it, so we
                # as well can unregister it now "just in case".
                self.remove_reader(sock)
            if DEBUG and __debug__:
                log.debug("Calling IO callback: %r", cb)
            if isinstance(cb, tuple):
                cb[0](*cb[1])
            else:
                cb.pend_throw(None)
                self.call_soon(cb)


class StreamReader:
    def __init__(self, polls, ios=None):
        if ios is None:
            ios = polls
        self.polls = polls
        self.ios = ios

    def read(self, n=-1):
        while True:
            yield IORead(self.polls)
            res = self.ios.read(n)
            if res is not None:
                break
            # This should not happen for real sockets, but can easily
            # happen for stream wrappers (ssl, websockets, etc.)
            # log.warn("Empty read")
        if not res:
            yield IOReadDone(self.polls)
        return res

    def readexactly(self, n):
        buf = b""
        while n:
            yield IORead(self.polls)
            res = self.ios.read(n)
            if res is None:
                # See comment in read()
                continue
            if not res:
                yield IOReadDone(self.polls)
                break
            buf += res
            n -= len(res)
        return buf

    def readline(self):
        if DEBUG and __debug__:
            log.debug("StreamReader.readline()")
        buf = b""
        while True:
            yield IORead(self.polls)
            res = self.ios.readline()
            if res is None:
                # See comment in read()
                continue
            if not res:
                yield IOReadDone(self.polls)
                break
            buf += res
            if buf[-1] == 0x0A:
                break
        if DEBUG and __debug__:
            log.debug("StreamReader.readline(): %s", buf)
        return buf

    def aclose(self):
        yield IOReadDone(self.polls)
        # .ios wraps .polls, so closing ios will lead to closure of polls too
        self.ios.close()

    def __repr__(self):
        return "<StreamReader %r %r>" % (self.polls, self.ios)


class StreamWriter:
    def __init__(self, s, extra):
        self.s = s
        self.extra = extra

    def awrite(self, buf, off=0, sz=-1):
        # This method is called awrite (async write) to not proliferate
        # incompatibility with original asyncio. Unlike original asyncio
        # whose .write() method is both not a coroutine and guaranteed
        # to return immediately (which means it has to buffer all the
        # data), this method is a coroutine.
        if sz == -1:
            sz = len(buf) - off
        if DEBUG and __debug__:
            log.debug("StreamWriter.awrite(): spooling %d bytes", sz)
        while True:
            res = self.s.write(buf, off, sz)
            # If we spooled everything, return immediately
            if res == sz:
                if DEBUG and __debug__:
                    log.debug("StreamWriter.awrite(): completed spooling %d bytes", res)
                return
            if res is None:
                res = 0
            if DEBUG and __debug__:
                log.debug("StreamWriter.awrite(): spooled partial %d bytes", res)
            assert res < sz
            off += res
            sz -= res
            yield IOWrite(self.s)
            # assert s2.fileno() == self.s.fileno()
            if DEBUG and __debug__:
                log.debug("StreamWriter.awrite(): can write more")

    # This function is tenative, subject to change
    def awritestr(self, s):
        yield from self.awrite(s.encode())

    # Write piecewise content from iterable (usually, a generator)
    def awriteiter(self, iterable):
        for buf in iterable:
            yield from self.awrite(buf)

    def aclose(self):
        yield IOWriteDone(self.s)
        self.s.close()

    def get_extra_info(self, name, default=None):
        return self.extra.get(name, default)

    def __repr__(self):
        return "<StreamWriter %r>" % self.s


def open_connection(host, port, ssl=False):
    if DEBUG and __debug__:
        log.debug("open_connection(%s, %s)", host, port)
    ai = _socket.getaddrinfo(host, port, 0, _socket.SOCK_STREAM)
    ai = ai[0]
    s = _socket.socket(ai[0], ai[1], ai[2])
    s.setblocking(False)
    try:
        s.connect(ai[-1])
    except OSError as e:
        if e.args[0] != uerrno.EINPROGRESS:
            raise
    if DEBUG and __debug__:
        log.debug("open_connection: After connect")
    yield IOWrite(s)
    #    if __debug__:
    #        assert s2.fileno() == s.fileno()
    if DEBUG and __debug__:
        log.debug("open_connection: After iowait: %s", s)
    if ssl:
        print("Warning: uasyncio SSL support is alpha")
        import ussl

        s.setblocking(True)
        s2 = ussl.wrap_socket(s)
        s.setblocking(False)
        return StreamReader(s, s2), StreamWriter(s2, {})
    return StreamReader(s), StreamWriter(s, {})


def start_server(client_coro, host, port, backlog=10):
    if DEBUG and __debug__:
        log.debug("start_server(%s, %s)", host, port)
    ai = _socket.getaddrinfo(host, port, 0, _socket.SOCK_STREAM)
    ai = ai[0]
    s = _socket.socket(ai[0], ai[1], ai[2])
    s.setblocking(False)

    s.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
    s.bind(ai[-1])
    s.listen(backlog)
    while True:
        if DEBUG and __debug__:
            log.debug("start_server: Before accept")
        yield IORead(s)
        if DEBUG and __debug__:
            log.debug("start_server: After iowait")
        s2, client_addr = s.accept()
        s2.setblocking(False)
        if DEBUG and __debug__:
            log.debug("start_server: After accept: %s", s2)
        extra = {"peername": client_addr}
        yield client_coro(StreamReader(s2), StreamWriter(s2, extra))


libraries.uasyncio.core._event_loop_class = PollEventLoop
