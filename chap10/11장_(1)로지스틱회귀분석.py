import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# In [1] 데이터 로드
b_cancer = load_breast_cancer()

# In [2] 데이터프레임 생성
b_cancer_df = pd.DataFrame(b_cancer.data, columns=b_cancer.feature_names)
b_cancer_df['diagnosis'] = b_cancer.target

print("데이터셋 크기:", b_cancer_df.shape)
print(b_cancer_df.head())

# In [3] 데이터 정보 확인
print("\n데이터 정보:")
print(b_cancer_df.info())

# In [4] 데이터 표준화
scaler = StandardScaler()
b_cancer_scaled = scaler.fit_transform(b_cancer.data)

# In [5] 훈련/테스트 분할
X = b_cancer_scaled
Y = b_cancer.target
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=10)

# In [6] 로지스틱 회귀 모델 생성 및 학습
lr_b_cancer = LogisticRegression(max_iter=10000)
lr_b_cancer.fit(X_train, Y_train)

# In [7] 예측
Y_predict = lr_b_cancer.predict(X_test)

# In [8] 혼동 행렬 출력
conf_matrix = confusion_matrix(Y_test, Y_predict)
print("\n혼동 행렬:")
print(conf_matrix)

# In [9] 성능 평가 지표 계산
acc = accuracy_score(Y_test, Y_predict)
pre = precision_score(Y_test, Y_predict)
rec = recall_score(Y_test, Y_predict)
f1 = f1_score(Y_test, Y_predict)
roc = roc_auc_score(Y_test, Y_predict)

# In [10] 평가 결과 출력
print("\n모델 평가 결과")
print("Accuracy :", acc)
print("Precision:", pre)
print("Recall   :", rec)
print("F1 Score :", f1)
print("ROC AUC  :", roc)