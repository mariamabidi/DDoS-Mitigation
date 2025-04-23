import pandas as pd

# Load your cleaned & encoded dataset
df = pd.read_csv("/Users/mariamabidi/Desktop/DDoS-Mitigation/src/data/cleaned/ddos_whole_data_cleaned.csv")

# Filter only DDoS entries
ddos_df = df[df['Label'] == 1]

# Show summary
print(f"\n✅ Found {len(ddos_df)} DDoS rows.\n")

# Show a few example rows
print(ddos_df.head(3).T)  # Transposed for easier viewing

# Optional: save a few DDoS examples to file for testing
ddos_df.head(5).to_csv("sample_ddos_rows.csv", index=False)
print("\n📁 Saved sample DDoS rows to: sample_ddos_rows.csv")
