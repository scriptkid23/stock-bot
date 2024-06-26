from pandas import DataFrame


def fibonacci_retracement_levels_calculate(df: DataFrame):

    highest_high = df['high'].rolling(window=20).max()
    lowest_low = df['low'].rolling(window=20).min()
    range_high = highest_high - lowest_low
    fibonacci_levels = {
        0.0: lowest_low,
        0.236: lowest_low + 0.236 * range_high,
        0.382: lowest_low + 0.382 * range_high,
        0.5: lowest_low + 0.5 * range_high,
        0.618: lowest_low + 0.618 * range_high,
        1.0: highest_high
    }

    return fibonacci_levels


def macd_calculate(df: DataFrame):
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_histogram = macd_line - signal_line

    return macd_line, signal_line, macd_histogram


def rsi_calculate(df: DataFrame):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    average_gain = gain.rolling(window=14).mean()
    average_loss = loss.rolling(window=14).mean()
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def pivot_points_calculate(df: DataFrame):
    pivot_point = (df['high'] + df['low'] + df['close']) / 3
    support_level_1 = pivot_point - (df['high'] - df['low'])
    support_level_2 = pivot_point - 2 * (df['high'] - df['low'])
    resistance_level_1 = pivot_point + (df['high'] - df['low'])
    resistance_level_2 = pivot_point + 2 * (df['high'] - df['low'])

    return support_level_1, support_level_2, resistance_level_1, resistance_level_2

def bollinger_bands_calculate(df: DataFrame):
    rolling_mean = df['close'].rolling(window=20).mean()
    rolling_std = df['close'].rolling(window=20).std()
    upper_band = rolling_mean + 2 * rolling_std
    lower_band = rolling_mean - 2 * rolling_std

    return upper_band, lower_band

def stochastic_oscillator_calculate(df: DataFrame):
    high = df['high']
    low = df['low']
    close = df['close']

    k_period = 14  # Kỳ tính toán Stochastic Oscillator
    d_period = 3  # Kỳ tính toán Stochastic Oscillator (đường D)

    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()

    k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d = k.rolling(window=d_period).mean()

    return k, d