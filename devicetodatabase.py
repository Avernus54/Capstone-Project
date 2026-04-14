import requests
import json
from datetime import datetime

# Supabase project details
SUPABASE_URL = "https://tycixfmaksnripcyxcwi.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR5Y2l4Zm1ha3NucmlwY3l4Y3dpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNzI5NTMsImV4cCI6MjA5MTc0ODk1M30.u1e6yG52Tip7vfYbR-08p6JXQsbhiA-QhmCQCrSrlYY"

# Target table endpoint
endpoint = f"{SUPABASE_URL}/rest/v1/soil_moisture"

# Example soil moisture data
payload = {
    "device_id": "raspi-soil-01",
    "moisture_level": 42.5,
    "ts": datetime.utcnow().isoformat()
}

# Headers required by Supabase
headers = {
    "apikey": SUPABASE_API_KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal"  # avoids returning full row data
}

# Send POST request
response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

print("Status:", response.status_code)
print("Response:", response.text)
