import asyncio
import time
import threading
import os

from OHLC import OHLC
from serverWs import run as runWs
from serverHttp import run as runHttp
from DB import User, Date

# reliance = OHLC('../../data/reliance.csv', clean=False)
# nse = OHLC('../../data/nse.csv', clean=False)
class Historical:
    def __init__(self):
        self.ohlc = {}

    def get(self, symbol):
        if symbol not in self.ohlc:
            file = f'../../data/{symbol}.csv'
            if not os.path.isfile(file):
                return None
            data = OHLC(file, clean=False)
            self.ohlc.update({symbol: data})
            return data
        return self.ohlc[symbol]

historical = Historical()
date_db = Date()
user_db = User(date_db=date_db)
db = {'user': user_db, 'date': date_db}

t1 = threading.Thread(target=runWs, args=(historical, db, ))
t2 = threading.Thread(target=runHttp, args=(historical, db, ))
t1.start()
t2.start()
try:
    t1.join()
except:
    print('keyboard ctrl-c')

try:
    t2.join()
except:
    print('keyboard ctrl-c')