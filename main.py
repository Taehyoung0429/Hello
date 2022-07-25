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

usdc_long = 12792.697207
usdc_rent = 4255.912278
matic_long = 15377.520332
matic_rent = 15407.553880
previous_price = (usdc_long*matic_long)/((matic_rent-binance_matic)**2)
volatility_range = 3.75
text = "Previous Matic price was " + str(previous_price)
bot.sendMessage(chat_id = 1489495601, text=text)

matic = binance.fetch_ticker("MATIC/USDT")
matic_price = matic['last']
text = "Current Matic price is " + str(matic_price)
bot.sendMessage(chat_id = 1489495601, text=text)

if abs(((matic_price - previous_price)/previous_price)*100) > volatility_range:
  sks = ((((usdc_long*matic_long)**(1/2))*2*(matic_price**(1/2)))/2)/matic_price
  difference = matic_rent - sks
  required_change = difference - binance_matic

  if required_change > 0:
    order = binance.create_market_buy_order(symbol="MATIC/USDT", amount= required_change)
    print('order = binance.create_market_buy_order(symbol="MATIC/USDT", amount= required_change)')
    text = 'binance.create_market_buy_order(symbol="MATIC/USDT", amount= ' + str(required_change) + ')'
    bot.sendMessage(chat_id = 1489495601, text=text)
  else:
    required_change = required_change*-1 
    order = binance.create_market_sell_order(symbol="MATIC/USDT", amount= required_change)
    print('order = binance.create_market_sell_order(symbol="MATIC/USDT", amount= required_change)')
    text = 'binance.create_market_sell_order(symbol="MATIC/USDT", amount= ' + str(required_change) + ')'
    bot.sendMessage(chat_id = 1489495601, text=text)
else:
  pass

current_balance = (((usdc_long*matic_long)**(1/2))*2*(matic_price**(1/2))) + balance['USDT']['total']- usdc_rent - (matic_rent*matic_price)
text = "Your current balance is " + str(current_balance)
bot.sendMessage(chat_id = 1489495601, text=text)
