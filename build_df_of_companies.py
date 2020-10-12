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

def get_base_url(ticker):
    full_link = df[df.ticker == ticker].link.item().split('=\'')[1].split('\'>')[0]
    return '/'.join(full_link.split('/')[:-1])

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_financial_ratios(ticker, df):
    full_link = df[df.ticker == ticker].link.item().split('=\'')[1].split('\'>')[0]
    url = '/'.join(full_link.split('/')[:-1]) + '/financial-ratios'
    r = requests.get(url)
    t = r.text

    l = t.split('var originalData = ')
    l = l[1].split(']')
    l = l[0] + ']'

    freeFromTags = cleanhtml(l)
    return json.loads(freeFromTags)




with open ('/Users/romankoshkin/mt/stocksByIndustry.txt', 'r') as f:
    urls = f.readlines()

AA = []
for i, url in enumerate(urls):
    print(f'{i} of {len(urls)}')
    r = requests.get(url)
    t = r.text

    l = t.split('var data = ')
    l = l[1].split(']')
    l = l[0] + ']'
    
    AA += json.loads(l)
df = pd.DataFrame(AA)

i = ["ORLY"]
for j in i:
    df.drop(df[df.ticker==j].index, inplace=True)
df.to_pickle("MT.pickle")

