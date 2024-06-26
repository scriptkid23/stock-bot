import pandas as pd
import mplfinance as mpf

# Chọn khoảng thời gian từ 'start_date' đến 'end_date'
import ta
from vnstock3 import Vnstock

stock = Vnstock().stock(symbol='VHM', source='TCBS')


data = stock.quote.history(start='2018-05-17', end='2024-06-26')

data['time'] = pd.to_datetime(data['time'])

data.set_index('time', inplace=True)

data_raw = ta.add_all_ta_features(
    data, 'open', 'high', 'low', 'close', 'volume')

# Xác định giai đoạn tích lũy và phân phối
for i in range(1, len(data)):
    if data['volume_adi'].iloc[i] > data['volume_adi'].iloc[i-1]:
        print(f"{data.index[i].date()}: Giai đoạn tích lũy")
    else:
        print(f"{data.index[i].date()}: Giai đoạn phân phối")

# Vẽ biểu đồ nến với chỉ số ADI
apds = [
    mpf.make_addplot(data['volume_adi'], panel=1, ylabel='ADI'),
    mpf.make_addplot([0] * len(data), panel=1, color='r', linestyle='--')
]

mpf.plot(data, type='candle', style='yahoo', addplot=apds)