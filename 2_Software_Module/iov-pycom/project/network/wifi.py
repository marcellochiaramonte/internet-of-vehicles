from network import WLAN
import libraries.uasyncio as uasyncio
from config.wlan_networks import known_wlan_networks


class WifiConnection:
    def __init__(self):
        self.station = WLAN(mode=WLAN.STA)
        self.station.init(
            antenna=WLAN.EXT_ANT,
        )
        self.ssid = ""
        self.password = ""

    def get_ip_address(self):
        return self.station.ifconfig()[0]

    def station_connected(self):
        return self.station.isconnected()

    async def connect(self):
        if self.ssid and self.password:
            print(self.station.connect(self.ssid, auth=(WLAN.WPA2, self.password)))
            print("connecting to wifi " + self.ssid, end="")
            timeout = 0
            while not self.station.isconnected() and timeout < 15:
                print(".", end="")
                timeout += 1
                await uasyncio.sleep(1)
            print("\nWifi connected: " + str(self.get_ip_address()))

    async def kill_wifi(self):
        await uasyncio.sleep(5)
        self.station.deinit()

    def is_network_available(self):
        self.station.disconnect()
        scanned_networks = self.station.scan()
        for network in scanned_networks:
            # print(network[0] + "   " + str(network[4]) + "dBm")
            pass
        found_networks = []
        for network in scanned_networks:
            for ap in known_wlan_networks:
                if ap["ssid"] == network[0]:
                    found_networks.append((ap["ssid"], ap["pwd"], network[4]))

        def get_key(item):
            return item[2]

        # sort the found networks by strongest signal (network[4])
        if found_networks:
            strongest_network = sorted(found_networks, key=get_key, reverse=True)[0]
            self.ssid = strongest_network[0]
            self.password = strongest_network[1]
            return True
        else:
            return False
