import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import numpy as np
import time

SEC_KEY = '6UEY5oCO2GEIn6B60yFFtEe3cm0FuauVDtxV21MC'
PUB_KEY = 'PK3GCIG4XNK6LSAUT181'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id=PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

symb = "TSLA"
pos_held = False
hours_to_test = 10

print("Checking Price")
market_data = api.get_bars(symb, TimeFrame.Minute, '2020-04-15', '2020-05-14')  # Pull market data from the past 60x minutes

close_list = []
print(market_data)
for bar in market_data:
    close_list.append(bar.c)
print(close_list)
print("Open: " + str(close_list[0]))
print("Close: " + str(close_list[60 * hours_to_test - 1]))

close_list = np.array(close_list, dtype=np.float64)
startBal = 2000  # Start out with 2000 dollars
balance = startBal
buys = 0
sells = 0

for i in range(4, 60 * hours_to_test):  # Start four minutes in, so that MA can be calculated
    ma = np.mean(close_list[i - 4:i + 1])
    last_price = close_list[i]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.1 < last_price and not pos_held:
        print("Buy")
        balance -= last_price
        pos_held = True
        buys += 1
    elif ma - 1 > last_price and pos_held:
        print("Sell")
        balance += last_price
        pos_held = False
        sells += 1
    print(balance)
    time.sleep(0.01)

print("")
print("Buys: " + str(buys))
print("Sells: " + str(sells))

if buys > sells:
    balance += close_list[60 * hours_to_test - 1]  # Add back your equity to your balance

print("Final Balance: " + str(balance))

print("Profit if held: " + str(close_list[60 * hours_to_test - 1] - close_list[0]))
print("Profit from algorithm: " + str(balance - startBal))

