import pandas as pd

df = pd.read_csv("201809-citibike-tripdata.csv")
df = df.groupby(['start station id']).sort_value()

print(df)

