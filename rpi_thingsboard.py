import paho.mqtt.client as mqtt
import json
import time

# ThingsBoard MQTT configuration
ACCESS_TOKEN = "zf1ztnuspiiv8jv0u9r9"
BROKER = "mqtt.thingsboard.cloud"
PORT = 1883

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(BROKER, PORT, 60)

def read_soil_moisture():
    """Return hardcoded soil moisture value for testing"""
    return 65.5

client.loop_start()

while True:
    try:
        soil_moisture = read_soil_moisture()
        payload = {
            "device_id": "raspi-soil-01",
            "soil_moisture": round(soil_moisture, 2)
        }
        client.publish("v1/devices/me/telemetry", json.dumps(payload), 1)
        print(f"Published: {payload}")
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(10)
