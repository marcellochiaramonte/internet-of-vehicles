class LocationDataChange:
    def __init__(self, timestamp, latitude, longitude):
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude


class DataChangeMessage:
    def __init__(self, timestamp, metric, value):
        self.timestamp = timestamp
        self.metric = metric
        self.value = value


### Mitsubishi iMieV metric ids [100-199]
mitsubishi_metric_ids = {
    "car_on": 101,
    "brake_pedal_position": 102,
    "accelerator_pedal_position": 103,
    "brake_pedal_switch": 104,
    "charger_temperature": 105,
    "charger_detection": 106,
    "motor_temperature": 107,
    "motor_rpm": 108,
    "handbrake": 109,
    "battery_soc": 110,
    "speed": 111,
    "odometer": 112,
    "transmission": 113,
    "quick_charge": 114,
    "charge_current_limit": 115,
}

mitsubishi_metric_ids_text = {
    101: "car_on",
    102: "brake_pedal_position",
    103: "accelerator_pedal_position",
    104: "brake_pedal_switch",
    105: "charger_temperature",
    106: "charger_detection",
    107: "motor_temperature",
    108: "motor_rpm",
    109: "handbrake",
    110: "battery_soc",
    111: "speed",
    112: "odometer",
    113: "transmission",
    114: "quick_charge",
    115: "charge_current_limit",
}

# list of can to be soft filtered
can_filter_frames = [
    0x101,
    0x208,
    0x210,
    0x231,
    0x286,
    0x298,
    0x346,
    0x373,
    0x374,
    0x384,
    0x389,
    0x412,
    0x418,
    0x697,
    0x6E4,
]

### Opel Ampera metric ids [200-299]
opel_ampera_metric_ids = {
    "vehicle_metric": 201,
}

opel_ampera_metric_ids_text = {
    201: "vehicle_metric",
}
