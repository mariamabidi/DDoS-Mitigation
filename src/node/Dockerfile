# node/Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask pandas scikit-learn joblib requests

CMD ["python", "app.py"]
