import json
from websocket import create_connection

class GDAXClient:
    def __init__(self,ticker):
        self.ticker = ticker
        connection = None

    def connect(self):
        if self.connection is not None:
            self.connection = create_connection("wss://ws-feed.gdax.com")
            "Connection successful!"
        else:
            print("Already connected!")

    def orderbook_request(self, ticker):

        




