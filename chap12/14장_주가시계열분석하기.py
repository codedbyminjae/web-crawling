import os
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# -------------------------
# 1. 데이터 다운로드
# -------------------------
name = 'GOOG'
start_day = '2021-01-01'
end_day = '2024-08-01'

stock = yf.download(name, start=start_day, end=end_day)

# 종가만 사용
stock2 = pd.DataFrame(stock['Close'])

# 저장 폴더 자동 생성
save_dir = '14장_data'
os.makedirs(save_dir, exist_ok=True)
stock2.to_csv(f'{save_dir}/{name}.csv', index=False, encoding='utf-8-sig')

# -------------------------
# 2. 정규화
# -------------------------
stock_values = stock2.values

scaler = MinMaxScaler(feature_range=(0, 1))
stock_scaled = scaler.fit_transform(stock_values)

# -------------------------
# 3. 학습 데이터 구성
# -------------------------
n_train = int(len(stock_scaled) * 0.8)

X_train, Y_train = [], []
for i in range(20, n_train):
    X_train.append(stock_scaled[i-20:i, 0])
    Y_train.append(stock_scaled[i, 0])

X_train = np.array(X_train)
Y_train = np.array(Y_train)

# LSTM 입력 형태 변환 (samples, timesteps, features)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# -------------------------
# 4. LSTM 모델 구축 및 학습
# -------------------------
model = Sequential()
model.add(LSTM(20, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(20, return_sequences=False))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, Y_train, epochs=10, batch_size=1, verbose=2)

# -------------------------
# 5. 평가 데이터 구성
# -------------------------
stock_test = stock_scaled[n_train-20:]
X_test = []

for i in range(20, len(stock_test)):
    X_test.append(stock_test[i-20:i, 0])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# 예측
predicted_value = model.predict(X_test)
predicted_value = scaler.inverse_transform(predicted_value)

# -------------------------
# 6. 시각화 준비
# -------------------------
stock_train_vis = stock.iloc[:n_train].copy()
stock_test_vis = stock.iloc[n_train:].copy()

stock_test_vis.loc[:, 'Predictions'] = predicted_value

# -------------------------
# 7. 시각화
# -------------------------
plt.figure(figsize=(12, 8))
plt.plot(stock_train_vis['Close'], label='Train')
plt.plot(stock_test_vis['Close'], label='Test')
plt.plot(stock_test_vis['Predictions'], label='Prediction')
plt.legend()
plt.title(f'{name} ({start_day} ~ {end_day})')
plt.show()
