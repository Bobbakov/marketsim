import time


class Trade(object):
    def __init__(self, buyer_maker, bid_order_id, ask_order_id, price, qty):
        self.trade_time = time.time()
        self.buyer_maker = buyer_maker
        self.bid_order_id = bid_order_id
        self.ask_order_id = ask_order_id
        self.trade_id = f"{str(self.trade_time)}_{str(self.bid_order_id)}_{str(self.ask_order_id)}"
        self.price = price
        self.qty = qty
