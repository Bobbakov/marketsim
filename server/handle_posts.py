def handle_order_request(json_order, order_book):
    print("Incoming order = {}".format(json_order))
    print("Order book before update = {}".format(order_book))
    if json_order['side'] == 'B':
        order_book.add_bid_order(json_order)
    elif json_order['side'] == 'A':
        order_book.add_ask_order(json_order)
    print("Order book after update = {}".format(order_book.get_json_order_book()))
    return order_book.get_json_order_book()