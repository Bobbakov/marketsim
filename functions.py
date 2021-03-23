def update_orderbook(order, orderbook):
    side = order["side"]
    price = order["price"]

    if price not in orderbook[side].keys():
        orderbook[side][price] = 1
    else:
        orderbook[side][price] += 1
    return orderbook