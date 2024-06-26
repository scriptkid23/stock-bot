
import pandas as pd
import ta


def analystic_obv(data: pd.DataFrame):

    # Tính chỉ số OBV
    data['obv'] = ta.volume.on_balance_volume(
        data['close'], data['volume'])

    # Xác định xu hướng giá dựa trên OBV và cột 'volume_obv'
    data['trend'] = 'sideways'
    data.loc[data['close'] > data['close'].shift(1), 'trend'] = 'up'
    data.loc[data['close'] < data['close'].shift(1), 'trend'] = 'down'

    # Xác định xu hướng OBV
    data['obv_trend'] = 'sideways'
    data.loc[data['obv'] > data['obv'].shift(1), 'obv_trend'] = 'up'
    data.loc[data['obv'] < data['obv'].shift(1), 'obv_trend'] = 'down'

    # Xác định xu hướng kết hợp
    data['combined_trend'] = 'sideways'
    data.loc[(data['trend'] == 'up') & (
        data['obv_trend'] == 'up'), 'combined_trend'] = 'up'
    data.loc[(data['trend'] == 'down') & (
        data['obv_trend'] == 'down'), 'combined_trend'] = 'down'

    # Trả về cột 'combined_trend'
    return data['combined_trend']
