import paho.mqtt.client as mqtt
import json
import time

ACCESS_TOKEN = "zf1ztnuspiiv8jv0u9r9"
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect("mqtt.thingsboard.cloud", 1883, 60)

while True:
    payload = {"soil_moisture": 42.5}
    client.publish("v1/devices/me/telemetry", json.dumps(payload), 1)
    time.sleep(10)
