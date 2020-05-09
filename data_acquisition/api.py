import requests
import simplejson
import pandas as pd
import numpy as np


# read symbol data
nasdaq = pd.read_csv('NASDAQ.csv')
nyse = pd.read_csv('NYSE.csv')
stock_list = nasdaq.Symbol.tolist() + nyse.Symbol.tolist()

# api function to fetch data
def company_key_metric(stock):
    """
    Performs data acquisition of the key metrics for a specific stock.
    :param stock: the stock symbol
    :return: all key metrics data of that stock
    """
    key_metric = requests.get(f"https://financialmodelingprep.com/api/v3/company-key-metrics/{stock}?period=quarter").json()

    return key_metric

# Structure of the returned json file
# - symbol
# - metrics
#     - date
#     - detailed metric

def json2df(stock_list):
    """
    Get data via API and transform json into dataframe.
    :param stock_list: list of stock symbols
    :return: dataframe with key metrics of all stocks
    """
    ct = 0  # count stock
    dict_ = {}  # collect all columns

    for stock in stock_list:
        js = company_key_metric(stock)  # metrics in json
        if js == {}:  # some are empty
            continue
        dict_["symbol"] = dict_.get("symbol", []) + [js["symbol"]] * len(js["metrics"])  # repeat symbol as 1st column
        for k in js["metrics"][0].keys():  # metrics names
            dict_[k] = dict_.get(k, []) + [d[k] for d in js["metrics"]]  # compile into a list

        ct += 1
        if ct % 100 == 0:
            print(f"{ct} stocks processed ...")

    df = pd.DataFrame(dict_)

    # convert to float data type
    for i in range(len(df.columns) - 2):
        df[df.columns[i + 2]].astype('float64')

    return df

df = json2df(stock_list)
df.to_csv('key_metrics.csv', index=False)
