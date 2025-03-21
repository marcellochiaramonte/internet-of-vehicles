from project.vehicles.metrics import DataChangeMessage, mitsubishi_metric_ids, mitsubishi_metric_ids_text
import gc
from utime import ticks_diff, ticks_ms

gc.collect()


class Mitsubishi:
    def __init__(self):
        print("Initialized Vehicle: Mitsubishi")
        self.DEBUG = False

        # Vehicle Specific Configuration
        self.metric_ids = mitsubishi_metric_ids
        self.metric_ids_text = mitsubishi_metric_ids_text
        # can raw byte strings
        self.current_can_raw_data = {
            0x101: None,
            0x208: None,
            0x210: None,
            0x231: None,
            0x286: None,
            0x298: None,
            0x346: None,
            0x373: None,
            0x374: None,
            0x384: None,
            0x389: None,
            0x412: None,
            0x418: None,
            0x697: None,
            0x6E4: None,
        }

        # translated vehicle-metric values # note that there might be more than 1 metric per CAN Frame
        self.current_metric_values = {
            101: None,
            102: None,
            103: None,
            104: None,
            105: None,
            106: None,
            107: None,
            108: None,
            109: None,
            110: None,
            111: None,
            112: None,
            113: None,
            114: None,
            115: None,
        }

        self.transmission_mapping = {80: -2, 82: -1, 78: 0, 68: 1, 131: 2, 50: 3}  # P R N D B C

        self.cfg_heater_old = False

    def dprint(self, *args):
        if self.DEBUG:
            for arg in args:
                print(arg, end=" ")
            print("")

    def write_to_buffer(self, metric_id, value):
        self.current_metric_values.update({metric_id: value})
        self.dprint(mitsubishi_metric_ids_text[metric_id], self.current_metric_values[metric_id])
        # print("writing to message_buffer")

        # currently the buffer will never be emptied, so the memory will eventually run full
        # self.message_buffer.append(DataChangeMessage(timestamp=ticks_ms(), metric=metric_id, value=value))
        self.dprint(len(self.message_buffer))

    def translate_frame(self, frame):
        id = frame[0]
        d = frame[1]

        try:
            if d != self.current_can_raw_data[id]:
                self.current_can_raw_data.update({id: d})

                if id == 0x101:  # Key status
                    value = d[0] == 4
                    metric_id = self.metric_ids["car_on"]
                    if value != self.current_metric_values[metric_id]:
                        self.write_to_buffer(metric_id, value)

                elif id == 0x208 and False:  # Brake pedal position # works, however too much data
                    value = ((d[2] * 256 + d[3]) - 24576) / 640 * 100
                    metric_id = self.metric_ids["brake_pedal_position"]
                    if value != self.current_metric_values[metric_id]:
                        self.write_to_buffer(metric_id, value)

                elif id == 0x210 and False:  # Accelerator pedal position
                    value = (d[2] * 100.0) / 255.0
                    metric_id = self.metric_ids["accelerator_pedal_position"]
                    if value != self.current_metric_values[metric_id]:
                        self.write_to_buffer(metric_id, value)

                elif id == 0x231:  # Brake pedal switch # true false
                    value = True if d[4] == 2 else False if d[4] == 0 else None
                    metric_id = self.metric_ids["brake_pedal_switch"]
                    if value != self.current_metric_values[metric_id]:
                        self.write_to_buffer(metric_id, value)

                elif id == 0x286 and False:  # Charger/inverter temperature
                    # working however too many messages, should filter out
                    charger_temperature = d[3] - 40
                    metric_id_1 = self.metric_ids["charger_temperature"]
                    if charger_temperature != self.current_metric_values[metric_id_1]:
                        self.write_to_buffer(metric_id_1, charger_temperature)

                    charger_detection = (d[1] & 32) != 0
                    metric_id_2 = self.metric_ids["charger_detection"]
                    if charger_detection != self.current_metric_values[metric_id_2]:
                        self.write_to_buffer(metric_id_2, charger_detection)

                elif id == 0x298 and False:
                    # Motor temperature and RPM # its working, however many messages, maybe get only the last 10 or so and make a mittelwert?
                    motor_temperature = d[3] - 40
                    metric_id_1 = self.metric_ids["motor_temperature"]
                    if motor_temperature != self.current_metric_values[metric_id_1]:
                        self.write_to_buffer(metric_id_1, motor_temperature)

                    motor_rpm = ((d[6] * 256.0) + d[7]) - 10000
                    if motor_rpm > -10 and motor_rpm < 10:
                        motor_rpm = 0
                    metric_id_2 = self.metric_ids["motor_rpm"]
                    if motor_rpm != self.current_metric_values[metric_id_2]:
                        self.write_to_buffer(metric_id_2, motor_rpm)

                elif id == 0x346:  # Estimated range, Handbrake state
                    handbrake = not ((d[4] & 32) == 0)
                    metric_id_1 = self.metric_ids["handbrake"]
                    if handbrake != self.current_metric_values[metric_id_1]:
                        self.write_to_buffer(metric_id_1, handbrake)

                    # TODO
                    # if self.quick_charge and self.estimated_range != 0:
                    #     self.estimated_range = 0
                    # else:
                    #     estimated_range_read = d[7]
                    #     if self.estimated_range != estimated_range_read:
                    #         self.estimated_range = estimated_range_read
                    #         self.dprint("estimated_range: ", estimated_range_read)

                # TODO check if correct
                # elif id == 0x373:  # Main Battery voltage and current
                #     bat_current_read = (((((d[2] * 256.0) + d[3])) - 32768)) / 100.0

                #     bat_current_diff = abs(self.bat_current - bat_current_read)
                #     bat_current_margin = abs(self.bat_current * self.bat_current_variation_margin)

                #     if self.bat_current != bat_current_read and bat_current_diff > bat_current_margin:
                #         self.dprint("bat_current_read:", bat_current_read, "diff:", bat_current_diff)
                #         self.bat_current = bat_current_read

                #         self.write_to_buffer(id, d)

                #     bat_voltage_read = (d[4] * 256 + d[5]) / 10.0
                #     if self.bat_voltage != bat_voltage_read:
                #         self.bat_voltage = bat_voltage_read
                #         self.dprint("bat_voltage:", bat_voltage_read)

                #         self.write_to_buffer(id, d)

                elif id == 0x374:  # Main Battery Soc
                    if d[1] > 10:
                        value = (d[1] - 10) / 2.0
                        metric_id = self.metric_ids["battery_soc"]
                        if value != self.current_metric_values[metric_id]:
                            self.write_to_buffer(metric_id, value)

                # TODO
                # elif id == 0x384:  # heating current
                #     try:
                #         heating_current_read = d[4] / 10.0
                #         if self.heating_current != heating_current_read:
                #             self.heating_current = heating_current_read
                #             self.dprint("heating_current:", heating_current_read)

                #             self.write_to_buffer(id, d)

                #             if self.cfg_heater_old:
                #                 self.env_heating_temp_return = ((d[5] - 32) / 1.8) - 3.0
                #                 self.env_heating_temp_flow = ((d[6] - 32) / 1.8) - 3.0
                #             else:
                #                 self.env_heating_temp_return = (d[5] * 0.6) - 40.0
                #                 self.env_heating_temp_flow = (d[6] * 0.6) - 40.0

                #         env_ac_amp_read = (d[0] * 256.0 + d[1]) / 1000.0
                #         if self.env_ac_amp != env_ac_amp_read:
                #             self.env_ac_amp = env_ac_amp_read
                #     except IndexError:
                #         print("Brake pedal position")

                # TODO
                # elif id == 0x389:  # Charger voltage and current
                #     if not self.quick_charge and self.slow_charge:
                #         charge_voltage_read = d[1]
                #         charge_current_read = d[6] / 10.0
                #         if self.charge_voltage_read != charge_voltage_read:
                #             self.charge_voltage_read = charge_voltage_read
                #             self.dprint("charge_voltage_read:", charge_voltage_read)

                #             self.write_to_buffer(id, d)

                #         if self.charge_current_read != charge_current_read:
                #             self.charge_current_read = charge_current_read
                #             self.dprint("charge_current_read:", charge_current_read)

                #             self.write_to_buffer(id, d)

                elif id == 0x412:  # Speed and odometer
                    speed = d[1] - 255 if d[1] > 200 else d[1]
                    metric_id_1 = self.metric_ids["speed"]
                    if speed != self.current_metric_values[metric_id_1]:
                        self.write_to_buffer(metric_id_1, speed)

                    odometer = (d[2] << 16) + (d[3] << 8) + d[4]
                    metric_id_2 = self.metric_ids["odometer"]
                    if odometer != self.current_metric_values[metric_id_2]:
                        self.write_to_buffer(metric_id_2, odometer)

                elif id == 0x418:  # Transmission state determination
                    try:
                        value = self.transmission_mapping[d[0]]
                        metric_id = self.metric_ids["transmission"]
                        if value != self.current_metric_values[metric_id]:
                            self.write_to_buffer(metric_id, value)
                    except KeyError as e:
                        print("key not on the transmission keys list")
                        # no problem, the id might have other data being transmitted as well

                # TODO
                elif id == 0x697 and False:  # Charging Quick Charge
                    quick_charge = d[0] == 1
                    metric_id_1 = self.metric_ids["quick_charge"]
                    if quick_charge != self.current_metric_values[metric_id_1]:
                        self.write_to_buffer(metric_id_1, quick_charge)

                    charge_current_limit = d[2]
                    metric_id_2 = self.metric_ids["charge_current_limit"]
                    if charge_current_limit != self.current_metric_values[metric_id_2]:
                        self.write_to_buffer(metric_id_2, charge_current_limit)

                # TODO
                elif False and id == 0x6E4:  # Battery temperatures and voltages

                    pid_index = id - 1761
                    cmu_id = d[0]

                    temp1 = d[1] - 50
                    temp2 = d[2] - 50
                    temp3 = d[3] - 50

                    voltage1 = ((d[4] * 256.0 + d[5]) / 200.0) + 2.1
                    voltage2 = ((d[6] * 256.0 + d[7]) / 200.0) + 2.1

                    voltage_index = (cmu_id - 1) * 8 + (2 * pid_index)
                    temp_index = (cmu_id - 1) * 6 + (2 * pid_index)

                    if cmu_id >= 7:
                        voltage_index -= 4
                        temp_index -= 3

                    changes = False

                    if voltage1 != self.cell_voltage_1:
                        self.cell_voltage_1 = voltage1
                        changes = True

                    if voltage2 != self.cell_voltage_2:
                        self.cell_voltage_2 = voltage2
                        changes = True
                    if self.cell_temperature_1 != temp1:
                        self.cell_temperature_1 = temp1
                        changes = True
                    if self.cell_temperature_2 != temp2:
                        self.cell_temperature_2 = temp2
                        changes = True
                    if self.cell_temperature_3 != temp3:
                        self.cell_temperature_3 = temp3
                        changes = True

                    if changes:
                        self.dprint(
                            "voltage1:",
                            voltage1,
                            "voltage2:",
                            voltage2,
                            "temp1:",
                            temp1,
                            "temp2:",
                            temp2,
                            "temp3:",
                            temp3,
                        )
                        # self.write_to_buffer(id, d)

                    # if pid_index == 0:
                    #     self.cell_temperature_1 =
                    #     self.cell_temperature_2 = CellTemperature(temp_index + 1, temp3)
                    # else:
                    #     self.cell_temperature_1 = CellTemperature(temp_index, temp1)
                    #     if cmu_id != 6 and cmu_id != 12:
                    #         self.cell_temperature_2 = CellTemperature(temp_index + 1, temp2)

        except IndexError:
            print("index error on id: ", hex(id))

    def test_translate(self):  # test the translate function
        self.translate_frame([0x101, [4, 1, 4, 6]])
        self.translate_frame([0x208, [0, 1, 4, 6]])
        self.translate_frame([0x210, [4, 1, 4, 6]])
        self.translate_frame([0x231, [4, 1, 4, 6, 2]])
        self.translate_frame([0x286, [4, 32, 4, 60]])
        self.translate_frame([0x298, [4, 1, 4, 60, 2, 4, 30, 70]])

        self.translate_frame([0x374, [4, 150, 4, 6, 32]])

        self.translate_frame([0x412, [4, 45, 1, 6, 7]])
        self.translate_frame([0x418, [68, 1, 4, 6]])
        self.translate_frame([0x697, [1, 1, 15, 6]])