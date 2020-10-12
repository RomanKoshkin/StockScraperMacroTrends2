import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import numpy as np
import pickle
from datetime import datetime, timedelta
import os
import json
import re
import requests

outfname = 'links.txt'
# to fix the underscore and replace with dots
tofix = ["BH.A",
            "AKO.B",
            "AKO.A",
            "JW.A",
            "JW.B",
            "HVT.A",
            "CRD.A",
            "CRD.B",
            "WSO.B",
            "GEF.B",
            "LEN.B",
            "HEI.A",
            "MOG.B",
            "MOG.A",
            "PBR.A",
            "GTN.A",
            "BF.B",
            "STZ.B",
            "BF.A",
            "GRP.U",
            "RDS.A",
            "RDS.B",
            "EBR.B",
            "BRK.A",
            "BRK.B",
            "BIO.B",
            "LGF.A",
            "LGF.B"]

def get_base_url(ticker):
    global tofix
    full_link = df[df.ticker == ticker].link.item().split('=\'')[1].split('\'>')[0]
    lnk = '/'.join(full_link.split('/')[:-1])
    if ticker in tofix:
        lnk = lnk.replace('_', '.')
    return lnk


# ==Recent== data on 7505 companies by [ticker, name, industry, country, PB, PS, PE]
df = pd.read_pickle("MT.pickle")


if 'links.txt' in os.listdir():
    os.remove(outfname)

indicators = ['revenue',
            'ebitda',
            'net-income',
            'shares-outstanding',
            'operating-income',
            'total-assets',
            'total-liabilities',
            'long-term-debt',
            'total-share-holder-equity',
            'cash-on-hand',
            'current-ratio',
            'quick-ratio',
            'debt-equity-ratio',
            'roe',
            'roa',
            'roi',
            'return-on-tangible-equity',
            'pe-ratio', 
            'price-sales',
            'price-book',
            'price-fcf']

tickers = df.ticker.to_list()
for i, ticker in enumerate(tickers):
    for indicator in indicators:
        url = get_base_url(ticker) + '/' + indicator
        print(i, url)
        with open (outfname, 'a') as f:
            f.writelines(url + "\n")