import pandas as pd
import mplfinance as mpf

# Chọn khoảng thời gian từ 'start_date' đến 'end_date'
import ta
from vnstock3 import Vnstock

stock = Vnstock().stock(symbol='VHM', source='VCI')


print(stock.finance.income_statement(period='year', lang='vi').to_csv("hello.csv"))