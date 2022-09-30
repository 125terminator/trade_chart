import json
import shutil
from abc import ABC, abstractmethod
from threading import Thread, Lock
from typing import final

from numpy import fromfile

from Stock import Stock
from const import *

mutex = Lock()

class DB(ABC):
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read()
        # shutil.copyfile(filename, filename + 'copy')
        
    def write(self, data):
        mutex.acquire()
        try:
            with open(self.filename, 'w') as f:
                f.write(json.dumps(data))
        finally:
            mutex.release()

    def read(self):
        mutex.acquire()
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        finally:
            mutex.release()


class Date(DB):
    def __init__(self):
        self.data = {'now': 'current date'}
        super().__init__('../../data/date.json')

    def set(self, data):
        mutex.acquire()
        try:
            self.data['now'] = data
        finally:
            mutex.release()
    
    def get(self):
        mutex.acquire()
        try:
            return self.data
        finally:
            mutex.release()

    @property
    def now(self):
        return self.get()['now']

class User(DB):
    def __init__(self, date_db):
        super().__init__('../../data/user.json')
        self.data = {'buy': [], 'sell': []}
        self.bought = {'cnc': Stock(), 'intraday': Stock(intraday=True)} 
        # cnc is not allowed for short selling
        self.sold = {'cnc': Stock(sold=True), 'intraday': Stock(sold=True, intraday=True)}
        # trades = ['buy_price', 'sell_price', 'qty', 'type', 'p&l', 'brokerage']
        self.trades = []
        self.pAndL = 0
        self.date_db = date_db

    def add_trades(self, trade):
        if trade[2] <= 0:
            return
        self.trades.append(trade)

    def buy(self, data):
        self.data['buy'].append(data)

        op = 'intraday' if data['intraday'] else 'cnc'     
        buy_stock = Stock(price=data['price'], qty=data['qty'])

        pAndL, trade = self.sold[op].square_off(buy_stock)
        self.pAndL += pAndL
        self.bought[op].avg(buy_stock)

        self.add_trades(trade)

        # if op == 'intraday':
        #     self.pAndL += self.sold[op].square_off(buy_stock)
        #     self.bought[op].avg(buy_stock)
        # elif op == 'cnc':
        #     self.bought[op].avg(buy_stock)
    
    def sell(self, data):
        self.data['sell'].append(data)

        op = 'intraday' if data['intraday'] else 'cnc'
        sell_stock = Stock(price=data['price'], qty=data['qty'])
        
        if op == 'cnc' and sell_stock.qty > self.bought[op].qty:
            return # cnc short selling not allowed
            
        pAndL, trade = self.bought[op].square_off(sell_stock)
        self.pAndL += pAndL
        self.sold[op].avg(sell_stock)


        self.add_trades(trade)
        # if op == 'intraday':
        #     self.pAndL += self.bought[op].square_off(sell_stock)
        #     self.sold[op].avg(sell_stock)
        # elif op == 'cnc':
        #     if sell_stock.qty <= self.bought[op].qty:
        #         self.pAndL += self.bought[op].square_off(sell_stock)
        #     else:
                # pass # cnc short selling not allowed

    @property
    def transactions(self):
        rt = []
        col = ['Instrument', 'Qty.', 'Avg.', 'Cur. val', 'P&L', 'Net chg.']
        for v in {self.bought['cnc'], self.bought['intraday'], self.sold['intraday']}:
            row = v.txn()
            if row is not None:
                rt.append(row)
        return rt

if __name__ == "__main__":
    o = User()
    # o.buy({"price": 2,"qty": 9,"intraday": False})
    o.buy({"price": 1,"qty": 20,"intraday": True})
    # print(o.bought)

    o.sell({"price": 2,"qty": 10,"intraday": True})
    o.sell({"price": 3,"qty": 20,"intraday": True})
    print(o.sold)
    print(o.bought)
    print(o.pAndL)
    print(o.transactions)
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.searchsorted.html