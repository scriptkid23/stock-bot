import pandas as pd
import ta
import mplfinance as mpf
# Giả định bạn đã có dữ liệu giá trị trong DataFrame có cột 'Close' chứa giá đóng cửa của tài sản.

# Tạo một DataFrame từ dữ liệu giá trị
from vnstock3 import Vnstock

stock = Vnstock().stock(symbol='ACB', source='TCBS')

print('Company: {}'.format(stock.company.profile()['company_name']))

data = stock.quote.history(start='2018-05-17', end='2024-06-25')


data['time'] = pd.to_datetime(data['time'])
data.set_index('time', inplace=True)


data = ta.add_all_ta_features(
    data, 'open', 'high', 'low', 'close', 'volume')
support_level = data['trend_ichimoku_a']
resistance_level = data['trend_ichimoku_b']

tenkan_sen = data['trend_ichimoku_conv']
kijun_sen = data['trend_ichimoku_base']

# Xác định các ngày có tín hiệu tăng giá và giảm giá
data['signal'] = 0  # Khởi tạo cột tín hiệu

for i in range(1, len(data)):
    if tenkan_sen[i] > kijun_sen[i] and tenkan_sen[i-1] <= kijun_sen[i-1]:
        data['signal'][i] = 1  # Tín hiệu mua (tăng giá)
    elif tenkan_sen[i] < kijun_sen[i] and tenkan_sen[i-1] >= kijun_sen[i-1]:
        data['signal'][i] = -1  # Tín hiệu bán (giảm giá)

# In các ngày có tín hiệu tăng giá và giảm giá
buy_signals = data[data['signal'] == 1]
sell_signals = data[data['signal'] == -1]

print("Ngày có tín hiệu tăng giá:")
print(buy_signals)
print("\nNgày có tín hiệu giảm giá:")
print(sell_signals)
