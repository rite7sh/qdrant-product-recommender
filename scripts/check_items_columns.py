import pandas as pd

df = pd.read_csv("data/items.csv", low_memory=False)

print("🧾 Columns in items.csv:")
print(df.columns.tolist())
print("\n🔍 Sample rows:")
print(df.head())
