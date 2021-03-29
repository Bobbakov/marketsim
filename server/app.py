# Import libraries
from flask import Flask, request, jsonify
from server.market import Market

# Initialize app
app = Flask(__name__)

# Initialize variables
counter = 1
market = Market()  # keep global order book in memory


# POSTS
@app.route('/submit_order', methods=['POST'])
def submit_order():
    global order_book
    # Process incoming order from client
    json_order = request.get_json(force=True)
    return handle_order_request(json_order, order_book)


# GETS
@app.route('/orderbook', methods=['GET'])
def return_order_book():
    global order_book
    # return order book to client
    print('GET Request made...')
    print(f'Return order book: {order_book.get_json_order_book()}')
    print('Raw Asks:', order_book.asks)
    print('Raw Bids:', order_book.bids)
    return order_book.get_json_order_book()


# Run application
if __name__ == "__main__":
    app.run(debug=True)