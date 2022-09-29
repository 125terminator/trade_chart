import asyncio
import time
import threading

from OHLC import OHLC
from serverWs import run as runWs
from serverHttp import run as runHttp
from DB import User, Date

reliance = OHLC('../../data/reliance.csv', clean=False)
nse = OHLC('../../data/nse.csv', clean=False)
ohlc_list = {'reliance': reliance, 'nse': nse}
date_db = Date()
user_db = User(date_db=date_db)
db = {'user': user_db, 'date': date_db}

t1 = threading.Thread(target=runWs, args=(ohlc_list, db, ))
t2 = threading.Thread(target=runHttp, args=(ohlc_list, db, ))
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