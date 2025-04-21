import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
)
from joblib import dump

# Load dataset
df = pd.read_csv("/Users/mariamabidi/Desktop/DDoS-Mitigation/src/data/cleaned/ddos_whole_data_cleaned.csv")

# Encode categorical columns
df = pd.get_dummies(df, drop_first=True)

# Features and labels
y = df['Label']
X = df.drop('Label', axis=1)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=55)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Text reports
print("\n✅ Classification Report:\n")
print(classification_report(y_test, y_pred))

print("\n🧮 Confusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# Save model + feature names
os.makedirs("../shared", exist_ok=True)
dump((model, list(X.columns)), "../shared/ddos_model.joblib")
print("\n💾 Model saved to: ../shared/ddos_model.joblib")

# 📊 Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Normal', 'DDoS'], yticklabels=['Normal', 'DDoS'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig("../shared/confusion_matrix.png")
print("📊 Saved: confusion_matrix.png")

# 📈 Plot ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 4))
plt.plot(fpr, tpr, color='darkorange', label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.tight_layout()
plt.savefig("../shared/roc_curve.png")
print("📈 Saved: roc_curve.png")

# 🔍 Plot Feature Importance
importances = model.feature_importances_
feat_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(8, 4))
sns.barplot(x='Importance', y='Feature', data=feat_df)
plt.title("Feature Importance (Random Forest)")
plt.tight_layout()
plt.savefig("../shared/feature_importance.png")
print("📌 Saved: feature_importance.png")