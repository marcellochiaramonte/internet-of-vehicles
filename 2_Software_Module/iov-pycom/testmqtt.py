import usocket as socket
import ssl
from network import WLAN
import time
import libraries.uasyncio as asyncio
from project.mqtt.mqtt_connection import IoVMQTTClient


async def start():
    mqtt_client = IoVMQTTClient()


loop = asyncio.get_event_loop()
loop.create_task(start())
loop.run_forever()
