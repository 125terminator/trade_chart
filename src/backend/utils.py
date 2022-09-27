import json
import numpy as np

statePath = '../../data/date.json'
def get_state():
    return json.load(open(statePath, 'r'))

def push_state(state):
    a = json.dumps(state)
    f = open(statePath, 'w')
    f.write(a)
    f.close()

def between_time(df, start, end):
    return df[(df.index >= start) & (df.index <= end)]

def greater_equal_index(df, start):
    # TODO: use binary search of pandas for faster access
    a = np.argmax(df.index >= start)
    return a

class Stock:
    def __init__(self, price=0, qty=0, sold=False, intraday=False):
        self.price = price
        self.qty = qty
        self.sold = sold
        self.intraday = intraday
    
    def square_off(self, stock):
        min_qty = min(self.qty, stock.qty)
        pAndL = abs(stock.price - self.price) * min_qty
        self.qty -= min_qty
        stock.qty -= min_qty
        return pAndL

    def avg(self, stock):
        qty = self.qty + stock.qty
        avg_price = (self.price * self.qty + stock.price * stock.qty) / (qty if qty > 0 else 1) # This is to stop from division by 0
        self.price = avg_price
        self.qty = qty
    
    def txn(self):
        if self.qty <= 0:
            return None
        
        col = ['Instrument', 'Qty.', 'Avg.', 'Cur. val', 'P&L', 'Net chg.']
        qty = -self.qty if self.sold else self.qty
        instrument = 's1-i' if self.intraday else 's1'
        return {col[0]: instrument, col[1]: qty, col[2]: round(self.price, 2), col[3]: self.price, col[4]: 0, col[5]: "0%"}
        

    def __str__(self) -> str:
        return str({'price':self.price, 'qty':self.qty})

    def __repr__(self) -> str:
        return str({'price':self.price, 'qty':self.qty})