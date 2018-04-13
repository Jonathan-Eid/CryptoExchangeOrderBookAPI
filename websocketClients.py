import json
from queue import Queue
from websocket import create_connection
import orders

class gdaxRequest:
    def __init__(self, type, tickers):
        self.type = type
        self.tickers = tickers

    def toJson(self):
        jsonStr = """
                {
                    "type": "%s",
                    "channels": [{ "name": "level2", "product_ids": ["%s"] }]
                }
                """ % (self.type, self.tickers)
        return json.loads(jsonStr)

class bitfenixRequest:
    def __init__(self, type, tickers):
        self.type = type
        self.tickers = tickers.replace("-", "")

    def toJson(self):
        jsonStr = """
                {
                    "event":"%s",
                    "channel":"book",
                    "pair":"%s"
                }
                """ % (self.type, self.tickers)
        return json.loads(jsonStr)


class Client:
    def __init__(self, url):
        self.url = url
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = create_connection(self.url)
            print("Connection successful!")
        else:
            print("Already connected!")

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Disconnected successfully!")
        else:
            print("Already disconnected!")

    def isConnected(self):
            if self.connection is not None:
                return self.connection.connected
            else:
                return False

class GDAXClient(Client):
    def __init__(self,url="wss://ws-feed.gdax.com"):
        Client.__init__(self, url)
        self.url = url

    def retrieveOrderBook(self, tickers):
        if self.isConnected():
            self.connection.send(json.dumps(gdaxRequest("subscribe", tickers).toJson()))
            return orders.createGDAXOrdersfromSnapshot(json.loads(self.connection.recv()))
        else:
            print("Connection needs to be established first!")

    def orderbookUpdates(self,queue):
        if self.isConnected():
            while self.isConnected():
                update = json.loads(self.connection.recv())
                if update["type"] == 'l2update':
                    if update["changes"][0][2] != "0":
                        update = orders.createGDAXOrderfromUpdate(update)
                        queue.put(update)

        else:
            print("Connection needs to be established first!")


class BitFenixClient(Client):
    def __init__(self,url="wss://api.bitfinex.com/ws/2"):
        Client.__init__(self, url)
        self.url = url
        self.tickers = None

    def retrieveOrderBook(self, tickers):
        if self.isConnected():
            self.tickers = tickers
            self.connection.send(json.dumps(bitfenixRequest("subscribe", tickers).toJson()))
            self.connection.recv()
            self.connection.recv()
            return orders.createBitFinexOrderfromSnapshot(json.loads(self.connection.recv()), tickers)
        else:
            print("Connection needs to be established first!")

    def orderbookUpdates(self,queue):
        if self.isConnected():
            while self.isConnected():
                update = json.loads(self.connection.recv())
                if update[1][1] is not 0:
                    update = orders.createBitFinexOrderfromUpdate(update,self.tickers)
                    queue.put(update)
        else:
            print("Connection needs to be established first!")

