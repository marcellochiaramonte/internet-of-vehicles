FROM python:3.9.1-alpine

RUN pip install requests

RUN pip install paho-mqtt

COPY source source

CMD ["python","/source/main.py"]


