import time


class LimitOrder(object):
    def __init__(self, is_buy, qty, price):
        self.order_id = str(time.time())
        self.is_buy = is_buy
        self.qty = qty
        self.price = price



