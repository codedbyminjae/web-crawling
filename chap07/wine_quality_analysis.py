import pandas as pd

# 레드 와인 데이터 불러오기
red_df = pd.read_csv('wine+quality/winequality-red2.csv', header=0, engine='python')

# 상위 5행 확인
print(red_df.head())

# 와인 타입 컬럼 추가 (맨 앞에 삽입)
red_df.insert(0, column='type', value='red')

# 컬럼 추가 후 확인
print(red_df.head())

# 행, 열 개수 확인
print(red_df.shape)

# 화이트 와인 데이터 불러오기
white_df = pd.read_csv('wine+quality/winequality-white2.csv', header=0, engine='python')

# 상위 5행 확인
print(white_df.head())

# 와인 타입 컬럼 추가 (맨 앞에 삽입)
white_df.insert(0, column='type', value='white')

# 추가된 컬럼 확인
print(white_df.head())

# 행, 열 개수 확인
print(white_df.shape)

# 레드 + 화이트 와인 데이터 합치기
wine = pd.concat([red_df, white_df])

# 합쳐진 데이터의 행, 열 개수 확인
print(wine.shape)  # (6497, 13)

# 병합된 데이터 저장
wine.to_csv('wine+quality/wine.csv', index=False)

# 데이터 기본 정보 확인
print(wine.info())

# 컬럼명에 공백이 있으면 밑줄(_)로 대체
wine.columns = wine.columns.str.replace(' ', '_')

# 상위 5행 확인
print(wine.head())

# 기술통계(descriptive statistics) 확인
print(wine.describe())

# quality 열의 고유한 값(등급) 정렬해서 출력
print(sorted(wine.quality.unique()))

# quality별 데이터 개수(빈도수) 확인
print(wine.quality.value_counts())

# 와인 종류(type)에 따른 quality 기술 통계 요약
print(wine.groupby('type')['quality'].describe())

# 평균(mean)만 따로 확인
print(wine.groupby('type')['quality'].mean())

# 표준편차(std)만 따로 확인
print(wine.groupby('type')['quality'].std())

# 평균과 표준편차를 함께 보기 (agg 함수 사용)
print(wine.groupby('type')['quality'].agg(['mean', 'std']))

from statsmodels.formula.api import ols

# 더미변수 추가 (white=1, red=0)
wine['w'] = (wine['type'] == 'white').astype(int)

# 회귀식
formula = (
    'quality ~ fixed_acidity + volatile_acidity + citric_acid + residual_sugar + '
    'chlorides + free_sulfur_dioxide + total_sulfur_dioxide + density + pH + '
    'sulphates + alcohol + w'
)

# 회귀모델 적합
regression_result = ols(formula, data=wine).fit()

# 요약 출력 (이제 정상 작동)
print(regression_result.summary())

# ----------------------------------------
# 와인 유형별 품질 등급 히스토그램
# ----------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns


red_wine_quality = wine.loc[wine['type'] == 'red', 'quality']
white_wine_quality = wine.loc[wine['type'] == 'white', 'quality']

# 시각화 스타일 설정
sns.set_style('dark')

# 레드 와인 품질 분포
sns.histplot(red_wine_quality, stat='density', kde=True, color='red', label='red wine')

# 화이트 와인 품질 분포
sns.histplot(white_wine_quality, stat='density', kde=True, color='orange', label='white wine')

# 그래프 제목 및 범례
plt.title("Quality of Wine Type")
plt.legend()
plt.show()

import matplotlib.pyplot as plt
import statsmodels.api as sm

# fixed_acidity의 부분 회귀 플롯
others = list(set(wine.columns).difference(set(["quality", "fixed_acidity"])))
p, resids = sm.graphics.plot_partregress("quality", "fixed_acidity", others, data=wine, ret_coords=True)
plt.show()

# 전체 변수에 대한 부분 회귀 플롯 그리드
fig = plt.figure(figsize=(8, 13))
sm.graphics.plot_partregress_grid(regression_result, fig=fig)
plt.show()
