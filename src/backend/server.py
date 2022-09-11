import asyncio
import time
import threading

from OHLC import OHLC
from serverWs import run as runWs
from serverHttp import run as runHttp
from DB import User, Date

ohlc = OHLC('../../data/reliance.csv', clean=False)
db = {}
db['user'] = User()
db['date'] = Date()

t1 = threading.Thread(target=runWs, args=(ohlc, db, ))
t2 = threading.Thread(target=runHttp, args=(ohlc, db, ))
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