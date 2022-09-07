from OHLC import OHLC
from pandas.tseries.frequencies import to_offset
import pandas as pd
import numpy as np
import pickle

# pd.to_datetime("2022-09-06 01:43:06.115000")
# print(pd.DatetimeIndex([pd.to_datetime("2015-04-09T15:29:00+0530")]).astype(np.int64))
# o = OHLC('../../data/reliance.csv')
# ohlc = OHLC('../../data/reliance.csv', clean=False)
# with open('ohlc.pkl', 'wb') as f:
#     pickle.dump(ohlc, f, -1)

# with open('ohlc.pkl', 'rb') as f:
#     ohlc = pickle.load(f)
#     print(ohlc.df)

# mins = 2
# df = o.toInterval(mins)
# # print(df.ge("2022-09-06 01:43:06.115000", axis='index'))

# # print(df.index.ge(pd.to_datetime("2015-03-02T09:17:00.115000")))
# print((df.index >= pd.to_datetime("2015-03-02T09:17:00.115000")) & (df.index <= pd.to_datetime("2015-03-02T09:22:00")))

1662408786115
1428573540000