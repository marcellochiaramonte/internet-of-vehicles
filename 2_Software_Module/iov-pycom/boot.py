import pycom
import gc

gc.enable()
print("***SOFTWARE VERSION:  1.0.0   *************")
print("boot started")
pycom.heartbeat(False)
pycom.wifi_on_boot(False)
print("boot finished")
