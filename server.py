import tornado.ioloop
import tornado.web
import tornado.websocket
import jsonpickle.pickler
import orderbook
import websocketClients

from tornado.options import define, options, parse_command_line


# we gonna store clients in dictionary..
gdax = websocketClients.GDAXClient()
gdax.connect()
bit = websocketClients.BitFenixClient()
bit.connect()
orders1 = bit.retrieveOrderBook("BTC-USD")
orders = gdax.retrieveOrderBook("BTC-USD")
orderbook.init()
orderbook.addOrders(orders1)
orderbook.addOrders(orders)

class PriceGreaterThanHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write("This is your response")
        self.finish()
    def post(self):
        self.write("catch me")
        self.finish()

class ExchangeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write("Exchange")
        self.finish()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.set_header("Content-Type", "application/json")
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
    parse_command_line()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()