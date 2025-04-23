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
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv("/Users/mariamabidi/Desktop/DDoS-Mitigation/src/data/cleaned/ddos_whole_data_cleaned.csv")
df = df.sample(frac=0.3, random_state=42)
top_features = ['direction_L2R', 'destination_192.168.5.122', 'totalDestinationPackets', 'appName_HTTPImageTransfer',
                'totalSourcePackets', 'sourceTCPFlagsDescription_S', 'sourcePort', 'totalDestinationBytes',
                'destinationTCPFlagsDescription_R,A', 'source_192.168.1.105', 'destinationPort',
                'sourcePayloadAsBase64_len', 'appName_HTTPWeb', 'destinationPayloadAsBase64_len', 'totalSourceBytes']


# Encode categorical columns
object_cols = df.select_dtypes(include=['object']).columns
df = pd.get_dummies(df, columns=object_cols, drop_first=True)
df = df[top_features + ['Label']]  # Keep only top features and label


# Features and labels
y = df['Label']
X = df.drop('Label', axis=1)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Train model
model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=23, class_weight='balanced')
model.fit(X_resampled, y_resampled)

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
top_n = 30  # You can adjust this
feat_df = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False).head(top_n)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=feat_df, palette="viridis", legend=False)
plt.title("Top Feature Importances (Random Forest)")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("../shared/feature_importance.png")
print("📌 Saved: feature_importance.png (Top 20 features)")