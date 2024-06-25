import os
from vnstock3 import Vnstock
import pandas as pd
import mplfinance as mpf


def main():
    if "ACCEPT_TC" not in os.environ:
        os.environ['ACCEPT_TC'] = 'tôi đồng ý'

    vni = pd.read_excel('datasets/vni-01.xlsx')

    vni['day'] = pd.to_datetime(vni['day'],  format='%d/%m/%Y')
    vni.set_index('day', inplace=True)
    vni = vni[['open', 'high', 'low', 'last']]


    # Đổi tên các cột để phù hợp với yêu cầu của mplfinance
    vni.rename(columns={'last': 'Close', 'open': 'Open',
               'high': 'High', 'low': 'Low'}, inplace=True)

    vni.dropna(inplace=True)
    
    print(vni.to_csv('datasets/models.csv'))


if __name__ == "__main__":
    main()
