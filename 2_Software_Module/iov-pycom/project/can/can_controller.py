from machine import CAN
import libraries.uasyncio as uasyncio
from project.vehicles.metrics import can_filter_frames

import gc

gc.collect()


class CanController:
    def __init__(self):
        self.can = None
        self.reset_can()
        print("initialized can with soft filtering")

    def reset_can(self):
        self.can = CAN(
            mode=CAN.NORMAL,
            baudrate=500000,
            pins=("P19", "P20"),
            rx_queue_len=512,  # messages on the queue
            frame_format=CAN.FORMAT_STD,  # 11 bit identifier
        )
        self.can.soft_filter(CAN.FILTER_LIST, can_filter_frames)

    def stop_can(self):
        self.can.deinit()

    def set_callback(self, callback_function):  # should be working
        def can_cb(can_obj):  # defines the callback function for a received frame
            try:
                receive_object = can_obj.recv()  # tuple in form (id,data)
                if receive_object:
                    callback_function(receive_object)  # calls the translate_frames function of the vehicle classes
            except:
                print("exception on reading can frame")

        try:
            # disables running threads that might still be active
            self.disable_callback()
            self.can.callback(handler=can_cb, trigger=CAN.RX_FRAME)
        except TypeError as e:
            print("typeerror on callback setup", e)
        print("callback is set")

    def disable_callback(self):
        self.can.callback(handler=None, trigger=CAN.RX_FRAME)
        print("can callback disabled")
