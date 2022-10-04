import logging
from websocket_server import WebsocketServer
from random import randrange
import datetime
from time import sleep
import datetime
from dateutil import parser
import threading
import json
from threading import Lock

import pandas as pd

from OHLC import OHLC
from utils import *

mutex = Lock()

historical = None
db = None
clients = {}
'''
key -> client id
val -> (client, properties)

properties:
	pause: true -> do not stream data to client
	subscription
		all -> receive all data
		trades -> receive only squarred off trade data
'''


def new_client(client, server):
	global clients

def client_left(client, server):
	global clients
	mutex.acquire()
	try:
		clients.pop(client['id'], None)
	finally:
		mutex.release()

def read(client, server, message):
	global clients
	print(json.loads(message))
	mutex.acquire()
	try:
		clients[client['id']] = (client, json.loads(message))
		print(clients)
	finally:
		mutex.release()


def stream_to_client(client, server, data, props):
	if props['pause']:
		return
	subs = props['subscription']
	if subs == 'all':
		server.send_message(client, json.dumps(data))
	if subs == 'trades':
		server.send_message(client, json.dumps(data['trades']))


def stream_to_clients(server, data):
	global clients
	mutex.acquire()
	try:
		for id, val in clients.items():
			stream_to_client(val[0], server, data, val[1])
	finally:
		mutex.release()

def all_client_ready():
	global clients
	for id, val in clients.items():
		if val[1]['pause']:
			return False
	return len(clients) > 0

def stream(server):
	global clients
	reliance, nse, ashokley = historical.get('reliance'), historical.get('nse'), historical.get('ashokley')
	while True:
		sleep(1)
		if not all_client_ready():
			continue

		startTime = parser.parse(db['date'].now, ignoretz=True)
		ind = nse.ge_index(startTime)
		nse_open_price = nse.df.Open[nse.open_index(ind)]
		nse_current_price = nse.df.Close[ind]
		nse_change = round(get_change(
			current=nse_current_price, previous=nse_open_price), 2)

		start = nse.df.index[ind].tz_localize('Asia/Kolkata')
		o, h, l, c, v = nse.df.iloc[ind]
		nse_data = [str(start), o, h, l, c, v]

		ind = reliance.ge_index(startTime)
		start = reliance.df.index[ind].tz_localize('Asia/Kolkata')
		o, h, l, c, v = reliance.df.iloc[ind]
		reliance_data = [str(start), o, h, l, c, v]

		ind = ashokley.ge_index(startTime)
		start = ashokley.df.index[ind].tz_localize('Asia/Kolkata')
		o, h, l, c, v = ashokley.df.iloc[ind]
		ashokley_data = [str(start), o, h, l, c, v]
		data = {
                    'live': {'nse': nse_data, 'reliance': reliance_data, 'ashokley': ashokley_data},
               					'holdings': db['user'].transactions,
               					'nse_change': nse_change,
               					'trades': db['user'].trades,
                }
		stream_to_clients(server, data)
		# server.send_message_to_all(json.dumps(data))
		start = start.replace(second=start.second+1)
		db['date'].set(f'{start}')


def run(_historical, _db):
	global historical, db, clients
	historical = _historical
	db = _db

	server = WebsocketServer(host='127.0.0.1', port=13254, loglevel=logging.INFO)
	server.set_fn_new_client(new_client)
	server.set_fn_client_left(client_left)
	server.set_fn_message_received(read)
	t1 = threading.Thread(target=stream, args=(server, ))
	t1.start()
	server.run_forever()


# https://github.com/Pithikos/python-websocket-server
