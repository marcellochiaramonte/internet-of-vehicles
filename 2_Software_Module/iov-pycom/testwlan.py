from network import WLAN


class WifiConnection:
    def __init__(self):
        self.station = WLAN(mode=WLAN.STA)
        self.station.init(
            antenna=WLAN.EXT_ANT,
        )

    def is_network_available(self):
        self.station.disconnect()
        scanned_networks = self.station.scan()
        for network in scanned_networks:
            print(network[0] + "   " + str(network[4]) + "dBm")


con = WifiConnection()
con.is_network_available()
