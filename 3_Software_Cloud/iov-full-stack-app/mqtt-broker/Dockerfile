FROM eclipse-mosquitto

COPY ./mosquitto.conf /mosquitto/config/mosquitto.conf

COPY ./certs/ca.crt /mosquitto/config/ca.crt
COPY ./certs/mqtt_broker.crt /mosquitto/config/mqtt_broker.crt
COPY ./certs/mqtt_broker.key /mosquitto/config/mqtt_broker.key

RUN adduser -D nonroot
USER nonroot