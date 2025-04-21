import requests
import random
import time

# Define sample traffic flows
normal_traffic = {
    "source": "192.168.1.100",
    "totalSourceBytes": 1500,
    "totalDestinationBytes": 500,
    "totalSourcePackets": 30,
    "totalDestinationPackets": 10
}

ddos_traffic = {
    "source": "10.10.10.10",  # Suspicious IP
    "totalSourceBytes": 1000000,
    "totalDestinationBytes": 200,
    "totalSourcePackets": 5000,
    "totalDestinationPackets": 5
}

# Choose which traffic to test
flows = [normal_traffic, ddos_traffic]

# Node URLs (localhost ports mapped in docker-compose)
nodes = ["http://localhost:5002/analyze", "http://localhost:5003/analyze"]

print("🚀 Sending traffic...\n")

for flow in flows:
    for url in nodes:
        print(f"→ Sending to {url}: {flow['source']}")
        response = requests.post(url, json=flow)
        print(f"  ← Response: {response.json()}\n")
        time.sleep(1)  # Slight delay to simulate real-time

print("✅ Done sending traffic.")
