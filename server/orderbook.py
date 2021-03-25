from server.orders import LimitOrder


def check_tick_size(price, tick_size):
    if '.' in str(price):
        return len(str(price).split('.')[1]) <= tick_size
    else:
        return True


def json_to_limit_order(json_order):
    is_buy = True if json_order['side'] == 'B' else False
    price = float(json_order['price'])
    qty = float(json_order['qty'])
    order = LimitOrder(is_buy, qty, price)
    return order


class OrderBook(object):
    def __init__(self, tick_size=5):
        self.bids = {}
        self.asks = {}
        self.tick_size = tick_size

    def get_json_order_book(self):
        order_book = {"B": [], "A": []}
        for price in self.bids:
            total_qty = 0
            for o in self.bids[price]:
                total_qty += o.qty
            order_book['B'].append([float(price), total_qty])
        for price in self.asks:
            total_qty = 0
            for o in self.asks[price]:
                total_qty += o.qty
            order_book['A'].append([float(price), total_qty])
        return order_book

    def add_bid_order(self, json_order):
        order = json_to_limit_order(json_order)
        price_str = str(order.price)
        if price_str in self.bids:
            self.bids[price_str].append(order)
        else:
            self.bids[price_str] = [order]

    def remove_bid_order(self, order):
        order_price = str(order.price)
        order_id = order.order_id
        for i, o in enumerate(self.bids[order_price]):
            if o.order_id == order_id:
                del self.bids[order_price][i]
                break

    def add_ask_order(self, json_order):
        order = json_to_limit_order(json_order)
        price_str = str(order.price)
        if price_str in self.asks:
            self.asks[price_str].append(order)
        else:
            self.asks[price_str] = [order]

    def remove_ask_order(self, order):
        order_price = str(order.price)
        order_id = order.order_id
        for i, o in enumerate(self.asks[order_price]):
            if o.order_id == order_id:
                del self.asks[order_price][i]
                break


