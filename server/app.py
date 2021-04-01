# Import libraries
from flask import Flask, request, jsonify
from server.order import order
from server.transaction import transaction

# Initialize app
app = Flask(__name__)

# Initialize variables
counter = 1


def get_active_orders():
    asks = [[o.price, o.quantity] for o in order.activeSellOrders]
    bids = [[o.price, o.quantity] for o in order.activeBuyOrders]
    return {'Asks': asks, 'Bids': bids}


def get_trades():
    trades = transaction.historyList
    return {'Trades': trades}


# POSTS
@app.route('/submit_order', methods=['POST'])
def submit_order():
    print('POST Request made...')
    # Process incoming order from client
    json_order = request.get_json(force=True)
    side = json_order['side']
    price = float(json_order['price'])
    quantity = float(json_order['quantity'])
    order(side, price, quantity)
    print(transaction.historyList)
    return 'Posted Order.'


# GETS
@app.route('/orderbook', methods=['GET'])
def return_order_book():
    # return order book to client
    print('GET ORDERBOOK Request made...')
    return get_active_orders()


@app.route('/trades', methods=['GET'])
def return_trades():
    # return order book to client
    print('GET TRADES Request made...')
    return get_trades()


# Run application
if __name__ == "__main__":
    app.run(debug=True)