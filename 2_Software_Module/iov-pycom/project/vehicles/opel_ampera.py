import gc
from project.vehicles.metrics import DataChangeMessage, opel_ampera_metric_ids, opel_ampera_metric_ids_text
from utime import ticks_diff, ticks_ms

gc.collect()


class OpelAmpera:
    def __init__(self):
        print("Initialized Vehicle: Opel Ampera")
        self.DEBUG = False

        # Vehicle Specific Configuration
        self.metric_ids = opel_ampera_metric_ids
        self.metric_ids_text = opel_ampera_metric_ids_text
        # can raw byte strings
        self.current_can_raw_data = {}

        # translated vehicle-metric values # note that there might be more than 1 metric per CAN Frame
        self.current_metric_values = {}

    def dprint(self, *args):
        if self.DEBUG:
            for arg in args:
                print(arg, end=" ")
            print("")

    def write_to_buffer(self, metric_id, value):
        self.current_metric_values.update({metric_id: value})
        self.dprint(self.metric_ids_text[metric_id], self.current_metric_values[metric_id])
        # print("writing to message_buffer")
        self.message_buffer.append(DataChangeMessage(timestamp=ticks_ms(), metric=metric_id, value=value))
        self.dprint(len(self.message_buffer))

    def translate_frame(self, frame):
        id = frame[0]
        d = frame[1]

        try:
            if d != self.current_can_raw_data[id]:
                self.current_can_raw_data.update({id: d})

                if id == 0x12345:  # VehicleMetric to be defined
                    value = d[0] == 4
                    metric_id = self.metric_ids["vehicle_metric"]
                    if value != self.current_metric_values[metric_id]:
                        self.write_to_buffer(metric_id, value)

        except IndexError:
            print("index error on id: ", hex(id))