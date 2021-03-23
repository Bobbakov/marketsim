from flask import Flask, request, render_template, jsonify
from functions import update_orderbook
app = Flask(__name__)

# Initialize view counter
counter = 1

# Initialize orderbook
orderbook = {"B": {},
             "A": {}}

# Page counter
@app.route('/counter', methods=['GET'])
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
        # Send order to orderbook
        content = request.get_json(force=True)
        print("Incoming order = {}".format(content))
        print("Orderbook before update = {}".format(orderbook))
        orderbook = update_orderbook(content, orderbook)
        print("Orderbook after update = {}".format(orderbook))
        print("Test")
        return orderbook
    if request.method == 'GET':
        # Get orderbook
        return orderbook

if __name__ == "__main__":
    app.run(debug=True)