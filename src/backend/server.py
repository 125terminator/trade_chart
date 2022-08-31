import logging
from websocket_server import WebsocketServer
from random import randrange
import time
import datetime

def rn():
	return randrange(-20, 20)
def new_client(client, server):
	print("new client connected")
	import json
	from time import sleep
	f = open('../../data/sbin-08-22.json', 'r')
	a = json.load(f)
	start, o, h, l, c, v = a['data']['candles'][-1]
	f.close()
	for i in range(100000):
		sleep(1)
		start = start + 1e6
		o+=rn()
		h+=rn()
		l+=rn()
		c+=rn()
		v+=randrange(20)
		data = "[{},{},{},{},{},{}]".format(start, o, h, l, c, v)
		server.send_message_to_all(data)
		print(datetime.datetime.fromtimestamp(start/1000.0), data)

server = WebsocketServer(host='127.0.0.1', port=13254, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.run_forever()



# https://github.com/Pithikos/python-websocket-server