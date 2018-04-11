from websocket import create_connection
import json
import orderbook



connection = create_connection("wss://api.bitfinex.com/ws/2")


connection.send(json.dumps({
   "event":"subscribe",
   "channel":"book",
   "pair":"BTCUSD",

}))
print(connection.recv())

while connection.connected:
    print(connection.recv())
