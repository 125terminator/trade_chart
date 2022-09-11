from calendar import month
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import datetime
import json
import pandas as pd

from OHLC import OHLC
from utils import *

ohlc = OHLC('../../data/reliance.csv', clean=False)



class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)

        if self.path == '/api/state' :
            return self.stateHandler()
        if 'stock' in params:
            self.getStockHandler(params=params)
    
    def do_POST(self): 
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        if self.path == "/api/buy":
            self.buyStockHandler(post_body)

    def buyStockHandler(self, body):
        self._set_headers()
        quantity = int(body)
    
    def sellStockHandler(self, body):
        self._set_headers()
        quantity = int(body)


    def getStockHandler(self, params):
        # print('new req with params', params)
        # startTime = datetime.datetime.fromtimestamp(int(params['startTime'][0])/1000.0)
        endTime = datetime.datetime.fromtimestamp(int(params['endTime'][0])/1000.0)
        startTime = endTime - datetime.timedelta(days=5)

        print(startTime, endTime)
        print(params['interval'][0])
        interval = int(params['interval'][0])//6000
        # interval = interval_dict[params['interval'][0]]
        data = ohlc.toInterval(interval)
        data = between_time(data, startTime, endTime).to_json(orient='table')
        data = json.loads(data)
        self._set_headers()
        # self.wfile.write(json.dumps(json.load(open('../../data/sbin-08-22.json', 'r'))).encode())
        self.wfile.write(json.dumps(data).encode())
    
    def stateHandler(self):
        self._set_headers()
        self.wfile.write(json.dumps(get_state()).encode())

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("access-control-allow-origin", "*")
        self.end_headers()
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        print('Starting httpd on port %d...' % port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    
# if __name__ == "__main__":
#     from sys import argv
    
#     if len(argv) == 2:
#         run(port=int(argv[1]))
#     else:
#         run()
run()