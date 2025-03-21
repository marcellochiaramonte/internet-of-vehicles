import machine
import ubinascii
import libraries.uasyncio as asyncio
from libraries.umqtt.robust2 import MQTTClient
from project.network.connection_interface import ConnectionInterface
from uerrno import ENOTCONN, ECONNRESET, ERR_MEM, ECONNABORTED
from config.constants import vehicle_id, mqtt_broker_IP, MQTT_SSL_PARAMS
import ssl
import struct
import socket
from utime import ticks_diff, ticks_ms
from os import urandom
import gc
import _thread
from time import time

gc.collect()

retain = 1
qos = 1
_DEFAULT_MS = 20


class IoVMQTTClient:
    def __init__(self):
        self.connection_interface = ConnectionInterface()  # starts the connection interface
        self.ping_frequency = 30000  # milliseconds

        self.client = MQTTClient(
            client_id="pycom_100",
            server=mqtt_broker_IP,
            port=8883,
            keepalive=0,
            ssl=True,
            ssl_params=MQTT_SSL_PARAMS,
            socket_timeout=3,
            message_timeout=10,
        )
        print("server ", self.client.server, ":", self.client.port)
        self.mqtt_topic = "v/" + vehicle_id + "/"
        self.connected_to_broker = False
        self.messages_to_send = set()
        # self.client.set_callback_status(self.status_callback)
        # self.client.set_callback(self.subscribe_callback)
        loop = asyncio.get_event_loop()
        loop.create_task(self.connect())

    async def connect(self):
        while not self.connected_to_broker:
            if self.connection_interface.internet_connectivity:
                print("will connect to mqtt broker")
                self.client.connect()
                await asyncio.sleep(1)
                # self.subscribe_to_status()
                self.connected_to_broker = True
                self.connection_interface.communication_mode_changed_ack = True
            else:
                self.connected_to_broker = False
                await self.connection_interface.connect_to_some_network()
        # connected, start subroutine to check for ping response
        self.create_loop_tasks()

    def create_loop_tasks(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.ping_with_timestamp())
        # loop.create_task(self.check_msgs_often())
        # loop.create_task(self.ping_and_get_response())
        loop.create_task(self.check_for_reconnection())

    def subscribe_to_status(self):
        print("subscribe to status", self.mqtt_topic + "status")
        self.client.subscribe(self.mqtt_topic + "status")

    def status_callback(self, pid, stat):
        print("server received", pid, stat)

    def subscribe_callback(self, topic, msg, retained, duplicate):
        print(topic, msg, ticks_diff(time(), int(msg)))

    async def ping_with_timestamp(self):
        # await asyncio.sleep(5)
        loop = asyncio.get_event_loop()
        # loop.create_task(self.check_msgs_often())
        while True:
            if self.connection_interface.internet_connectivity and self.connected_to_broker:
                self.publish_current_system_timestamp()
                print("will check emssage")
                # a_lock = _thread.allocate_lock()
                # with a_lock:
                #     print("a_lock is locked while this executes")
                #     _thread.start_new_thread(self.client.check_msg, ())
                #     print("done")
            await asyncio.sleep(120)

    def publish_current_system_timestamp(self):
        self.client.publish(topic=self.mqtt_topic + "status", msg=str(time()), retain=True, qos=0)

    def publish(self, topic, msg):
        if topic == "mqtt_live_data":
            print("will publish new live data metric")
            self.client.publish(topic=self.mqtt_topic + "live", msg=msg, retain=True, qos=0)

    async def ping_and_get_response(self):
        while True:
            if self.connection_interface.internet_connectivity and self.connected_to_broker:
                print("to receive:", self.client.rcv_pids)
                ping_diff = ticks_diff(ticks_ms(), self.client.last_ping) // 1000
                print("since last ping:", ping_diff, "seconds")
                received_diff = ticks_diff(ticks_ms(), self.client.last_cpacket) // 1000
                print("since last cpacket:", received_diff, "seconds")
                self.client.ping()
            await asyncio.sleep(10)

    async def check_msgs_often(self):
        while True:
            a_lock = _thread.allocate_lock()
            print("checking message")
            with a_lock:
                print("a_lock is locked while this executes")
                _thread.start_new_thread(self.client.check_msg, ())

            await asyncio.sleep(10)

    async def check_for_reconnection(self):
        print("started check for reconnection loop")
        while True:
            received_diff = ticks_diff(ticks_ms(), self.client.last_cpacket)
            print("received diff", received_diff // 1000)
            if (
                not self.connection_interface.communication_mode_changed_ack
                or not self.connection_interface.internet_connectivity
            ):
                print("changed station, ack:", self.connection_interface.communication_mode_changed_ack)
                await self.reconnect()
            elif received_diff > self.ping_frequency:
                # should be connected, so lets ping the server to be sure
                self.client.ping()
                await asyncio.sleep(2)
                self.client.check_msg()
                # await asyncio.sleep(6)
                received_diff_after = ticks_diff(ticks_ms(), self.client.last_cpacket)
                print("received diff after check", received_diff // 1000)
                if received_diff_after > self.ping_frequency * 4:
                    print("bad news, no answer from server")
                    await self.reconnect()

            await asyncio.sleep(3)

    async def reconnect(self):
        self.connected_to_broker = False
        self.connection_interface.check_internet_conncetivity()
        await self.connection_interface.connect_to_some_network()
        if self.connection_interface.internet_connectivity:
            self.client.connect()
            await asyncio.sleep(1)
            self.client.last_cpacket = ticks_ms()
            self.connected_to_broker = True
            self.connection_interface.communication_mode_changed_ack = True
            self.publish_current_system_timestamp()
