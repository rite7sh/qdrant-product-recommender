import pandas as pd

df1 = pd.read_csv("data/item_properties_part1.csv", low_memory=False)
df2 = pd.read_csv("data/item_properties_part2.csv", low_memory=False)

# Combine both datasets
df = pd.concat([df1, df2])

# Show top 20 most common properties
property_counts = df["property"].value_counts()
print("Top 20 most common property IDs:")
print(property_counts.head(20))

# Optional: print unique properties
# print("\nAll unique property values:")
# print(df["property"].unique())
