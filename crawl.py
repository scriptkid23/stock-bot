import os
import pandas as pd

from analystic.adi import analystic_adi
from analystic.ichimoku import Sign, analystic_ichimoku
from analystic.mfi import analystic_mfi
import mplfinance as mpf
from analystic.obv import analystic_obv

from lib import bollinger_bands_calculate, fibonacci_retracement_levels_calculate, macd_calculate, pivot_points_calculate, rsi_calculate, stochastic_oscillator_calculate


if "ACCEPT_TC" not in os.environ:
    os.environ["ACCEPT_TC"] = "tôi đồng ý"

# Nạp thư viện sử dụng bình thường
from vnstock3 import Vnstock

stock = Vnstock().stock(symbol='VHM', source='TCBS')

print('Company: {}'.format(stock.company.profile()['company_name']))

datasets = stock.quote.history(start='2018-05-17', end='2024-06-25')

datasets['time'] = pd.to_datetime(datasets['time'])

datasets['range'] = datasets['high'] - datasets['low']

# Tính toán tỉ lệ thay đổi (percentage change)
datasets['change'] = (datasets['close'] - datasets['open']
                      ) / datasets['open'] * 100


print(datasets)


macd_line, signal_line, macd_histogram = macd_calculate(datasets)

rsi = rsi_calculate(datasets)

support_level_1, support_level_2, resistance_level_1, resistance_level_2 = pivot_points_calculate(
    datasets)
fibonacci_levels = fibonacci_retracement_levels_calculate(datasets)
# Xác định các điểm mua và bán
buy_signals = []
sell_signals = []


for i in range(1, len(datasets)):
    # Tín hiệu mua (bullish crossover, MACD Histogram dương, RSI dưới ngưỡng quá mua, giá vượt mức Fibonacci retracement, giá vượt qua mức hỗ trợ 1, và xu hướng tăng)
    if macd_line[i] > signal_line[i] and macd_line[i-1] <= signal_line[i-1] and macd_histogram[i] > 0 and rsi[i] < 70 and datasets['close'][i] > fibonacci_levels[0.618][i] and datasets['close'][i] > support_level_1[i]:
        buy_signals.append(i)
    # Tín hiệu bán (bearish crossover, MACD Histogram âm, RSI trên ngưỡng quá bán, giá dưới mức Fibonacci retracement, giá dưới mức kháng cự 1, và xu hướng giảm)
    elif macd_line[i] < signal_line[i] and macd_line[i-1] >= signal_line[i-1] and macd_histogram[i] < 0 and rsi[i] > 30 and datasets['close'][i] < fibonacci_levels[0.618][i] and datasets['close'][i] < resistance_level_1[i]:
        sell_signals.append(i)



# In ra số lượng các điểm mua và bán
print("Số lượng các điểm mua:", len(buy_signals))
print("Số lượng các điểm bán:", len(sell_signals))

buy_dates = datasets.index[buy_signals]
sell_dates = datasets.index[sell_signals]

# Tạo danh sách tất cả các điểm mua và bán
all_dates = list(buy_dates) + list(sell_dates)

# Sắp xếp danh sách theo ngày tăng dần
sorted_dates = sorted(all_dates)

print("Ngày - Mua/Bán - Giá:")
my_coin = 0
my_fault = 0
max_my_fault = -100000

for date in sorted_dates:
  
    if date in buy_dates:
        index = buy_dates.get_loc(date)
        price = datasets['close'].iloc[buy_signals[index]]
        if my_fault - price >= max_my_fault:
            my_fault -= price
            my_coin += 1
            print(date, "- Mua - Giá:", price)
        else:
            print("Không đủ my_fault để mua vào ngày", date)
    elif date in sell_dates:
        if my_coin == 0:
            break
        index = sell_dates.get_loc(date)
        price = datasets['close'].iloc[sell_signals[index]]
        my_coin -= 1
        my_fault += price
        print(date, "- Bán - Giá:", price)

print("Số lượng my_coin:", my_coin)
print("Số lượng my_fault:", my_fault)

# Tính tổng lợi nhuận (hoặc lỗ) từ các điểm mua và bán
total_buy = 0
total_sell = 0

for buy_signal in buy_signals:
    total_buy += datasets['close'][buy_signal]

for sell_signal in sell_signals:
    total_sell += datasets['close'][sell_signal]

profit = total_sell - total_buy
print("Tổng lợi nhuận (hoặc lỗ):", profit)