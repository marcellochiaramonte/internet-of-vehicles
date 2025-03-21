import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage, Client
from request_post import PostRequest
import random
import time

docker_env = True

location = "/source/certs/"
MQTTbroker = "mqtt-secure-broker"

if not docker_env:
    location = "./certs/"
    MQTTbroker = "18.159.1.128"

ca_cert = location + "ca.pem"
client_key = location + "python_paho_connector.key"
client_cert = location + "python_paho_connector.pem"

client_id = f"python-mqtt-{random.randint(0, 100)}"


http_handler = PostRequest(docker_env=docker_env)


def subscribe(client: Client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        http_handler.decode_message(msg)

    client.subscribe("#")
    print("subscribed")
    client.on_message = on_message


def connect_mqtt():
    not_connected = True

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            subscribe(client)
            not_connected = False
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = paho.Client(client_id)
    client.tls_set(ca_cert, client_cert, client_key)
    client.tls_insecure_set(True)
    # the domain name of the broker does not match the one of the certificate
    # however this is not important as both containers are on the same docker internal network
    client.on_connect = on_connect
    client.connect(MQTTbroker, 8883)

    return client


def run():
    client = connect_mqtt()
    client.loop_forever()


if __name__ == "__main__":
    try:
        run()
    except:
        print("exception on run()")
        raise
