import pandas as pd

# Load item property files
df1 = pd.read_csv("data/item_properties_part1.csv", low_memory=False)
df2 = pd.read_csv("data/item_properties_part2.csv", low_memory=False)

# Combine both
df = pd.concat([df1, df2])

# Drop rows with missing values
df = df.dropna(subset=["itemid", "value"])

# Group by itemid, join all property values into a text blob
grouped = df.groupby("itemid")["value"].apply(lambda x: " ".join(map(str, x))).reset_index()
grouped.columns = ["item_id", "value"]

# Save to data/items.csv
grouped.to_csv("data/items.csv", index=False)
print("✅ Combined text data saved to data/items.csv")
