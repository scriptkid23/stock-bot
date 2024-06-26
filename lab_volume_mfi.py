import pandas as pd
import ta
# Đọc dữ liệu từ file CSV
import mplfinance as mpf

# Chuyển đổi cột 'date' sang định dạng datetime
# Tạo một DataFrame từ dữ liệu giá trị
from vnstock3 import Vnstock

stock = Vnstock().stock(symbol='MWG', source='TCBS')

for i in stock.company.events()['event_desc']:
    print(i)

print('Company: {}'.format(stock.company.profile()['company_name']))

data = stock.quote.history(start='2018-05-17', end='2024-06-25')

data['time'] = pd.to_datetime(data['time'])

data.set_index('time', inplace=True)


data = ta.add_all_ta_features(
    data, 'open', 'high', 'low', 'close', 'volume')
print(data['volume_mfi'])


mpf.plot(data, type='candle', style='yahoo', addplot=[mpf.make_addplot(data['volume_mfi'], panel=1, ylabel='MFI'), mpf.make_addplot([20] * len(data), panel=1, color='r', linestyle='--'),
                                                      mpf.make_addplot([80] * len(data), panel=1, color='r', linestyle='--')])
