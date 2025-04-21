# ✅ Updated clean_data.py
import pandas as pd
import os

# Paths to raw data
raw_paths = [
    "/Users/mariamabidi/Desktop/DDoS-Mitigation/dataset/raw/TestbedMonJun14Flows.csv",
    "/Users/mariamabidi/Desktop/DDoS-Mitigation/dataset/raw/TestbedTueJun15Flows.csv",
    "/Users/mariamabidi/Desktop/DDoS-Mitigation/dataset/raw/TestbedWedJun16Flows.csv",
    "/Users/mariamabidi/Desktop/DDoS-Mitigation/dataset/raw/TestbedThuJun17Flows.csv",
    "/Users/mariamabidi/Desktop/DDoS-Mitigation/dataset/raw/TestbedSatJun12Flows.csv",
    "/Users/mariamabidi/Desktop/DDoS-Mitigation/dataset/raw/TestbedSunJun13Flows.csv",
]

# Load and concatenate all CSVs
df = pd.concat([pd.read_csv(path) for path in raw_paths], ignore_index=True)

# Label: 1 = Attack, 0 = Normal
df["Label"] = df["Label"].apply(lambda x: 1 if "Attack" in str(x) else 0)

# Drop columns with only 1 unique value
df = df.loc[:, df.nunique() > 1]

# Optional: replace NaN base64/UTF fields with string 'missing'
for col in ["sourcePayloadAsBase64", "destinationPayloadAsBase64"]:
    if col in df.columns:
        df[col] = df[col].fillna("missing")
        df[f"{col}_len"] = df[col].apply(lambda x: len(x) if isinstance(x, str) else 0)
        df.drop(columns=[col], inplace=True)

# Drop columns that are still likely irrelevant
irrelevant_cols = [
    "sourcePayloadAsUTF", "destinationPayloadAsUTF", "generated",
    "startDateTime", "stopDateTime"
]
df.drop(columns=[col for col in irrelevant_cols if col in df.columns], inplace=True, errors='ignore')

# Drop rows with missing values
df.dropna(inplace=True)

# Save cleaned dataset
output_dir = "../data/cleaned"
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "ddos_whole_data_cleaned.csv"), index=False)
print(f"\n✅ Cleaned dataset saved to: {output_dir}/ddos_whole_data_cleaned.csv")