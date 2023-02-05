import pandas as pd

df = pd.read_json("products2_data.json")
df.to_csv("products_data.csv")      