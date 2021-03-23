# Import libraries
from flask import Flask, request, render_template, jsonify
from functions import update_orderbook

# Initialize app
app = Flask(__name__)

# Initialize variables
counter = 1
orderbook = {"B": {},
             "A": {}}


# Get page counter
@app.route('/', methods=['GET'])
def show_counter():
    global counter
    counter +=1
    return jsonify(page_refresh_count=counter)


# Orderbook
@app.route('/orderbook', methods=['GET', 'POST'])
def show_orderbook():
    global counter
    global orderbook
    counter +=1
    if request.method == 'POST':
        # Process incoming order
        order = request.get_json(force=True)
        print("Incoming order = {}".format(order))
        print("Orderbook before update = {}".format(orderbook))
        orderbook = update_orderbook(order, orderbook)
        print("Orderbook after update = {}".format(orderbook))
        return orderbook
    if request.method == 'GET':
        # Show orderbook
        print('GET Request made...')
        print(f'Return orderbook: {orderbook}')
        return orderbook


# Run application
if __name__ == "__main__":
    app.run(debug=True)