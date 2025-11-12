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
data_df = pd.read_csv('./10장_data/auto-mpg.csv', header=0, engine='python')

print("✅ 원본 데이터셋 크기:", data_df.shape)
print(data_df.head())

# =========================
# 🧹 불필요한 열 제거
# =========================
data_df = data_df.drop(['car_name', 'origin', 'horsepower'], axis=1)
print("\n✅ 열 제거 후 데이터셋 크기:", data_df.shape)
data_df.info()

# =========================
# 🎯 입력(X) / 출력(Y) 데이터 설정
# =========================
X = data_df.drop(['mpg'], axis=1)
Y = data_df['mpg']

# 학습용 / 테스트용 분리 (7:3)
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
# ⚙️ 회귀 계수 출력
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
features = ['model_year', 'acceleration', 'displacement', 'weight', 'cylinders']

for i, feature in enumerate(features):
    row = i // 3
    col = i % 3
    sns.regplot(x=feature, y="mpg", data=data_df, ax=axs[row][col])

plt.tight_layout()
plt.show()

# =========================
# 🧮 사용자 입력을 통한 예측
# =========================
try:
    print("\n🚗 새로운 차량의 연비 예측하기")
    cylinders = float(input("cylinders: "))
    displacement = float(input("displacement: "))
    weight = float(input("weight: "))
    acceleration = float(input("acceleration: "))
    model_year = float(input("model_year: "))

    new_data = pd.DataFrame(
        [[cylinders, displacement, weight, acceleration, model_year]],
        columns=['cylinders', 'displacement', 'weight', 'acceleration', 'model_year']
    )

    prediction = lr.predict(new_data)
    print("\n🔮 예측 연비(mpg):", prediction[0])
except Exception as e:
    print("⚠️ 입력 또는 예측 중 오류:", e)
