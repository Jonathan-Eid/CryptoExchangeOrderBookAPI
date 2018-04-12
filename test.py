import websocketClients
import websocket

gdax = websocketClients.GDAXClient()

gdax.connect()

gdax.retrieveOrderBook("BTC-USD")


print(gdax.isConnected())

gdax.disconnect()

