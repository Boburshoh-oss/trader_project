import websocket
import rel
import json

intervall = "1h"  # example: 1s 1m 3m 5m 15m 30m 1h 1d 1w 1M

perscentage = 1  

ws_url = f"wss://stream.binance.us:9443/ws/ethusdt@kline_{intervall}"


def calculate_percentage_change(current_pirce,changed_price):
    percentage_change = ((current_pirce - changed_price) / current_pirce) * 100
    return percentage_change


def on_message(ws, message):
    # load the data from json format
    load_json = json.loads(message)
    print("name: ", load_json["s"])
    print("Interval: ", load_json["k"]["i"])
    
    current_price = load_json["k"]["o"]
    high_price = load_json["k"]["h"]
    low_price = load_json["k"]["l"]
    
    #calculate persatage of increase
    percentage_increased = calculate_percentage_change(
        float(current_price), float(high_price))
    if abs(percentage_increased) >= perscentage:
        print(
            f"ETH price has increased by {percentage_increased:.2f}% in the last 60 minutes.")
    
    # calculate persatage of deacrease
    percentage_decreased = calculate_percentage_change(
        float(current_price), float(low_price))
    if abs(percentage_decreased) >= perscentage:
        print(
            f"ETH price has decreased by {percentage_decreased:.2f}% in the last 60 minutes.")
        
    print("current price: ",current_price)
    
   
def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
