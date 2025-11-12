import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# 📂 데이터 불러오기
# =========================
data_df = pd.read_csv(
    './10장_data/대기오염데이터_종로구_20220401_20240215.csv',
    header=0, encoding='CP949', engine='python'
)

print("✅ 원본 데이터 미리보기:")
print(data_df.head())

# =========================
# 🧹 불필요한 열 제거 및 결측치 처리
# =========================
data_df = data_df.drop(['location', 'day'], axis=1)
data_df = data_df.dropna()

print("\n✅ 전처리 완료 데이터:")
print(data_df.head())

# =========================
# 🎯 입력(X) / 출력(Y) 데이터 설정
# =========================
X = data_df[['so2', 'co', 'o3', 'no2', 'pm10']]
Y = data_df['pm25']

# 데이터 분할 (train/test = 7:3)
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3, random_state=10
)

# =========================
# 🤖 선형 회귀 모델 학습
# =========================
lr = LinearRegression()
lr.fit(X_train, Y_train)
Y_predict = lr.predict(X_test)

# =========================
# 📊 성능 평가 (MSE, RMSE, R²)
# =========================
mse = mean_squared_error(Y_test, Y_predict)
rmse = np.sqrt(mse)
r2 = r2_score(Y_test, Y_predict)

print("\n📈 모델 평가 지표")
print("MSE:", mse)
print("RMSE:", rmse)
print("R²:", r2)

# =========================
# ⚙️ 회귀 계수 확인
# =========================
print("\n⚙️ 회귀식 정보")
print("Intercept:", lr.intercept_)
print("Coefficients:", lr.coef_)

coef = pd.Series(lr.coef_, index=X.columns)
coef_sort = coef.sort_values(ascending=False)
print("\n📊 변수 중요도 (큰 순서대로)")
print(coef_sort)

# =========================
# 📉 시각화
# =========================
sns.set(style="whitegrid")
fig, axs = plt.subplots(2, 3, figsize=(15, 10))
features = ['so2', 'co', 'o3', 'no2', 'pm10']

for i, feature in enumerate(features):
    row = i // 3
    col = i % 3
    sns.regplot(x=feature, y="pm25", data=data_df, ax=axs[row][col])

plt.tight_layout()
plt.show()
