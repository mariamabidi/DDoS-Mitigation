🚨 Distributed DDoS Detection and Mitigation System

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
      cd src/scripts
      python clean_data.py


