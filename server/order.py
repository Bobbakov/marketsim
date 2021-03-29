import itertools
from datetime import datetime, timedelta
import operator

from .transaction import transaction


class order(object):
    counter = itertools.count()
    datetimeCounter = datetime(2019, 1, 1, 9, 0, 0)
    history = []
    activeOrders = []
    activeBuyOrders = []
    activeSellOrders = []
    historyIntialOrder = {}

    # Initialize order
    def __init__(self, side, price, quantity):
        self.id = next(order.counter)
        order.datetimeCounter += timedelta(seconds=1)
        self.datetime = order.datetimeCounter
        self.side = side
        price = float("%.2f" % (price))
        self.price = price
        self.quantity = quantity

        # Add order to order history
        order.history.append(self)

        # Add hardcoded values to dictionaries (If you add self --> values get overwritten)
        order.historyIntialOrder[self.id] = {"id": self.id,
                                             "side": side,
                                             "price": price,
                                             "quantity": quantity}

        # Check if order results in transaction
        # If order is buy order
        if self.side == "Buy":
            # start loop
            remainingQuantity = self.quantity
            while True:
                # If there are active sell orders --> continue
                if not not order.activeSellOrders:
                    sellOrders = sorted(order.activeSellOrders, key=operator.attrgetter("price"))
                    bestOffer = sellOrders[0]

                    # If limit price buy order >= price best offer --> transaction
                    if self.price >= bestOffer.price:
                        transactionPrice = bestOffer.price

                        # If quantity buy order larger quantity than best offer --> remove best offer from active orders
                        if remainingQuantity > bestOffer.quantity:
                            transactionQuantity = bestOffer.quantity

                            # Register transaction
                            # transaction(self, bestOffer, transactionPrice, transactionQuantity)

                            # Remove offer from orderbook
                            order.removeOffer(bestOffer)

                            # Reduce remaining quantity order
                            remainingQuantity -= transactionQuantity

                        # If quantity buy order equals quantity best offer
                        elif remainingQuantity == bestOffer.quantity:
                            transactionQuantity = bestOffer.quantity

                            # Register transaction
                            # transaction(self, bestOffer, market, transactionPrice, transactionQuantity)

                            # Remove offer from orderbook
                            order.removeOffer(bestOffer)

                            # Buy order is executed --> break loop
                            break

                        # if quantity buy order is small than quantity best offer --> reduce quantity best offer
                        else:
                            transactionQuantity = remainingQuantity

                            # Register transaction
                            # transaction(self, bestOffer, market, transactionPrice, transactionQuantity)

                            # Reduce quantity offer
                            order.reduceOffer(bestOffer, transactionQuantity)

                            # Buy order is executed --> break loop
                            break

                    # If bid price < best offer --> no transaction
                    else:
                        self.quantity = remainingQuantity
                        # Send order to orderbook
                        order.activeOrders.append(self)
                        order.activeBuyOrders.append(self)
                        break

                # If there are NO active sell orders --> add order to active orders
                else:
                    self.quantity = remainingQuantity
                    order.activeOrders.append(self)
                    order.activeBuyOrders.append(self)
                    break

        # If order is sell order
        else:
            # start loop
            remainingQuantity = self.quantity
            while True:
                # if there are active buy orders --> continue
                if not not order.activeBuyOrders:
                    buyOrders = sorted(order.activeBuyOrders,
                                       key=operator.attrgetter("price"),
                                       reverse=True)
                    bestBid = buyOrders[0]

                    # If price sell order <= price best bid --> transaction
                    if bestBid.price >= self.price:
                        transactionPrice = bestBid.price

                        # If quantity offer larger than quantity best bid
                        if remainingQuantity > bestBid.quantity:
                            transactionQuantity = bestBid.quantity

                            # Register transaction
                            # transaction(bestBid, self, market, transactionPrice, transactionQuantity)

                            # Remove bid from orderbook
                            order.removeBid(bestBid)

                            remainingQuantity -= transactionQuantity
                        # If quantity order equals quantity best offer
                        elif remainingQuantity == bestBid.quantity:
                            transactionQuantity = bestBid.quantity

                            # Register transaction
                            # transaction(bestBid, self, market, transactionPrice, transactionQuantity)

                            # Remove best bid from orderbook
                            order.removeBid(bestBid)

                            # Order is executed --> break loop
                            break

                            # If quantity sell order is smaller than quantity best bid
                        else:
                            transactionQuantity = remainingQuantity

                            # Register transaction
                            # transaction(bestBid, self, market, transactionPrice, transactionQuantity)

                            # Reduce quantity best bid
                            order.reduceBid(bestBid, transactionQuantity)
                            break

                    # If best offer price > best bid price --> no transaction
                    else:
                        self.quantity = remainingQuantity
                        order.activeOrders.append(self)
                        order.activeSellOrders.append(self)
                        break

                # If there are no active buy orders --> add order to active orders
                else:
                    self.quantity = remainingQuantity
                    order.activeOrders.append(self)
                    order.activeSellOrders.append(self)
                    break

    ### METHODS
    def __str__(self):
        return "{} \t {} \t {} \t {} \t {}".format(self.market, self.agent.name, self.side, self.price, self.quantity)

    # Remove offer from orderbook
    def removeOffer(offer):
        a = order.activeSellOrders
        for c, o in enumerate(a):
            if o.id == offer.id:
                del a[c]
                break

    # Reduce quantity offer in orderbook
    def reduceOffer(offer, transactionQuantity):
        a = order.activeSellOrders
        for c, o in enumerate(a):
            if o.id == offer.id:
                if a[c].quantity == transactionQuantity:
                    order.removeOffer(offer, market)
                else:
                    a[c].quantity -= transactionQuantity
                break

    # Remove bid from orderbook
    def removeBid(bid):
        a = order.activeBuyOrders
        for c, o in enumerate(a):
            if o.id == bid.id:
                del a[c]
                break

                # Reduce quantity bid in orderbook

    def reduceBid(bid, transactionQuantity):
        a = order.activeBuyOrders
        for c, o in enumerate(a):
            if o.id == bid.id:
                if a[c].quantity == transactionQuantity:
                    order.removeBid(bid, market)
                else:
                    a[c].quantity -= transactionQuantity
                break