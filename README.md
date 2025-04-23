## 🚨 Distributed DDoS Detection and Mitigation System

A scalable, containerized system for detecting and mitigating Distributed Denial-of-Service (DDoS) attacks using machine learning and Docker-based microservices.

📜 Overview
 - This project implements a distributed real-time DDoS detection system that:
 - Uses multiple Dockerized analysis nodes to classify network traffic.
 - Relays suspicious activity to a central Coordinator service.
 - Leverages a Random Forest machine learning model trained on features from the CICIDS 2010 dataset.
 - Can be scaled horizontally by adding more analysis nodes.

⚙️ Requirements
 - Python 3.10+
 - Docker & Docker Compose
 - pip install -r requirements.txt (for local Python testing)

🚀 Getting Started
1. 📊 Clean & Prepare Data
    ```bash
      cd src/scripts
      python clean_data.py

2. 🧠 Train the Model
   ```bash
   python train_model.py

3. 🐳 Start the Distributed System
   ```bash
   docker-compose up --build

4. 📡 Simulate Traffic
   ```bash
   python src/scripts/send_traffic.py

5. 📈 Evaluate Model Performance (Optional)
   ```bash
   python src/scripts/evaluate_model.py


🧩 Future Improvements
 - Real-time alerting and dashboard
 - Automatic IP blocking (firewall integration)
 - Online learning for continuous model updates
 - Cloud-native deployment with Kubernetes

