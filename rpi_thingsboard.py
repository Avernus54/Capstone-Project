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

client.loop_start()

# Get user input for soil moisture
while True:
    try:
        soil_moisture = float(input("Enter soil moisture value (0-100%): "))
        
        # Validate input range
        if soil_moisture < 0 or soil_moisture > 100:
            print("Please enter a value between 0 and 100")
            continue
        
        payload = {
            "device_id": "raspi-soil-01",
            "soil_moisture": round(soil_moisture, 2)
        }
        client.publish("v1/devices/me/telemetry", json.dumps(payload), 1)
        print(f"Published: {payload}")
        
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
    except Exception as e:
        print(f"Error: {e}")
