import pandas as pd
import mplfinance as mpf
import ta
from enum import Enum


class Sign(Enum):
    Sell = 1
    Buy = -1


def analystic_ichimoku(data: pd.DataFrame):

    ichimoku_indicator = ta.trend.IchimokuIndicator(data['high'], data['low'])

    tenkan_sen = ichimoku_indicator.ichimoku_conversion_line()

    kijun_sen = ichimoku_indicator.ichimoku_base_line()

    data['signal'] = 0

    for i in range(1, len(data)):
        if tenkan_sen[i] > kijun_sen[i] and tenkan_sen[i-1] <= kijun_sen[i-1]:
            data.loc[i, 'signal'] = Sign.Buy.value
        elif tenkan_sen[i] < kijun_sen[i] and tenkan_sen[i-1] >= kijun_sen[i-1]:
            data.loc[i, 'signal'] = Sign.Sell.value

    return data['signal']