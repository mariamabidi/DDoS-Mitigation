# clean_data.py
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

# Final features you want to retain (plus Label)
base_features = [
    'direction', 'destination', 'totalDestinationPackets', 'appName',
    'totalSourcePackets', 'sourceTCPFlagsDescription', 'sourcePort', 'totalDestinationBytes',
    'destinationTCPFlagsDescription', 'source', 'destinationPort',
    'sourcePayloadAsBase64', 'appName', 'destinationPayloadAsBase64', 'totalSourceBytes'
]
features_to_keep = list(set(base_features)) + ['Label']

# Load and sample from each raw file
dfs = []

for path in raw_paths:
    df = pd.read_csv(path)
    sample = df.sample(frac=0.2, random_state=42)
    dfs.append(sample)

# Combine all sampled data
df = pd.concat(dfs, ignore_index=True)

# Convert labels
df["Label"] = df["Label"].apply(lambda x: 1 if "Attack" in str(x) else 0)

# Keep only selected columns that exist
features_found = [col for col in features_to_keep if col in df.columns]
df = df[features_found]

# Handle payload lengths and drop raw base64 fields
for col in ["sourcePayloadAsBase64", "destinationPayloadAsBase64"]:
    if col in df.columns:
        df[col] = df[col].fillna("missing")
        df[f"{col}_len"] = df[col].apply(lambda x: len(x) if isinstance(x, str) else 0)
        df.drop(columns=[col], inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Save cleaned dataset
output_dir = "../data/cleaned"
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "ddos_whole_data_cleaned.csv"), index=False)

print(f"\n✅ Cleaned dataset saved to: {output_dir}/ddos_whole_data_cleaned.csv")
