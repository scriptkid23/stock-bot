import os
from sklearn.model_selection import train_test_split
from vnstock3 import Vnstock
import pandas as pd
import mplfinance as mpf

import plotly.graph_objects as go

import numpy as np

from analystic import flags_pennants, harmonic_patterns, trendline_automation


if "ACCEPT_TC" not in os.environ:
    os.environ['ACCEPT_TC'] = 'tôi đồng ý'

stock = Vnstock().stock(symbol='HPG', source='VCI')

dataset: pd.DataFrame = stock.quote.history(start='2008-01-01', end='2024-06-29') 



dataset =dataset.loc[(dataset != 0).all(axis=1)]



dataset.rename(columns={'time': 'date'}, inplace=True)



data, bull_flags, bear_flags, bull_pennants, bear_pennants = flags_pennants.prepare(dataset)

# Nhân toàn bộ giá trị của các cột số (trừ cột datetime) với 1000
numeric_columns = dataset.select_dtypes(include=[float, int]).columns



harmonic_patterns.prepare(dataset)
