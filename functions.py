def update_orderbook(content, orderbook):
    side = content["side"]
    price = content["price"]

    if price not in orderbook[side].keys():
        orderbook[side][price] = 1
    else:
        orderbook[side][price] += 1
    return orderbook

