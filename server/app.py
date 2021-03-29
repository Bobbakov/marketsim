# Import libraries
from flask import Flask, request, jsonify
from server.order import order

# Initialize app
app = Flask(__name__)

# Initialize variables
counter = 1


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
    return 'Posted Order.'


# GETS
@app.route('/orderbook', methods=['GET'])
def return_order_book():
    # return order book to client
    print('GET Request made...')
    return {'history': len(order.history),
            'active buy orders': len(order.activeBuyOrders),
            'active sell orders':len(order.activeSellOrders)
            }


# Run application
if __name__ == "__main__":
    app.run(debug=True)