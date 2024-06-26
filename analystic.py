import pandas as pd
import argparse
from analystic.adi import analystic_adi
from analystic.ichimoku import Sign, analystic_ichimoku
from analystic.mfi import analystic_mfi
import mplfinance as mpf
from analystic.obv import analystic_obv
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True,
                    help='Path to the input CSV file')
parser.add_argument('--start_date', type=str, required=True,
                    help='Specify the start date in YYYY-MM-DD format')
parser.add_argument('--end_date', type=str, required=True,
                    help='Specify the end date in YYYY-MM-DD format')
args = parser.parse_args()

data_raw = pd.read_csv(args.file)

# Chuyển đổi cột 'date' sang kiểu dữ liệu datetime
data_raw['date'] = pd.to_datetime(data_raw['date'])

data_raw.sort_values('date', inplace=True)


# Đặt cột 'date' làm chỉ mục (index)
data_raw.set_index('date', inplace=True)

# Select data within the specified date range
data = data_raw.loc[args.start_date:args.end_date]

func = [analystic_obv, analystic_adi, analystic_mfi, analystic_ichimoku]

for i in func:
    data = data.join(i(data.copy()))

data.index = pd.to_datetime(data.index)

print("===============Analystic All====================")
print(data)

print("==============Buy Now=================")


print(data[data['mfi'] <= 20])

print("==============Sell Now=================")


print(data[data['mfi'] >= 80])
mpf.plot(data, type='candle', style='yahoo', addplot=[mpf.make_addplot(data['mfi'], panel=1, ylabel='MFI'), mpf.make_addplot([20] * len(data), panel=1, color='r', linestyle='--'),
                                                      mpf.make_addplot([80] * len(data), panel=1, color='r', linestyle='--')])


