import paho.mqtt.client as mqtt
import json
import time
import random

ACCESS_TOKEN = "zf1ztnuspiiv8jv0u9r9"
BROKER = "demo.thingsboard.io"  # or your server IP

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

client.connect(BROKER, 1883, 60)

while True:
    data = {
        "temperature": random.randint(20, 35),
        "humidity": random.randint(50, 80)
    }

    client.publish("v1/devices/me/telemetry", json.dumps(data))
    print("Sent:", data)

    time.sleep(5)