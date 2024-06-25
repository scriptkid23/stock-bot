from keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import tensorflow as tf

# Load the pre-trained model
model = load_model('./lstm_model.keras')

# Load the dataset
data = pd.read_csv('datasets/models.csv')

# Extract relevant features
feature_data = data[['Open', 'High', 'Low', 'Close']].values

# Print the feature data
print("Feature Data:\n", feature_data)

# Create a MinMaxScaler object
scaler = MinMaxScaler()

# Scale the columns of the feature_data DataFrame
scaled_feature_data = scaler.fit_transform(feature_data)

# Print the scaled data
print("Scaled Feature Data:\n", scaled_feature_data)

# Define the number of time steps and features
time_steps = 5  # the number of lookback
num_features = 4  # the number of features (Open, High, Low, Close)

# Prepare the test data
X_test = []

# Get the last `time_steps` of scaled data for prediction
for i in range(time_steps, len(scaled_feature_data) + 1):
    X_test.append(scaled_feature_data[i - time_steps:i])

# Convert to numpy array and reshape
X_test = np.array(X_test)

# Print the shape of X_test
print("Shape of X_test:", X_test.shape)

# Print the first 5 elements of the feature data
print("First 5 elements of feature data:\n", feature_data[:5])

predicted_scaled = model.predict(X_test)

predicted = scaler.inverse_transform(predicted_scaled)

print("Predicted Value for June 25, 2024:\n", predicted[0])
