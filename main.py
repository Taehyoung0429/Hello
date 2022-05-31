import ccxt
import pandas as pd 
import pprint
import sys
import telegram

if __name__ == '__main__':
  binance_api = sys.argv[1]
  binance_secret = sys.argv[2]
  chat_token = sys.argv[3]

bot = telegram.Bot(token = chat_token)
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
text = print(previous_price)
bot.sendMessage(chat_id = 1489495601, text=text)

matic = binance.fetch_ticker("MATIC/USDT")
matic_price = matic['last']
text = print(matic_price)
bot.sendMessage(chat_id = 1489495601, text=text)

if abs(((matic_price - previous_price)/previous_price)*100) > volatility_range:
  sks = ((((usdc_long*matic_long)**(1/2))*2*(matic_price**(1/2)))/2)/matic_price
  difference = matic_rent - sks
  required_change = difference - binance_matic

  if required_change > 0:
    order = binance.create_market_buy_order(symbol="MATIC/USDT", amount= required_change)
    text = print('order = binance.create_market_buy_order(symbol="MATIC/USDT", amount= required_change)')
    bot.sendMessage(chat_id = 1489495601, text=text)
  else:
    required_change = required_change*-1 
    order = binance.create_market_sell_order(symbol="MATIC/USDT", amount= required_change)
    text = print('order = binance.create_market_sell_order(symbol="MATIC/USDT", amount= required_change)')
    bot.sendMessage(chat_id = 1489495601, text=text)
else:
  pass

current balance = (((usdc_long*matic_long)**(1/2))*2*(matic_price**(1/2))) + balance['USDT']['total']
text = current balance
bot.sendMessage(chat_id = 1489495601, text=text)
