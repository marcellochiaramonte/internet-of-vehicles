from network import LTE
import libraries.uping as uping
import libraries.uasyncio as uasyncio


class LTEConnection:
    def __init__(self):
        self.station = LTE()
        self.station.init()

    async def connect(self):
        try:
            self.station.attach(band=20, apn="iot.1nce.net")
            print("lte station initialized, connecting", end="")
            while not self.station.isattached():
                print(".", end="")
                await uasyncio.sleep(1)
            print("\nlte station attached: " + str(self.station.isattached()))
            self.station.connect()
            print("connecting lte", end="")
            while not self.station.isconnected():
                print(".")
                await uasyncio.sleep(1)
            print("\nlte station connected: " + str(self.station.isconnected()))
            await uasyncio.sleep(3)
        except OSError:
            print("os except")

    def station_connected(self):
        if self.station_attached():
            return self.station.isconnected()
        else:
            return False

    def station_attached(self):
        return self.station.isattached()

    def disconnect(self):
        self.station.disconnect()
        self.station.dettach()
