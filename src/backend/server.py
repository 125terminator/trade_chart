import logging
from websocket_server import WebsocketServer
from random import randrange
import datetime
from time import sleep
import datetime
from dateutil import parser

import pandas as pd

from OHLC import OHLC
from utils import *

ohlc = OHLC('../../data/reliance.csv', clean=False)

def new_client(client, server):
	print("new client connected")
	df = ohlc.df
	state = get_state()
	startTime = parser.parse(state['now'], ignoretz=True)
	ind = greater_equal_index(df, startTime)
	for i in range(100000):
		sleep(1)
		start = df.index[ind].tz_localize('Asia/Kolkata')
		o, h, l, c, v = df.iloc[ind]
		data = '["{}",{},{},{},{},{}]'.format(start, o, h, l, c, v)
		server.send_message(client, data)
		state['now'] = f'{start}'
		push_state(state)
		ind += 1
		print(data)

server = WebsocketServer(host='127.0.0.1', port=13254, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.run_forever()



# https://github.com/Pithikos/python-websocket-server