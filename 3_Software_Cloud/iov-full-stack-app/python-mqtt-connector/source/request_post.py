import requests
from paho.mqtt.client import MQTTMessage
import json


class PostRequest:
    def __init__(self, docker_env=True):
        self.url = "http://iov-backend:8080/api/" if docker_env else "http://localhost:8080/api/"
        self.metric_path_url = "event/new/multiple"
        self.location_path_url = "location/new/multiple"

    def post(self, path, params, http_body):
        url = self.url + path
        req = requests.post(url, params=params, data=http_body)
        print(req.status_code, url, params, http_body)

    def decode_message(self, message: MQTTMessage):
        # expects format being vehicle/1234/live
        try:
            _, carId, metric_type = message.topic.split("/")
            try:
                payload = json.loads(message.payload.decode("utf-8"))
                # print("received payload:", payload)

                if metric_type == "live":
                    try:
                        metric_buffer = json.dumps(payload["m"])
                        # print("metrics", metric_buffer)
                        location_buffer = json.dumps(payload["p"])
                        # print("location", location_buffer)

                        try:
                            metric_params = {"carId": carId}
                            self.post(self.metric_path_url, metric_params, metric_buffer)
                        except:
                            print("http post exception metrics")

                        try:
                            location_params = {"carId": carId}
                            self.post(self.location_path_url, location_params, location_buffer)
                        except:
                            print("http post exception metrics")
                    except KeyError:
                        print("exception: key not available at the json object")

            except:
                print("JSON Payload not on correct format or not a string")

        except ValueError:
            print("check the format of the message topic")
