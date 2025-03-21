import libraries.uasyncio as asyncio
from project.network.wifi import WifiConnection
from project.network.lte import LTEConnection
from libraries.uping import ping
from config.constants import connection_interface_wifi_scan_rate
from machine import RTC
import utime
import socket
import gc

gc.collect()


class ConnectionInterface:
    def __init__(self, wifi_only=False, keepalive_interval=30):
        self.wifi_only = wifi_only  # to avoid using lte data while testing
        self.wifi = WifiConnection()
        self.lte = LTEConnection()
        self.internet_connectivity = False
        # will search for wifi connectivity every x seconds and ping google dns
        self.keepalive_interval = connection_interface_wifi_scan_rate  # interval in seconds
        self.keepalive_loop_already_setup = False
        self.communication_mode_changed_ack = True
        # start the keepalive connection task

    async def check_wlan_station_connected(self):
        while True:
            if not self.wifi.station_connected() and not self.lte.station_connected():
                print("WLAN disconnected")
                self.internet_connectivity = False
                await self.connect_to_some_network()
            await asyncio.sleep(2)

    def setup_keepalive(self):  # starts connection keepalive subroutines
        loop = asyncio.get_event_loop()
        loop.create_task(self.connection_keepalive())
        loop.create_task(self.check_wlan_station_connected())

    async def connection_keepalive(self):
        print("setup connection keepalive loop")
        while True:
            await self.connect_to_some_network()  # check if there is connectivity
            await asyncio.sleep(self.keepalive_interval)  # sleeps

    async def connect_to_some_network(self):
        if self.wifi.station_connected():
            print("conencted to wifi")
            await self.check_internet_conncetivity()
        # scans for a known wifi network and returns true if network is available
        elif self.wifi.is_network_available():
            await self.wifi.connect()
            await self.check_internet_conncetivity()
            self.communication_mode_changed_ack = (
                False  # flag for the mqtt broker so it knows it must reconnect to the broker
            )

            if self.lte.station_connected():  # if there is wifi connection, disables the LTE modem to save energy
                self.lte.disconnect()

        else:  # no wifi, lets try LTE
            if self.lte.station_connected():
                print("no wifi network available, lte already connected")
                # await self.check_internet_conncetivity() # pinging 8.8.8.8 can use the data volume faster
            else:
                print("connecting to lte")
                await self.lte.connect()
                await self.check_internet_conncetivity()
                self.communication_mode_changed_ack = False

        if not self.keepalive_loop_already_setup:  # only setup the connection keepalive loop once
            self.setup_keepalive()
            self.keepalive_loop_already_setup = True

    async def wan_ok(self):
        if not self.wifi.station_connected() and not self.lte.station_connected():  # WiFi and LTE are down
            return False
        try:
            ping_res = ping("8.8.8.8", count=1, interval=5, size=16)  # ping google dns server
            return ping_res[0] == ping_res[1]  # sent packets must be equal to received packets
        except:
            return False

    async def check_internet_conncetivity(self):
        self.internet_connectivity = await self.wan_ok()  # set the connected flag as the ping response
        print("internet connectivity: ", self.internet_connectivity)