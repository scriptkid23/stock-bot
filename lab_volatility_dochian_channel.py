import pandas as pd
import mplfinance as mpf

# Chọn khoảng thời gian từ 'start_date' đến 'end_date'
import ta
from vnstock3 import Vnstock

stock = Vnstock().stock(symbol='ACB', source='TCBS')


data = stock.quote.history(start='2018-05-17', end='2024-06-26')

data['time'] = pd.to_datetime(data['time'])

data.set_index('time', inplace=True)

data = ta.add_all_ta_features(
    data, 'open', 'high', 'low', 'close', 'volume')

# Xác định điểm mua và điểm bán
buy_signals = []
sell_signals = []

for i in range(1, len(data)):
    if data['close'][i] > data['volatility_dch'][i-1]:
        # Giá vượt qua đường trên (Upper Band) - Điểm mua
        buy_signals.append((data.index[i], data['close'][i]))
    elif data['close'][i] < data['volatility_dcl'][i-1]:
        # Giá vượt qua đường dưới (Lower Band) - Điểm bán
        sell_signals.append((data.index[i], data['close'][i]))

# In ra các điểm mua và điểm bán
print("Điểm mua:")
for signal in buy_signals:
    print("Ngày:", signal[0].strftime("%Y-%m-%d"), "- Giá:", signal[1])

print("\nĐiểm bán:")
for signal in sell_signals:
    print("Ngày:", signal[0].strftime("%Y-%m-%d"), "- Giá:", signal[1])