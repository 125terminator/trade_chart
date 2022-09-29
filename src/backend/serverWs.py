import logging
from websocket_server import WebsocketServer
from random import randrange
import datetime
from time import sleep
import datetime
from dateutil import parser
import threading
import json

import pandas as pd

from OHLC import OHLC
from utils import *

ohlc_list = None
db = None
clients = None


def new_client(client, server):
	pass
	# global clients
	# clients = client

def client_left(client, server):
	global clients
	clients = None

def read(client, server, message):
	global clients
	# Logic to pause or resume streaming
	if clients is not None:
		clients = None
	else:
		clients = client

def stream(server):
	global clients
	reliance, nse = ohlc_list['reliance'], ohlc_list['nse']
	startTime = parser.parse(db['date'].now, ignoretz=True)
	ind = reliance.ge_index(startTime)
	while True:
		sleep(1)
		if clients == None:
			continue
		
		nse_open_price = nse.df.Open[nse.open_index(ind)]
		nse_current_price = nse.df.Close[ind]
		nse_change = round(get_change(current=nse_current_price, previous=nse_open_price), 2)

		start = nse.df.index[ind].tz_localize('Asia/Kolkata')
		o, h, l, c, v = nse.df.iloc[ind]
		nse_data = [str(start), o, h, l, c, v]

		start = reliance.df.index[ind].tz_localize('Asia/Kolkata')
		o, h, l, c, v = reliance.df.iloc[ind]
		reliance_data = [str(start), o, h, l, c, v]
		data = {
			'live': {'nse': nse_data, 'reliance': reliance_data}, 
			'holdings': db['user'].transactions,
			'nse_change': nse_change
			}
		server.send_message_to_all(json.dumps(data))
		db['date'].set(f'{start}')
		ind += 1

def run(_ohlc, _db):
	global ohlc_list, db, clients
	ohlc_list = _ohlc
	db = _db


	server = WebsocketServer(host='127.0.0.1', port=13254, loglevel=logging.INFO)
	server.set_fn_new_client(new_client)
	server.set_fn_client_left(client_left)
	server.set_fn_message_received(read)
	t1 = threading.Thread(target=stream, args=(server, ))
	t1.start()
	server.run_forever()



# https://github.com/Pithikos/python-websocket-server