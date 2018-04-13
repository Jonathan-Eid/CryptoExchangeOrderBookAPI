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
    bidStop = 0
    for order in snapshot["bids"]:
        if bidStop is 25:
            break
        gdaxOrder = ExchangeOrder()
        gdaxOrder.pairname = tickers
        gdaxOrder.type = "Bid"
        gdaxOrder.price = float(order[0])
        gdaxOrder.quantity = float(order[1])
        gdaxOrder.exchange = "GDAX"

        orders.append(gdaxOrder)

        bidStop += 1


    askStop = 0
    for order in snapshot["asks"]:
        if askStop is 25:
            break
        gdaxOrder = ExchangeOrder()
        gdaxOrder.pairname = tickers
        gdaxOrder.type = "Ask"
        gdaxOrder.price = float(order[0])
        gdaxOrder.quantity = float(order[1])
        gdaxOrder.exchange = "GDAX"

        orders.append(gdaxOrder)

        askStop += 1

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
    for order in snapshot[1]:
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
    if update[1][2] < 0:
        order.quantity = update[1][2] * -1
        order.type = "Ask"
    else:
        order.quantity = update[1][2]
        order.type = "Bid"

    order.price = update[1][0]
    order.exchange = "BitFenix"
    return order


