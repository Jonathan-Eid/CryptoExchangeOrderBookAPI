import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import orderbook
import websocketClients
import jsonout
import threading
from queue import Queue

updateQ = Queue()

gdax = websocketClients.GDAXClient()
bit = websocketClients.BitFenixClient()

def databateInit():
    gdax.connect()
    bit.connect()
    orders1 = bit.retrieveOrderBook("BTC-USD")
    orders = gdax.retrieveOrderBook("BTC-USD")
    orderbook.addOrders(orders1)
    orderbook.addOrders(orders)

class PriceGreaterThanHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def initialize(self):
        self.set_header("Content-Type", "application/json")
    def get(self):
        self.write("This is your response")
        self.finish()
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        try:
            write_data = jsonout.priceRequestsToJson(orderbook.ordersGreaterThan(data["greater"]))
            self.write(write_data)
        except KeyError:
            self.write(json.dumps({"error": "invalidRequest"}).encode())
        self.finish()

class ExchangeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def initialize(self):
        self.set_header("Content-Type", "application/json")
    def get(self):
        self.write("Exchange")
        self.finish()
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        try:
            write_data = jsonout.exchangeRequestsToJson(orderbook.ordersFromExchange(data["exchange"]))
            self.write(write_data)
        except KeyError:
            self.write(json.dumps({"error": "invalidRequest"}).encode())
        self.finish()

"""class PairnameHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def initialize(self):
        self.set_header("Content-Type", "application/json")
    def get(self):
        self.write("Pairs")
        self.finish()
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        try:
            #pairorder = gdax.retrieveOrderBook(data["pairname"])
            #orderbook.addOrders(pairorder)
            pairorder = bit.retrieveOrderBook(data["pairname"])
            orderbook.addOrders(pairorder)

            write_data = jsonout.pairnameRequestsToJson(orderbook.ordersFromPairname(data["pairname"]))
            self.write(write_data)
        except KeyError:
            self.write(json.dumps({"error": "invalidRequest"}).encode())
        self.finish()"""

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.write_message(jsonout.ordersToJson(orderbook.snapshotOrders()))
        print("Websocket opened")

    def on_message(self, message):
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print("Client received a message : %s" % ( message))
        self.write_message("you sent a message")

    def on_close(self):
        print("websocket opened")


app = tornado.web.Application([
    (r'/price_greater_than', PriceGreaterThanHandler),
    (r'/exchange', ExchangeHandler),
    (r'/websocket', WebSocketHandler),
])

if __name__ == '__main__':
    databateInit()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

