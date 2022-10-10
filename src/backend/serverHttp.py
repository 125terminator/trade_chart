from calendar import month
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import datetime
import json
import pandas as pd
import os

from OHLC import OHLC
from utils import *

historical = None
db = None


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)

        # print(self.path)
        if self.path == "/api/trades":
            return self.tradesHandler()
        if self.path == "/api/holdings":
            return self.holdingsHandler()
        if self.path == '/api/state':
            return self.stateHandler()
        if '/api/stock' in self.path:
            self.getStockHandler(params=params)
        if "/api/analysis" in self.path:
            return self.analysisHandler(params=params)

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        if self.path == "/api/buy":
            self.buyStockHandler(post_body)
        if self.path == "/api/sell":
            self.sellStockHandler(post_body)

    def tradesHandler(self):
        self._set_headers()
        self.wfile.write(json.dumps(db['user'].trades).encode())

    def analysisHandler(self, params):
        symbol = params['stock'][0]
        ohlc = historical.get(symbol)
        if ohlc is None:
            return

        endTime = datetime.datetime.fromtimestamp(
            int(params['endTime'][0])/1000.0)
        startTime = endTime - datetime.timedelta(days=60)

        # print(startTime, endTime)
        interval = int(params['interval'][0])//6000  # convert ms to seconds
        df = ohlc.toInterval(interval)

        df = between_time(df, startTime, endTime)[-1000:]
        df = df[::-1]
        close_open = get_change(df.Close, df.Open).round(2)
        high_low = get_change(df.High, df.Low).round(2)
        high_open = get_change(df.High, df.Open).round(2)
        low_open = get_change(df.Low, df.Open).round(2)
        volume = (df.Volume/10000000).round(2)
        data = pd.DataFrame({'high_low': high_low.values, 'close_open': close_open, 'high_open': high_open,
                            'low_open': low_open, 'volume': volume}, index=close_open.index).to_json(orient='table')

        data = json.loads(data)
        self._set_headers()
        # self.wfile.write(json.dumps(json.load(open('../../data/sbin-08-22.json', 'r'))).encode())
        self.wfile.write(json.dumps(data).encode())

    def buyStockHandler(self, body):
        self._set_headers()
        db['user'].buy(body)
        # print(json.dumps(db['user'].transactions, indent=4))

    def sellStockHandler(self, body):
        self._set_headers()
        db['user'].sell(body)
        # print(json.dumps(db['user'].transactions, indent=4))

    def getStockHandler(self, params):
        symbol = params['stock'][0]
        ohlc = historical.get(symbol)
        if ohlc is None:
            return

        endTime = datetime.datetime.fromtimestamp(
            int(params['endTime'][0])/1000.0)
        startTime = endTime - datetime.timedelta(days=5)

        # print(startTime, endTime)
        interval = int(params['interval'][0])//6000  # convert ms to seconds
        data = ohlc.toInterval(interval)
        data = between_time(data, startTime, endTime).to_json(orient='table')
        data = json.loads(data)
        self._set_headers()
        # self.wfile.write(json.dumps(json.load(open('../../data/sbin-08-22.json', 'r'))).encode())
        self.wfile.write(json.dumps(data).encode())

    def stateHandler(self):
        self._set_headers()
        self.wfile.write(json.dumps(db['date'].get()).encode())

    def holdingsHandler(self):
        self._set_headers()
        self.wfile.write(json.dumps(db['user'].holdings).encode())

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("access-control-allow-origin", "*")
        self.end_headers()


def run(_historical, _db, server_class=HTTPServer, handler_class=Server, port=8008):
    global historical, db
    historical = _historical
    db = _db
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        print('Starting httpd on port %d...' % port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
