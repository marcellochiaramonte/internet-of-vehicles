import libraries.uasyncio as asyncio
from project.vehicles.base_vehicle import BaseVehicle
from project.can.can_controller import CanController
from machine import reset
import gc

gc.collect()  # garbage collector empty unnecessary cached data in the Stack/RAM


def main():
    print("main func")  # starts the base vehicle class, which calls other dependencies
    vehicle = BaseVehicle()
    gc.collect()
    loop = asyncio.get_event_loop()
    loop.run_forever()


try:
    main()  # main func

except:
    print("exception occoured, reseting module")
finally:
    print("end, resetting")
    reset()
