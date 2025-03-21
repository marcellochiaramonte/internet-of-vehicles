from config.constants import vehicles, selected_vehicle
from project.mqtt.mqtt_connection import IoVMQTTClient
from project.can.can_controller import CanController
from project.gps.gps import GPSReader
import libraries.uasyncio as asyncio
from uos import urandom
import json
import gc
import _thread
from project.vehicles.metrics import DataChangeMessage, LocationDataChange
from utime import ticks_ms, time

gc.collect()

### Defines which vehicle is being used and extends the base vehicle class accordingly
if selected_vehicle == vehicles["Mitsubishi"]:
    from project.vehicles.mitsubishi import Mitsubishi

    class FullVehicle(Mitsubishi):
        def __init__(self):
            print("extending full vehicle class")
            super(FullVehicle, self).__init__()


elif selected_vehicle == vehicles["OpelAmpera"]:
    from project.vehicles.opel_ampera import OpelAmpera

    class FullVehicle(OpelAmpera):
        def __init__(self):
            super(FullVehicle, self).__init__()


else:

    class FullVehicle:
        def __init__(self):
            super(FullVehicle, self).__init__()
            print("Created Empty Base Vehicle Object")


# Main Vehicle Class, Organizes all other classes
class BaseVehicle(FullVehicle, CanController):  # check if this gonna work
    def __init__(self):
        self.BASE_VEHICLE_DEBUG = False
        self.message_buffer = []  # buffer of can dataframes received. This list is standard for all vehicles
        super(BaseVehicle, self).__init__()  # equivalent to FullVehicle.__init__(self)
        CanController.__init__(self)
        # self.mqtt_client = None
        self.mqtt_client = IoVMQTTClient()
        self.gps_reader = GPSReader()
        self.set_can_callback()  # defines the can callback function
        self.create_loop_tasks()

    def dprint(self, *args):
        if self.BASE_VEHICLE_DEBUG:
            print(*args)

    def create_loop_tasks(self):
        loop = asyncio.get_event_loop()

        # this function will periodically check for datachanges on the current state of the can bus data
        loop.create_task(self.poll_can_frames_and_location_publish_mqtt())

        # uncomment the next line to log the CAN Bus decoded messages on a local file. The implementation to later read and send the file through HTTP is not done yet
        # loop.create_task(self.poll_can_frames_write_to_file())

        loop.create_task(
            self.simulate_new_value()
        )  # uncomment this to simulate new value every x seconds, that will be published via mqtt

        # loop.create_task(self.publish_test())  # published test values to the topic test

        loop.create_task(self.cleanup_ram())  # runs the garbage collector and prints stats about the RAM

    def set_can_callback(self):
        # defines the callback function of the can controller on a received frame
        # the callback function is defined at the vehicle specific class, like Mitsubishi or OpelAmpera
        # the callback function must be implemented at the vehicle-specific class
        self.set_callback(self.translate_frame)

    # poll the current values of the vehicle metrics and location every 5 seconds and send the datachages via mqtt
    async def poll_can_frames_and_location_publish_mqtt(self):
        # makes a copy of the empty dictionary on startup
        current_metrics_data_snapshot = self.current_metric_values.copy()
        current_location_snapshot = None
        datachanges_to_send_mqtt = []
        location_changes_to_send_mqtt = []

        # starts loop
        while True:
            # Checks for CAN Datachanges
            for key in current_metrics_data_snapshot:
                snapshot_data = current_metrics_data_snapshot[key]
                current_data = self.current_metric_values[key]
                if snapshot_data != current_data:
                    # updated the current snapshot of data in case of datachanges
                    current_metrics_data_snapshot[key] = current_data
                    self.dprint(self.metric_ids_text[key], "old:", snapshot_data, "new", current_data)
                    # prints "state_of_charge, old: 75, new: 74"
                    if self.gps_reader.gps_time_is_set:
                        # only publishes data once the time is known from the GPS signal
                        datachanges_to_send_mqtt.append(
                            DataChangeMessage(timestamp=time(), metric=key, value=current_data)
                        )

            # Checks for Location Datachanges
            current_location = self.gps_reader.current_location
            if current_location:
                if (
                    not current_location_snapshot
                    or current_location_snapshot.latitude != current_location.latitude
                    or current_location_snapshot.longitude != current_location.longitude
                ):
                    current_location_snapshot = current_location
                    if self.gps_reader.gps_time_is_set:
                        location_changes_to_send_mqtt.append(current_location)

            # publish to mqtt
            if self.mqtt_client:
                if datachanges_to_send_mqtt or location_changes_to_send_mqtt:
                    print("broker connection", self.mqtt_client.connected_to_broker)
                    if (
                        self.mqtt_client.connected_to_broker
                        and self.mqtt_client.connection_interface.internet_connectivity
                    ):
                        json_payload = self.serialize_json_live_metric(
                            datachanges_to_send_mqtt, location_changes_to_send_mqtt
                        )
                        datachanges_to_send_mqtt = []
                        location_changes_to_send_mqtt = []
                        self.dprint("PUBLISH:", json_payload)
                        self.mqtt_client.publish(topic="mqtt_live_data", msg=json_payload)
                    else:
                        print("still not connected to broker")

            await asyncio.sleep(5)

    # related to writing json files to flash
    async def poll_can_frames_write_to_file(self):
        while True:
            if self.message_buffer and len(self.message_buffer) > 99:
                # 100 data changes per file or 30 seconds without saving
                self.disable_callback()
                self.can.deinit()
                await asyncio.sleep(2)
                a_lock = _thread.allocate_lock()
                with a_lock:
                    print("a_lock is locked while this executes")
                    _thread.start_new_thread(self.write_buffer_to_file, ())
                    print("done")
                await asyncio.sleep(2)
                self.print_debug_messages()
                self.reset_can()
                self.set_can_callback()

            await asyncio.sleep(10)

    def serialize_json_live_metric(self, metric_buffer, location_changes):
        serialized = {"m": [], "p": []}
        for msg in metric_buffer:
            serialized["m"].append(
                {
                    "t": msg.timestamp,
                    "id": msg.metric,
                    "v": msg.value,
                }
            )
        for location in location_changes:
            serialized["p"].append(
                {
                    "t": location.timestamp,
                    "lat": location.latitude,
                    "lon": location.longitude,
                }
            )
        return json.dumps(serialized)

    def write_buffer_to_file(self):
        print("****start sync write****")
        # start_time = time.ticks_ms()
        try:
            filename = "/flash/data/2021_03_04_" + str(time()) + ".json"
            with open(filename, "w+") as file:
                file.write(self.serialize_json_live_metric(self.message_buffer))
            print("writing to flash OK")
        except:
            print("something went bad")
        finally:
            pass
            self.message_buffer = []
            # bytes_before = gc.mem_free()
            # print("before gc", bytes_before)
            # gc.collect()
            # bytes_after = gc.mem_free()
            # print("after gc ", bytes_after, "\n", "freed up", bytes_after - bytes_before, "bytes")
            # self.writing_to_file = False
            # print("****end sync write****")
            # print("diff: ", time.ticks_diff(time.ticks_ms(), start_time), "ms")

    async def cleanup_ram(self):
        while True:
            self.print_debug_messages()
            await asyncio.sleep(10)

    async def simulate_new_value(self):  # emulate can frames being received
        while True:
            x = int.from_bytes(urandom(1), 0)
            self.translate_frame([0x374, [4, x, 4, 6, 32]])
            self.translate_frame([0x412, [4, x, 4, 6, x // 5]])
            await asyncio.sleep(2)

    def print_debug_messages(self):
        self.dprint("message buffer = ", len(self.message_buffer))
        self.dprint("BEFORE RAM free {} alloc {}".format(gc.mem_free(), gc.mem_alloc()))
        gc.collect()
        self.dprint("AFTER RAM free {} alloc {}".format(gc.mem_free(), gc.mem_alloc()))

    async def publish_test(self):
        x = 0
        while True:
            if self.mqtt_client.connected_to_broker and self.mqtt_client.connection_interface.internet_connectivity:
                print("publish msg", x)
                self.mqtt_client.client.publish(topic="test", msg="msg_" + str(x), retain=True, qos=0)
                x = x + 1
            await asyncio.sleep(5)


gc.collect()
