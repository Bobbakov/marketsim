import requests, json, random, time
import numpy as np

# Link to localhost and endpoints
BASE_ENDPOINT = "http://127.0.0.1:5000/"
ORDER_BOOK_ENDPOINT = BASE_ENDPOINT + "orderbook"
SEND_ORDER_ENDPOINT = BASE_ENDPOINT + "submit_order"


class Agent(object):
    def __init__(self, agent_id=None):
        self.agent_id = agent_id

        self.order_book_endpoint = ORDER_BOOK_ENDPOINT
        self.send_order_endpoint = SEND_ORDER_ENDPOINT

        self.order_book_current_state = None
        self.order_book_history = []

    def update_order_book(self):
        print(f'[{self.agent_id}][ORDER_BOOK] requesting new order book state from server.')
        current_order_book = requests.get(self.order_book_endpoint).json()
        print(f'[{self.agent_id}][ORDER_BOOK] {current_order_book}')
        self.order_book_current_state = current_order_book
        self.order_book_history.append(current_order_book)

    def send_random_order(self):
        side_choices = ["B", "A"]
        price_choices = np.arange(1, 10)
        qty_choices = np.arange(1, 10)
        side = random.choice(side_choices)
        price = np.random.choice(price_choices)
        qty = np.random.choice(qty_choices)
        data = {"side": side, "qty": str(qty), "price": str(price)}
        print(f'[{self.agent_id}][ORDER] Sending order to Server for side {side} and price {price}.')
        requests.post(self.send_order_endpoint, json.dumps(data))

    def agent_trading_session(self, time_secs, update_interval):
        for i in range(0, time_secs, update_interval):
            self.update_order_book()
            self.send_random_order()
            time.sleep(update_interval)