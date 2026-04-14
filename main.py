import paho.mqtt.client as mqtt
import json
import time

ACCESS_TOKEN = "zf1ztnuspiiv8jv0u9r9"
BROKER = "demo.thingsboard.io"

def on_connect(client, userdata, flags, rc):
    print("Connected with code:", rc)

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.on_connect = on_connect


client.connect(BROKER, 1883, 60)
client.loop_start()

while True:
    payload = {
        "temperature": 30,
        "humidity": 70
    }

    result = client.publish(
        "v1/devices/me/telemetry",
        json.dumps(payload)
    )

    print("Publish result:", result.rc)

    time.sleep(5)