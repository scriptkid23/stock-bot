import os
from sklearn.model_selection import train_test_split
from vnstock3 import Vnstock
import pandas as pd
import mplfinance as mpf


def main():
    if "ACCEPT_TC" not in os.environ:
        os.environ['ACCEPT_TC'] = 'tôi đồng ý'

    vni = pd.read_csv('datasets/models.csv')

    datasets = vni[::-1]

    feature_data = datasets[['Open', 'High', 'Low', 'Close']].values

    from sklearn.preprocessing import MinMaxScaler

    # Create a MinMaxScaler object
    scaler = MinMaxScaler()

    # Scale the columns of the feature_data DataFrame
    scaled_feature_data = scaler.fit_transform(feature_data)

    # Print the scaled data

    import numpy as np

    time_steps = 5  # the number of lookback
    num_features = 4  # the number of feature (close and volumes)

    X = []
    y = []

    for i in range(time_steps, len(scaled_feature_data)):
        X.append(scaled_feature_data[i - time_steps: i, :])
        y.append(scaled_feature_data[i, :4])

    X, y = np.array(X), np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False)

    from keras.models import Sequential
    from keras.layers import LSTM, Dense

    model = Sequential()

    model.add(LSTM(units=256, activation='relu', return_sequences=True,
                   input_shape=(time_steps, num_features)))

    model.add(LSTM(units=100, return_sequences=False))

    model.add(Dense(units=50))

    model.add(Dense(units=4))

    model.compile(optimizer="Adam", loss="mean_squared_error", metrics=['mae'])

    model.fit(X_train, y_train,
              epochs=10,
              batch_size=10,
              verbose=1)

    loss, mae = model.evaluate(X_test, y_test)

    print("loss is {} and mae is {}".format(loss, mae))

    predicted = model.predict(X_test)

    predicted = scaler.inverse_transform(predicted)

    y_test = scaler.inverse_transform(y_test)

    model.save('./lstm_model.keras')


if __name__ == "__main__":
    main()
