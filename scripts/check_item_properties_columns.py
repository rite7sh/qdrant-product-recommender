import pandas as pd

#Part 1
df1 = pd.read_csv("data/item_properties_part1.csv", low_memory=False, nrows=5)
print("Columns in item_properties_part1.csv:")
print(df1.columns)
print("\nSample rows:")
print(df1.head())

#Part 2
df2 = pd.read_csv("data/item_properties_part2.csv", low_memory=False, nrows=5)
print("\nColumns in item_properties_part2.csv:")
print(df2.columns)
print("\nSample rows:")
print(df2.head())
