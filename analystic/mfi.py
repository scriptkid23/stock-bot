import pandas as pd

import ta


def analystic_mfi(data: pd.DataFrame):

    data.index = pd.to_datetime(data.index)

    # Calculate MFI (Money Flow Index)
    mfi = ta.volume.money_flow_index(
        data['high'], data['low'], data['close'], data['volume'])
    
    data['mfi'] = mfi


    return data['mfi']