import json
from websocket import create_connection

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
    def __init__(self,url):
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
        if self.connection is not None:
            self.connection.send(json.dumps(gdaxRequest("subscribe", tickers).toJson()))
            return self.connection.recv()
            print("Connection needs to be established first!")


class BitFenixClient(Client):
    def __init__(self,url="wss://api.bitfinex.com/ws/2"):
        Client.__init__(self, url)
        self.url = url

    def retrieveOrderBook(self, tickers):
        if self.connection is not None:
            self.connection.send(json.dumps(bitfenixRequest("subscribe", tickers).toJson()))
            self.connection.recv()
            self.connection.recv()
            return self.connection.recv()
        else:
            print("Connection needs to be established first!")



