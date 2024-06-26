import pandas as pd


# Chọn khoảng thời gian từ 'start_date' đến 'end_date'
import ta
from vnstock3 import Vnstock

stock = Vnstock().stock(symbol='ACB', source='TCBS')


data_raw = stock.quote.history(start='2018-05-17', end='2024-06-25')

data_raw['time'] = pd.to_datetime(data_raw['time'])

data_raw.set_index('time', inplace=True)

data_raw = ta.add_all_ta_features(
    data_raw, 'open', 'high', 'low', 'close', 'volume')

# Xác định xu hướng giá dựa trên OBV và cột 'volume_obv'
# Gán giá trị mặc định 'sideways' cho cột 'trend'
data_raw['trend'] = 'sideways'
data_raw.loc[data_raw['close'] > data_raw['close'].shift(
    1), 'trend'] = 'up'  # Đánh dấu xu hướng tăng giá khi giá tăng
data_raw.loc[data_raw['close'] < data_raw['close'].shift(
    1), 'trend'] = 'down'  # Đánh dấu xu hướng giảm giá khi giá giảm

# Xác định xu hướng OBV
# Gán giá trị mặc định 'sideways' cho cột 'obv_trend'
data_raw['obv_trend'] = 'sideways'
data_raw.loc[data_raw['volume_obv'] > data_raw['volume_obv'].shift(
    1), 'obv_trend'] = 'up'  # Đánh dấu xu hướng tăng OBV khi OBV tăng
data_raw.loc[data_raw['volume_obv'] < data_raw['volume_obv'].shift(
    1), 'obv_trend'] = 'down'  # Đánh dấu xu hướng giảm OBV khi OBV giảm

# Xác định xu hướng kết hợp
# Gán giá trị mặc định 'sideways' cho cột 'combined_trend'
data_raw['combined_trend'] = 'sideways'
data_raw.loc[(data_raw['trend'] == 'up') & (data_raw['obv_trend'] == 'up'),
             'combined_trend'] = 'up'  # Đánh dấu xu hướng tăng kết hợp khi cả giá và OBV tăng
data_raw.loc[(data_raw['trend'] == 'down') & (data_raw['obv_trend'] == 'down'),
             'combined_trend'] = 'down'  # Đánh dấu xu hướng giảm kết hợp khi cả giá và OBV giảm

# Lọc ra những ngày có xu hướng tăng kết hợp
up_combined_trend_days = data_raw[data_raw['combined_trend']
                                  == 'up'].index.tolist()

# Lọc ra những ngày có xu hướng giảm kết hợp
down_combined_trend_days = data_raw[data_raw['combined_trend']
                                    == 'down'].index.tolist()

# In ra các ngày có xu hướng tăng kết hợp
print("Ngày có xu hướng tăng kết hợp:")
for day in up_combined_trend_days:
    print(day)

# In ra các ngày có xu hướng giảm kết hợp
print("Ngày có xu hướng giảm kết hợp:")
for day in down_combined_trend_days:
    print(day)
