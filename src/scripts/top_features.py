from joblib import load
import pandas as pd

model, feature_list = load("/Users/mariamabidi/Desktop/DDoS-Mitigation/src/shared/ddos_model.joblib")
importances = model.feature_importances_

feat_df = pd.DataFrame({
    'Feature': feature_list,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

top_feature_list = feat_df['Feature'].head(20).tolist()

print(top_feature_list)
