import ccxt
import pandas as pd 
import pprint

binance_api = ${{ screts.BINANCE_API }}
binance_secret = ${{ screts.BINANCE_SECRET }}

binance = ccxt.binance(config={'apiKey': binance_api, 'secret': binance_secret, 'enableRateLimit': True, 'options': { 'defaultType': 'future' } })

balance = binance.fetch_balance() 
positions = balance['info']['positions']
for position in positions: 
  if position["symbol"] == "MATICUSDT": 
    pprint.pprint(position)
    binance_matic = position['positionAmt']
    binance_matic = float(binance_matic)

usdc_long = 66896.922644
usdc_rent = 22351.776189
matic_long = 100957.149571
matic_rent = 102043.221440
previous_price = (usdc_long*matic_long)/((matic_rent-binance_matic)**2)
volatility_range = 2.5
print(previous_price)

matic = binance.fetch_ticker("MATIC/USDT")
matic_price = matic['last']
print(matic_price)

if abs(((matic_price - previous_price)/previous_price)*100) > volatility_range:
  sks = ((((usdc_long*matic_long)**(1/2))*2*(matic_price**(1/2)))/2)/matic_price
  difference = matic_rent - sks
  required_change = difference - binance_matic

  if required_change > 0:
    print('order = binance.create_market_buy_order(symbol="MATIC/USDT", amount= required_change)')
    print(required_change)
  else:
    required_change = required_change*-1 
    print('order = binance.create_market_sell_order(symbol="MATIC/USDT", amount= required_change)')
    print(required_change)
else:
  pass
