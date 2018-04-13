class ExchangeOrder:
    def __init__(self):
        self.pairname = None
        self.type = None
        self.price = None
        self.quantity = None
        self.exchange = None

def createGDAXOrdersfromSnapshot(snapshot):
    orders = []
    tickers = snapshot['product_id']
    for order in snapshot["bids"]:
        gdaxOrder = ExchangeOrder()
        gdaxOrder.pairname = tickers
        gdaxOrder.type = "Bid"
        gdaxOrder.price = float(order[0])
        gdaxOrder.quantity = float(order[1])
        gdaxOrder.exchange = "GDAX"

        orders.append(gdaxOrder)

    for order in snapshot["asks"]:
        gdaxOrder = ExchangeOrder()
        gdaxOrder.pairname = tickers
        gdaxOrder.type = "Ask"
        gdaxOrder.price = float(order[0])
        gdaxOrder.quantity = float(order[1])
        gdaxOrder.exchange = "GDAX"

        orders.append(gdaxOrder)

    return orders


def createGDAXOrderfromUpdate(update):
    tickers = update["product_id"]

    update = update["changes"][0]

    order = ExchangeOrder()
    order.pairname = tickers

    if update[0] == "buy":
        order.type = "Bid"
    else:
        order.type = "Ask"
    order.price = float(update[1])
    order.quantity = float(update[2])
    order.exchange = "GDAX"
    return order

def createBitFinexOrderfromSnapshot(snapshot,tickers):
    orders=[]
    for order in snapshot[0][1]:
        bitfinexOrder = ExchangeOrder()
        bitfinexOrder.pairname = tickers
        bitfinexOrder.price = order[0]
        if order[2] < 0:
            bitfinexOrder.type = "Ask"
            bitfinexOrder.quantity = order[2] * -1
        else:
            bitfinexOrder.type = "Bid"
            bitfinexOrder.quantity = order[2]
        bitfinexOrder.exchange = "BitFenix"

        orders.append(bitfinexOrder)
    return orders

def createBitFinexOrderfromUpdate(update,tickers):
    order = ExchangeOrder()
    order.pairname = tickers
    if update[0][1][0] < 0:
        order.price = update[0][1][0] * -1
        order.type = "Ask"
    else:
        order.price = update[0][1][0]
        order.type = "Bid"
    order.quantity = update[0][1][2]
    order.exchange = "BitFenix"
    return order

