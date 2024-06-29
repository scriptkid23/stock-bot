import os
from sklearn.model_selection import train_test_split
from vnstock3 import Vnstock
import pandas as pd
import mplfinance as mpf

import plotly.graph_objects as go

import numpy as np


if "ACCEPT_TC" not in os.environ:
    os.environ['ACCEPT_TC'] = 'tôi đồng ý'

stock = Vnstock().stock(symbol='HPG', source='VCI')

dataset = stock.quote.history(start='2010-01-01', end='2024-06-29')


import pandas_ta as ta


dataset['EMA'] = ta.ema(dataset.close, length=150)


dataset.tail()


EMAsignal = [0]*len(dataset)
backcandles = 15

for row in range(backcandles, len(dataset)):
    upt = 1
    dnt = 1
    for i in range(row-backcandles, row+1):
        if max(dataset.open[i], dataset.close[i])>=dataset.EMA[i]:
            dnt=0
        if min(dataset.open[i], dataset.close[i])<=dataset.EMA[i]:
            upt=0
    if upt==1 and dnt==1:
        EMAsignal[row]=3
    elif upt==1:
        EMAsignal[row]=2
    elif dnt==1:
        EMAsignal[row]=1

dataset['EMASignal'] = EMAsignal

def isPivot(candle, window):
    """
    function that detects if a candle is a pivot/fractal point
    args: candle index, window before and after candle to test if pivot
    returns: 1 if pivot high, 2 if pivot low, 3 if both and 0 default
    """
    if candle-window < 0 or candle+window >= len(dataset):
        return 0
    
    pivotHigh = 1
    pivotLow = 2
    for i in range(candle-window, candle+window+1):
        if dataset.iloc[candle].low > dataset.iloc[i].low:
            pivotLow=0
        if dataset.iloc[candle].high < dataset.iloc[i].high:
            pivotHigh=0
    if (pivotHigh and pivotLow):
        return 3
    elif pivotHigh:
        return pivotHigh
    elif pivotLow:
        return pivotLow
    else:
        return 0
    

window=10
dataset['isPivot'] = dataset.apply(lambda x: isPivot(x.name,window), axis=1)

def pointpos(x):
    if x['isPivot']==2:
        return x['low']-1e-3
    elif x['isPivot']==1:
        return x['high']+1e-3
    else:
        return np.nan
dataset['pointpos'] = dataset.apply(lambda row: pointpos(row), axis=1)





def detect_structure(candle, backcandles, window):
    """
    Attention! window should always be greater than the pivot window! to avoid look ahead bias
    """
    if (candle <= (backcandles+window)) or (candle+window+1 >= len(dataset)):
        return 0
    
    localdf = dataset.iloc[candle-backcandles-window:candle-window] #window must be greater than pivot window to avoid look ahead bias
    highs = localdf[localdf['isPivot'] == 1].high.tail(3).values
    lows = localdf[localdf['isPivot'] == 2].low.tail(3).values
    levelbreak = 0
    zone_width = 0.001
    if len(lows)==3:
        support_condition = True
        mean_low = lows.mean()
        for low in lows:
            if abs(low-mean_low)>zone_width:
                support_condition = False
                break
        if support_condition and (mean_low - dataset.loc[candle].close)>zone_width*2:
            levelbreak = 1

    if len(highs)==3:
        resistance_condition = True
        mean_high = highs.mean()
        for high in highs:
            if abs(high-mean_high)>zone_width:
                resistance_condition = False
                break
        if resistance_condition and (dataset.loc[candle].close-mean_high)>zone_width*2:
            levelbreak = 2
    return levelbreak


#df['pattern_detected'] = df.index.map(lambda x: detect_structure(x, backcandles=40, window=15))
dataset['pattern_detected'] = dataset.apply(lambda row: detect_structure(row.name, backcandles=40, window=11), axis=1)

print(dataset)