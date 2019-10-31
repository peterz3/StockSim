import re
import json
import sqlite3
from worldtradingdata import WorldTradingData

# NOTE: This is currently only inserting 95 stocks into the database

if __name__ == "__main__":
	
	# First, retrieve all stock symbols as a list of symbol batches of 5
	filepath = 'nasdaq100list.txt'
	pattern = re.compile('\S*')
	with open(filepath) as file:
		symbol_batches = []
		curr_symbol_batch = []
		for i, line in enumerate(file):
			# split symbol list into lists of size 5 for API request
			if (i % 5 == 0) and i != 0 and i != 100:
				symbol_batches.append(curr_symbol_batch)
				curr_symbol_batch = []

			# find the symbol on the current line
			match = pattern.match(line)
			if match:
				curr_symbol_batch.append(match.group(0))

	# Testing data:
	# dict_response = {'symbols_requested': 5, 'symbols_returned': 5, 'data': [{'symbol': 'ADBE', 'name': 'Adobe Inc.', 'currency': 'USD', 'price': '278.41', 'price_open': '273.25', 'day_high': '278.64', 'day_low': '272.61', '52_week_high': '313.11', '52_week_low': '204.95', 'day_change': '6.96', 'change_pct': '2.56', 'close_yesterday': '271.45', 'market_cap': '134772441088', 'volume': '2075526', 'volume_avg': '2653700', 'shares': '484079008', 'stock_exchange_long': 'NASDAQ Stock Exchange', 'stock_exchange_short': 'NASDAQ', 'timezone': 'EDT', 'timezone_name': 'America/New_York', 'gmt_offset': '-14400', 'last_trade_time': '2019-10-30 16:00:01', 'pe': '49.54', 'eps': '5.62'}, {'symbol': 'ALGN', 'name': 'Align Technology, Inc.', 'currency': 'USD', 'price': '252.71', 'price_open': '255.65', 'day_high': '255.65', 'day_low': '247.54', '52_week_high': '334.64', '52_week_low': '169.84', 'day_change': '-3.41', 'change_pct': '-1.33', 'close_yesterday': '256.12', 'market_cap': '20184174592', 'volume': '754894', 'volume_avg': '1603285', 'shares': '79870896', 'stock_exchange_long': 'NASDAQ Stock Exchange', 'stock_exchange_short': 'NASDAQ', 'timezone': 'EDT', 'timezone_name': 'America/New_York', 'gmt_offset': '-14400', 'last_trade_time': '2019-10-30 16:00:01', 'pe': '48.51', 'eps': '5.21'}, {'symbol': 'ALXN', 'name': 'Alexion Pharmaceuticals, Inc.', 'currency': 'USD', 'price': '106.25', 'price_open': '107.49', 'day_high': '107.73', 'day_low': '104.96', '52_week_high': '141.86', '52_week_low': '92.56', 'day_change': '-1.24', 'change_pct': '-1.15', 'close_yesterday': '107.49', 'market_cap': '23512170496', 'volume': '1025023', 'volume_avg': '2154042', 'shares': '224227008', 'stock_exchange_long': 'NASDAQ Stock Exchange', 'stock_exchange_short': 'NASDAQ', 'timezone': 'EDT', 'timezone_name': 'America/New_York', 'gmt_offset': '-14400', 'last_trade_time': '2019-10-30 16:00:01', 'pe': '16.29', 'eps': '6.52'}, {'symbol': 'AMD', 'name': 'Advanced Micro Devices, Inc.', 'currency': 'USD', 'price': '33.13', 'price_open': '32.93', 'day_high': '33.34', 'day_low': '32.04', '52_week_high': '35.55', '52_week_low': '16.03', 'day_change': '0.10', 'change_pct': '0.30', 'close_yesterday': '33.03', 'market_cap': '36486070272', 'volume': '76468831', 'volume_avg': '45176557', 'shares': '1085549952', 'stock_exchange_long': 'NASDAQ Stock Exchange', 'stock_exchange_short': 'NASDAQ', 'timezone': 'EDT', 'timezone_name': 'America/New_York', 'gmt_offset': '-14400', 'last_trade_time': '2019-10-30 16:00:01', 'pe': '173.46', 'eps': '0.19'}, {'symbol': 'ATVI', 'name': 'Activision Blizzard, Inc.', 'currency': 'USD', 'price': '55.87', 'price_open': '55.25', 'day_high': '55.95', 'day_low': '54.41', '52_week_high': '70.29', '52_week_low': '39.85', 'day_change': '1.87', 'change_pct': '3.46', 'close_yesterday': '54.00', 'market_cap': '42853740544', 'volume': '7582605', 'volume_avg': '5537814', 'shares': '767025984', 'stock_exchange_long': 'NASDAQ Stock Exchange', 'stock_exchange_short': 'NASDAQ', 'timezone': 'EDT', 'timezone_name': 'America/New_York', 'gmt_offset': '-14400', 'last_trade_time': '2019-10-30 16:00:01', 'pe': '25.51', 'eps': '2.19'}]}

	# Second, make API requests to get all data on each symbol and insert into database
	my_api_token = 'SDkzDidRK2esOGFgvME99XA3L5W52dMSnNFYHHpO2V775gKFI4GwZ6w0vdha'

	conn = sqlite3.connect('db.sqlite3')
	cursor = conn.cursor()

	wtd = WorldTradingData(my_api_token)

	try:
		for symbol_batch in symbol_batches:
			dict_response = wtd.stock(symbol_batch)

			for stock in dict_response['data']:
				cursor.execute('INSERT INTO Stocks VALUES (?,?,?,?)', (stock['symbol'],stock['name'],stock['price'],stock['volume']))
				conn.commit()
				
			print("Total of ", cursor.rowcount, " records inserted successfully")
	except sqlite3.Error as err:
		print('Failed to insert records. Error: ', err)
	finally:
		conn.close()

