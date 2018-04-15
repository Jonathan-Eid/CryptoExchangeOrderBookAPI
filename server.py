from tornado.ioloop import IOLoop
from datetime import timedelta
import tornado.web
import tornado.websocket
import json
import orderbook
from orderbook import Session
import websocketClients
import jsonout
import threading






def databaseInit():
    gdax = websocketClients.GDAXClient()
    bit = websocketClients.BitFenixClient()
    gdax.connect()
    bit.connect()
    bit.retrieveOrderBook("BTC-USD")
    gdax.retrieveOrderBook("ETH-USD")


def dataErase():
    orderbook.clear_data()

class SnapshotHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def initialize(self):
        self.set_header("Content-Type", "application/json")
    def get(self):
        self.write(jsonout.ordersToJson(orderbook.snapshotOrders()))
        self.finish()
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        try:
            if data["request"] == "greater":
                write_data = jsonout.priceRequestsToJson(orderbook.ordersGreaterThan(data["number"]))
                self.write(write_data)
            if data["request"] == "exchange":
                write_data = jsonout.exchangeRequestsToJson(orderbook.ordersFromExchange(data["name"]))
                self.write(write_data)
            if data["request"] == "pairname":
                write_data = jsonout.pairnameRequestsToJson(orderbook.ordersFromPairname(data["tickers"]))
                self.write(write_data)
        except KeyError:
            self.write(json.dumps({"error": "invalidRequest"}).encode())
        self.finish()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print("Websocket opened")
        self.add_header("Content-Type", "application/json")
        self.write_message(jsonout.ordersToJson(orderbook.snapshotOrders()))
        self.schedule_update()

    def schedule_update(self):
        self.timeout = IOLoop.instance().add_timeout(timedelta(seconds=1),
                                                         self.update_client)

    def update_client(self):
        try:
            self.write_message(jsonout.ordersToJson([orderbook.updateQ.get()]))
        finally:
            self.schedule_update()

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
    (r'/snapshot', SnapshotHandler),
    (r'/websocket', WebSocketHandler),
])

if __name__ == '__main__':
    databaseInit()
    app.listen(8888)
    IOLoop.instance().start()

