import requests, json, random, time
import numpy as np

# Link to localhost
ORDER_BOOK_ENDPOINT = "http://127.0.0.1:5000/orderbook"

# Get orderbook
'''
response = requests.get(url)    # To execute get request
print(response.status_code)     # To print http response code
print(response.text)
'''

# Update orderbook
'''
Send order in format:
    {"side": "B" or "A",
    "price": int} 
'''


class Agent(object):
    def __init__(self, order_book_endpoint, agent_id=None):
        self.agent_id = agent_id
        self.order_book_endpoint = order_book_endpoint
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
        side = random.choice(side_choices)
        price = np.random.choice(price_choices)
        data = {"side": side, "price": str(price)}
        print(f'[{self.agent_id}][ORDER] Sending order to Server for side {side} and price {price}.')
        requests.post(self.order_book_endpoint, json.dumps(data))

    def agent_trading_session(self, time_secs, update_interval):
        for i in range(0, time_secs, update_interval):
            self.update_order_book()
            self.send_random_order()
            time.sleep(update_interval)