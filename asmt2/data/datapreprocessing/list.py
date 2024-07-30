import pandas as pd
df = pd.read_csv("grouped_data_bynearest_station.csv")
df = df['location']
df = set(df)
print(df)
