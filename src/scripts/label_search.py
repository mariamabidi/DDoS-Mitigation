import pandas as pd

# Load your dataset (change the path as needed)
df = pd.read_csv("/Users/mariamabidi/Desktop/DDoS-Mitigation/dataset/raw/TestbedMonJun14Flows.csv")

# Loop through each column and print unique values
for column in df.columns:
    unique_vals = df[column].unique()
    print(f"\n🧩 Feature: {column}")
    print(f"🔢 Unique Values ({len(unique_vals)}):")

    # Print up to 20 unique values to avoid overwhelming output
    print(unique_vals[:20])

    if len(unique_vals) > 20:
        print("... (truncated)")
