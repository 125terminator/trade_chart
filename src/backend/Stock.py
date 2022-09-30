from broker_calc import get_net_profit

class Stock:
    def __init__(self, price=0, qty=0, sold=False, intraday=False):
        self.price = price
        self.qty = qty
        self.sold = sold
        self.intraday = intraday
    
    def trade(self, stock):
        # trades = ['buy_price', 'sell_price', 'qty', 'type', 'p&l', 'brokerage']
        qty = min(self.qty, stock.qty)
        bp = self.price if not self.sold else stock.price
        sp = self.price if self.sold else stock.price
        net_profit, brokerage = get_net_profit(bp, sp, qty)
        typ = 'Intraday' if self.intraday else 'CNC'
        print([bp, sp, qty, typ, net_profit, brokerage])
        return [bp, sp, qty, typ, net_profit, brokerage]

    def square_off(self, stock):
        min_qty = min(self.qty, stock.qty)
        pAndL = abs(stock.price - self.price) * min_qty
        self.qty -= min_qty
        stock.qty -= min_qty
        return pAndL, self.trade(stock)

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