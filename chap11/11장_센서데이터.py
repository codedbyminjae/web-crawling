# 센서 데이터 기반 움직임 분류 (결정 트리)

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import os
from collections import Counter

# 데이터 경로
BASE_DIR = "11장_data/UCI_HAR_Dataset"
FEATURE_PATH = os.path.join(BASE_DIR, "features.txt")
LABEL_PATH = os.path.join(BASE_DIR, "activity_labels.txt")
X_TRAIN_PATH = os.path.join(BASE_DIR, "train", "X_train.txt")
Y_TRAIN_PATH = os.path.join(BASE_DIR, "train", "y_train.txt")
X_TEST_PATH = os.path.join(BASE_DIR, "test", "X_test.txt")
Y_TEST_PATH = os.path.join(BASE_DIR, "test", "y_test.txt")

# 피처명 로드
feature_name = pd.read_csv(FEATURE_PATH, sep=r"\s+", header=None, names=["index", "feature"])
feature_list = feature_name["feature"].tolist()

# 중복 피처명 처리
counter = Counter(feature_list)
new_list = []
dup_count = {}

for name in feature_list:
    if counter[name] == 1:
        new_list.append(name)
    else:
        if name not in dup_count:
            dup_count[name] = 0

        suffix = dup_count[name]
        new_name = f"{name}_{suffix}" if suffix > 0 else name
        new_list.append(new_name)
        dup_count[name] += 1

feature_list = new_list  # 수정된 피처명 사용

# X, Y 데이터 로드
X_train = pd.read_csv(X_TRAIN_PATH, sep=r"\s+", header=None, names=feature_list)
X_test = pd.read_csv(X_TEST_PATH, sep=r"\s+", header=None, names=feature_list)
Y_train = pd.read_csv(Y_TRAIN_PATH, sep=r"\s+", header=None, names=["activity"])
Y_test = pd.read_csv(Y_TEST_PATH, sep=r"\s+", header=None, names=["activity"])

# 레이블명
label_df = pd.read_csv(LABEL_PATH, sep=r"\s+", header=None, names=["id", "label"])
label_list = label_df["label"].tolist()

print("✔ 데이터 로드 완료")
print("X_train:", X_train.shape, "Y_train:", Y_train.shape)
print("X_test:", X_test.shape, "Y_test:", Y_test.shape)

# 기본 결정 트리 모델
dt = DecisionTreeClassifier(criterion="gini", random_state=123)
dt.fit(X_train, Y_train)
pred = dt.predict(X_test)
print("기본 정확도:", accuracy_score(Y_test, pred))

# GridSearchCV (하이퍼파라미터 튜닝)
param_grid = {
    'max_depth': [6, 8, 10, 12],
    'min_samples_split': [8, 16, 24]
}

grid_cv = GridSearchCV(dt, param_grid, cv=3, scoring='accuracy', return_train_score=True)
grid_cv.fit(X_train, Y_train.values.ravel())

print("최적 파라미터:", grid_cv.best_params_)
print("평균 정확도:", grid_cv.best_score_)

# 최적 모델 테스트 성능
best_model = grid_cv.best_estimator_
best_pred = best_model.predict(X_test)
print("최적 모델 정확도:", accuracy_score(Y_test, best_pred))

# 중요 피처 상위 10
importances = best_model.feature_importances_
importance_series = pd.Series(importances, index=feature_list)
top10 = importance_series.sort_values(ascending=False).head(10)

print("\n중요 피처 TOP10:")
print(top10)

# 중요도 그래프
plt.figure(figsize=(10, 6))
top10.sort_values().plot(kind="barh")
plt.title("Top 10 Important Features")
plt.xlabel("Importance")
plt.show()
