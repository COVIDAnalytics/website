import pandas as pd
from colMapping import mapping
d = "0331"

df = pd.read_csv('../data/raw/{}.csv'.format(d))

#remove top column
df.columns = df.iloc[0,:]
df = df.drop(0)

#rename columns
df.columns = [mapping[c] for c in df.columns]

#remove commas from numeric columns
df = df.loc[df["Notes"] != "EXCLUDE"]

df.to_csv('../data/{}.csv'.format(d),index=False)
