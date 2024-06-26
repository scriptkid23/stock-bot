
import pandas as pd
import ta


def analystic_adi(data: pd.DataFrame):

   
    # Tính chỉ số ADI (Accumulation/Distribution Index)
    adi = ta.volume.acc_dist_index(data['high'], data['low'], data['close'], data['volume'])

    data['adi'] = adi

     # Tính toán thời điểm tích luỹ và phân phối
    data['accumulation'] = (data['adi'] > data['adi'].shift(1)).astype(int)
    data['distribution'] = (data['adi'] < data['adi'].shift(1)).astype(int)

    # Xóa cột 'adi'
    data = data.drop('adi', axis=1)

    return data[['accumulation', 'distribution']]
    # xác định giai đoạn tích luỹ và phân phối sau đó lưu vào cột tương ứng

