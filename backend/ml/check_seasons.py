import pandas as pd

df = pd.read_csv("data.csv")
print("✅ Total rows:", len(df))
print("✅ Seasons in dataset:", sorted(df["season"].unique()))
print("✅ Rows per season:")
print(df["season"].value_counts().sort_index())
