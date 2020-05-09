import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans


# retrieve the metrics data
df = pd.read_csv("key_metrics.csv", parse_dates=["date"])

# test with 2019Q4 quarterly data
quarterly = df.loc[(df.date.dt.month.isin([10, 11, 12]) & (df.date.dt.year == 2019))]
quarterly.sort_values(by="date", ascending=False, inplace=True)
quarterly.drop_duplicates(subset="symbol", keep="first", inplace=True)

# preprocessing
metrics = ['symbol', 'Revenue per Share', 'Net Income per Share',
       'Operating Cash Flow per Share', 'Free Cash Flow per Share',
       'Cash per Share', 'Book Value per Share',
       'Tangible Book Value per Share', 'Shareholders Equity per Share',
       'Interest Debt per Share', 'Market Cap', 'Enterprise Value', 'PE ratio',
       'POCF ratio', 'PFCF ratio', 'PB ratio',
       'PTB ratio', 'Enterprise Value over EBITDA',
       'EV to Operating cash flow', 'EV to Free cash flow', 'Earnings Yield',
       'Free Cash Flow Yield', 'Debt to Equity', 'Debt to Assets',
       'Net Debt to EBITDA',
       'Income Quality', 'Payout Ratio', 'Intangibles to Total Assets',
       'Graham Net-Net',
       'Net Current Asset Value',
       'Capex per Share']
sub_qrt = quarterly[metrics]
sub_qrt.dropna(inplace=True)
sub_qrt.reset_index(drop=True, inplace=True)

# simple kmeans
symbol = sub_qrt.symbol
data = sub_qrt.drop(columns="symbol")

scaler = MinMaxScaler()
scaler.fit(data)
data_norm = scaler.transform(data)

kmeans = KMeans(n_clusters=9, random_state=0).fit(data_norm)

# find clusters
nasdaq = pd.read_csv("NASDAQ.csv")
nyse = pd.read_csv("NYSE.csv")
mapping = pd.concat([nasdaq, nyse])[["Symbol", "Description"]].rename(columns={"Symbol":"symbol", "Description":"company"})
sub_qrt = pd.merge(sub_qrt, mapping, on="symbol", how="left")

# test with 4 clusters
cluster0 = sub_qrt[kmeans.labels_ == 0].sort_values(by="Market Cap", ascending=False)[:20]
cluster1 = sub_qrt[kmeans.labels_ == 1].sort_values(by="Market Cap", ascending=False)[:20]
cluster2 = sub_qrt[kmeans.labels_ == 3].sort_values(by="Market Cap", ascending=False)[:20]
cluster3 = sub_qrt[kmeans.labels_ == 6].sort_values(by="Market Cap", ascending=False)[:20]
cluster0.to_csv('cluster0.csv', index=False)
cluster1.to_csv('cluster1.csv', index=False)
cluster2.to_csv('cluster2.csv', index=False)
cluster3.to_csv('cluster3.csv', index=False)
