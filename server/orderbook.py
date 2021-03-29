from server.orders import LimitOrder
from server.trades import Trade


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
        self.orders = []
        self.trades = []
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

    def bid_can_trade(self, order):
        bid_price = order.price
        min_ask_price = min(list(self.asks))
        if bid_price >= min_ask_price:
            return True
        else:
            return False

    def ask_can_trade(self, order):
        ask_price = order.price
        max_bid_price = max(list(self.bids))
        if ask_price <= max_bid_price:
            return True
        else:
            return False

    def match_bid_order(self, new_order):
        new_trades = []
        bid_price = new_order.price
        bid_qty = new_order.qty
        bid_id = new_order.order_id
        current_ask_prices = list(self.asks)
        current_ask_prices.sort()
        for ask_price in current_ask_prices:
            if bid_price >= ask_price:
                ask_qty_at_price = sum([o.qty for o in self.asks[ask_price]])
                if ask_qty_at_price >= bid_qty:
                    # 1) bid can be filled at current price level
                    for i, ask in enumerate(self.asks[ask_price]):
                        ask_qty = ask.qty
                        if ask_qty == bid_qty:
                            # 1.1) both ask and bid get fully filled
                            trade = Trade(True, bid_id, ask.order_id, bid_qty, bid_price)
                            del self.asks[ask_price][i]
                            self.trades.append(trade)
                            bid_qty -= ask_qty
                        elif ask_qty >= bid_qty:
                            # 1.2) ask order get partially filled and bid fully
                            bid_qty -= ask_qty
                            ask_remainder_qty = ask_qty - bid_qty
                            self.asks[ask_price][i] = LimitOrder(ask.is_buy, ask_remainder_qty, ask.price)
                        elif ask_qty < bid_qty:
                            # 1.3) ask order gets fully filled and bid partially
                            pass
                    return True
                elif bid_qty > ask_qty_at_price:
                    # 2) bid can be partially filled at current price level
                    pass

    def add_bid_order(self, json_order):
        order = json_to_limit_order(json_order)
        price_str = order.price
        if price_str in self.bids:
            self.bids[price_str].append(order)
        else:
            self.bids[price_str] = [order]
        self.orders.append(order)

    def remove_bid_order(self, order):
        order_price = order.price
        order_id = order.order_id
        for i, o in enumerate(self.bids[order_price]):
            if o.order_id == order_id:
                del self.bids[order_price][i]
                break

    def add_ask_order(self, json_order):
        order = json_to_limit_order(json_order)
        price_str = order.price
        if price_str in self.asks:
            self.asks[price_str].append(order)
        else:
            self.asks[price_str] = [order]
        self.orders.append(order)

    def remove_ask_order(self, order):
        order_price = order.price
        order_id = order.order_id
        for i, o in enumerate(self.asks[order_price]):
            if o.order_id == order_id:
                del self.asks[order_price][i]
                break


