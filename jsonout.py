import jsonpickle.pickler

class OrdersForJson:
    def __init__(self):
        self.orders = []
        self.instance = None

    def append(self,order,instance):
        self.instance = instance
        self.orders.append((order.pairname, order.type, order.price, order.quantity, order.exchange))


def ordersToJson(orders):
    orderForJson = OrdersForJson()
    for o in orders:
        orderForJson.append(o,o.instance)

    return jsonpickle.encode(orderForJson, unpicklable=False)



def priceRequestsToJson(orders):
    orderForJson = OrdersForJson()
    for o in orders:
        orderForJson.append(o, "greater")

    return jsonpickle.encode(orderForJson, unpicklable=False)

def exchangeRequestsToJson(orders):
    orderForJson = OrdersForJson()
    for o in orders:
        orderForJson.append(o, "exchange")

    return jsonpickle.encode(orderForJson, unpicklable=False)

def pairnameRequestsToJson(orders):
    orderForJson = OrdersForJson()
    for o in orders:
        orderForJson.append(o, "pairname")

    return jsonpickle.encode(orderForJson, unpicklable=False)