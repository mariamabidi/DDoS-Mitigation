import os
import yaml

NUM_NODES = 4  # 🔁 Change to however many you want!

compose_path = "/Users/mariamabidi/Desktop/DDoS-Mitigation/docker-compose.yml"
base_port = 5000

# Load existing compose file
with open(compose_path, "r") as f:
    compose = yaml.safe_load(f)

# Reset all node entries
compose["services"] = {
    k: v for k, v in compose["services"].items() if not k.startswith("node")
}

# Add nodes dynamically
for i in range(1, NUM_NODES + 1):
    node_name = f"node{i}"
    host_port = base_port + i + 1

    compose["services"][node_name] = {
        "build": "./src/node",
        "container_name": node_name,
        "ports": [f"{host_port}:5000"],
        "volumes": ["./src/shared:/app/shared"],
        "depends_on": ["coordinator"]
    }

# Write updated compose file
with open(compose_path, "w") as f:
    yaml.dump(compose, f, default_flow_style=False)

print(f"✅ Updated docker-compose.yml with {NUM_NODES} nodes!")

# Optionally run docker
os.system("docker compose up --build")
