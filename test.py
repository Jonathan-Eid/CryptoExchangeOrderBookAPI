import websocketClients
import websocket
import json
import orderbook

gdax = websocketClients.GDAXClient()

gdax.connect()

snapshot = gdax.retrieveOrderBook("BTC-USD")
snapshot = json.loads(snapshot)

orderbook.addGDAXSnapshot(snapshot)

gdax.disconnect()



