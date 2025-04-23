from joblib import load

import requests
import time

model, feature_list = load("../shared/ddos_model.joblib")
base_input = {feature: 0 for feature in feature_list}


# === Normal Traffic Example ===
normal = base_input.copy()
normal.update({
    "direction_L2R": 1,
    "destination_192.168.5.122": 1,
    "totalDestinationPackets": 20,
    "appName_HTTPImageTransfer": 1,
    "totalSourcePackets": 25,
    "sourceTCPFlagsDescription_S": 1,
    "sourcePort": 443,
    "totalDestinationBytes": 500,
    "destinationTCPFlagsDescription_R,A": 1,
    "source_192.168.1.105": 1,
    "destinationPort": 80,
    "sourcePayloadAsBase64_len": 60,
    "appName_HTTPWeb": 1,
    "destinationPayloadAsBase64_len": 70,
    "totalSourceBytes": 1500,
    "source_192.168.2.107": 0,
    "sourceTCPFlagsDescription_S,P,A": 0,
    "destination_203.73.24.75": 0,
    "sourceTCPFlagsDescription_F,S,P,A": 0,
    "destinationTCPFlagsDescription_F,A": 0
})

# === DDoS Traffic Example ===
ddos = base_input.copy()
ddos.update({
    "direction_L2L": 1,
    "destination_192.168.5.122": 1,
    "totalDestinationPackets": 4,
    "appName_HTTPWeb": 1,
    "totalSourcePackets": 6,
    "sourceTCPFlagsDescription_S": 1,
    "sourcePort": 2705,
    "totalDestinationBytes": 256,
    "destinationTCPFlagsDescription_S,A": 1,
    "source_192.168.2.106": 1,
    "destinationPort": 80,
    "sourcePayloadAsBase64_len": 7,
    "destinationPayloadAsBase64_len": 7,
    "totalSourceBytes": 392
})

# === Nodes ===
nodes = ["http://localhost:5002/analyze",  # node1
    "http://localhost:5003/analyze",  # node2
    "http://localhost:5004/analyze",  # node3
    "http://localhost:5005/analyze"  # node4
         ]

# === Send traffic ===
print("🚀 Sending traffic...\n")
for traffic in [normal, ddos]:
    for url in nodes:
        print(f"→ Sending to {url}")
        response = requests.post(url, json=traffic)
        try:
            print(f"  ← Response: {response.json()}\n")
        except Exception as e:
            print(f"  ✖ Error: {e}")
        time.sleep(1)

print("✅ Done sending traffic.")
