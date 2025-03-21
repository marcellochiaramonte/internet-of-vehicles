vehicles = {
    "Mitsubishi": 1,
    "OpelAmpera": 2,
}

can_filter_frames = []
selected_vehicle = vehicles["Mitsubishi"]

vehicle_id = "1234"  # does not support spaces " "

gps_update_rate = 5  # seconds
connection_interface_wifi_scan_rate = 30  # seconds

import ssl

mqtt_broker_IP = "18.159.1.128"  # private AWS VM
CACERT_PATH = "/flash/cert/ca.pem"
KEY_PATH = "/flash/cert/client.key"
CERT_PATH = "/flash/cert/client.pem"
MQTT_SSL_PARAMS = {"cert_reqs": ssl.CERT_REQUIRED, "keyfile": KEY_PATH, "certfile": CERT_PATH, "ca_certs": CACERT_PATH}
