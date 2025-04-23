# scripts/evaluate_model.py

import pandas as pd
from joblib import load
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import os

# === Load the model and expected features ===
model_path = "../src/shared/ddos_model.joblib"
model, expected_features = load(model_path)

# === Load the new test dataset ===
new_data_path = "/src/data/cleaned/ddos_data2_cleaned.csv"  # <-- change this if your test data is elsewhere
df = pd.read_csv(new_data_path)

# === Ensure it has the same features ===
X = df[expected_features]
y = df["Label"]

# === Predict ===
y_pred = model.predict(X)
y_prob = model.predict_proba(X)[:, 1]  # For ROC curve

# === Evaluation metrics ===
print("\n✅ Classification Report:\n")
print(classification_report(y, y_pred))

print("\n🧮 Confusion Matrix:\n")
print(confusion_matrix(y, y_pred))

# === ROC Curve ===
fpr, tpr, _ = roc_curve(y, y_prob)
auc_score = roc_auc_score(y, y_prob)

plt.figure(figsize=(6, 4))
plt.plot(fpr, tpr, color='darkorange', label=f"ROC Curve (AUC = {auc_score:.2f})")
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.title("ROC Curve (Holdout Test Data)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc="lower right")

# Save the plot
os.makedirs("../src/outputs", exist_ok=True)
plt.savefig("../outputs/roc_holdout.png")
print("\n📈 ROC curve saved to: ../outputs/roc_holdout.png")
