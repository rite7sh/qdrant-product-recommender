import pandas as pd
from pathlib import Path

#Path
DATA_DIR = Path("data")
PART1_PATH = DATA_DIR / "item_properties_part1.csv"
PART2_PATH = DATA_DIR / "item_properties_part2.csv"
OUTPUT_PATH = DATA_DIR / "items.csv"

#Read CSV
print("Reading part1 and part2...")
df1 = pd.read_csv(PART1_PATH)
df2 = pd.read_csv(PART2_PATH)

#Combine both part
print("Concatenating...")
df = pd.concat([df1, df2], ignore_index=True)

#remove missing values or duplicates
df.dropna(inplace=True)
df.drop_duplicates(subset=["itemid", "property", "value"], inplace=True)

#Optional: Keep latest property values
df.sort_values(by="timestamp", ascending=False, inplace=True)
df = df.drop_duplicates(subset=["itemid", "property"], keep="first")

#Pivot to wide format
print("Pivoting to wide format...")
df_wide = df.pivot_table(index="itemid", columns="property", values="value", aggfunc="first").reset_index()

#Save preprocessed data
print(f"Saving to {OUTPUT_PATH}")
df_wide.to_csv(OUTPUT_PATH, index=False)
print("Done!")
