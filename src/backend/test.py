# from utils import *
import numpy as np
from dateutil import parser
from OHLC import OHLC

def gt(df, start):
    return df.index.searchsorted(start)

def open_index(df, start):
    ind = df.index.searchsorted(start)
    while ind > 0:
        if df.index[ind-1].hour > df.index[ind].hour:
            return df.index[ind]
        ind -= 1
    return ind

nse = OHLC('../../data/nse.csv', clean=False)

start = parser.parse("2021-12-06T09:36:00+0530", ignoretz=True)
print(gt(nse.df, start))
# print(open_index(nse.df, start))