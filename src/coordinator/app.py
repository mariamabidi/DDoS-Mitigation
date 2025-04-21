# coordinator/app.py

from flask import Flask, request, jsonify
from collections import defaultdict

app = Flask(__name__)
print("🚀 Coordinator starting...")
# Track alert counts per IP
alert_counts = defaultdict(int)
BLOCK_THRESHOLD = 2  # How many nodes need to report before blocking

blocklist = set()

@app.route('/report', methods=['POST'])
def report_alert():
    print("🔥 DEBUG: /report endpoint hit")
    data = request.get_json()
    print("🔎 Incoming data:", data)

    ip = data.get("source_ip")
    if ip:
        alert_counts[ip] += 1
        print(f"[⚠️ ALERT] IP {ip} reported ({alert_counts[ip]}/{BLOCK_THRESHOLD})")

        if alert_counts[ip] >= BLOCK_THRESHOLD:
            if ip not in blocklist:
                print(f"[🔥 BLOCKED] IP: {ip}")
                blocklist.add(ip)

    else:
        print("❌ No source_ip found in request.")

    return jsonify({"status": "received"})

@app.route('/blocklist', methods=['GET'])
def get_blocklist():
    return jsonify(list(blocklist))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
