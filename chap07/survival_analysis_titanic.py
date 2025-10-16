import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ------------------------------------------------------------
# 1. 데이터 불러오기
# ------------------------------------------------------------
titanic = pd.read_csv('titanic/titanic2.csv')  # 전처리 완료된 타이타닉 데이터 불러오기

# ------------------------------------------------------------
# 2. 성별별 생존/사망 비율 파이차트
# ------------------------------------------------------------
ax = plt.subplots(1, 2, figsize=(10, 5))[1]  # 1행 2열 subplot 생성

# 남성 생존/사망 비율 시각화
titanic[titanic['sex'] == 'male']['survived'].value_counts().plot.pie(
    explode=[0.01, 0.01],        # 파이 조각 간격 설정
    autopct='%1.1f%%',           # 백분율 표시
    ax=ax[0],                    # 왼쪽 subplot
    shadow=True                  # 그림자 효과
)
ax[0].set_title('Survived (Male)')  # 제목 설정
ax[0].set_ylabel('survived')        # y축 레이블 설정

# 여성 생존/사망 비율 시각화
titanic[titanic['sex'] == 'female']['survived'].value_counts().plot.pie(
    explode=[0.01, 0.01],
    autopct='%1.1f%%',
    ax=ax[1],
    shadow=True
)
ax[1].set_title('Survived (Female)')
ax[1].set_ylabel('survived')

plt.show()  # 파이차트 출력

# ------------------------------------------------------------
# 3. 등급별 생존자 수 시각화
# ------------------------------------------------------------
sns.countplot(x='pclass', hue='survived', data=titanic)  # Pclass별 생존자 수 비교
plt.title('Pclass vs Survived')  # 그래프 제목 설정
plt.show()  # 그래프 출력

# ------------------------------------------------------------
# 4. 상관분석
# ------------------------------------------------------------
titanic2 = titanic.select_dtypes(include=[int, float, bool])  # 수치형/불리언 데이터만 선택
print(titanic2.shape)  # 선택된 데이터 크기 확인

titanic_corr = titanic2.corr(method='pearson')  # 피어슨 상관계수 계산
print(titanic_corr)  # 상관계수 결과 출력

titanic_corr.to_csv('titanic/titanic_corr.csv', index=False)  # 상관계수 결과 CSV로 저장

# 특정 변수 간 상관계수 확인
print("Survived vs Adult Male Correlation:", titanic['survived'].corr(titanic['adult_male']))  # 생존 여부 vs 성인남성 여부
print("Survived vs Fare Correlation:", titanic['survived'].corr(titanic['fare']))  # 생존 여부 vs 운임

# ------------------------------------------------------------
# 5. 변수 간 관계 시각화 (pairplot, pointplot)
# ------------------------------------------------------------
sns.pairplot(titanic, hue='survived')  # 생존 여부에 따른 변수 간 관계 시각화
plt.show()

sns.catplot(
    x='pclass',
    y='survived',
    hue='sex',
    data=titanic,
    kind='point'  # 포인트플롯: 성별/등급별 생존률 비교
)
plt.show()

# ------------------------------------------------------------
# 6. 파생 변수 추가
# ------------------------------------------------------------
def category_age(age):  # 나이 구간을 범주형 변수로 변환하는 함수
    if age < 10:
        return 1
    elif age < 20:
        return 2
    elif age < 30:
        return 3
    elif age < 40:
        return 4
    elif age < 50:
        return 5
    elif age < 60:
        return 6
    else:
        return 7

titanic['age2'] = titanic['age'].apply(category_age)  # age2: 연령대 구간 변수 추가
titanic['sex1'] = titanic['sex'].map({'male': 1, 'female': 0})  # 성별을 수치로 변환 (male=1, female=0)
titanic['family'] = titanic['sibsp'] + titanic['parch'] + 1  # 가족 수 변수 추가

titanic.to_csv('titanic/titanic3.csv', index=False)  # 새로운 변수 포함된 CSV 저장

# ------------------------------------------------------------
# ✅ 7. 상관분석 결과 히트맵으로 시각화하기 (추가 부분)
# ------------------------------------------------------------
heatmap_data = titanic[['survived', 'sex1', 'age2', 'family', 'pclass', 'fare']]  # 히트맵용 주요 변수 선택
colormap = plt.cm.RdBu  # 색상 팔레트 지정 (Red-Blue)

plt.figure(figsize=(8, 6))  # 그래프 크기 설정
sns.heatmap(
    heatmap_data.astype(float).corr(),  # 상관계수 계산 및 히트맵 생성
    linewidths=0.1,                     # 셀 경계선 두께
    vmax=1.0,                           # 색상 최대값
    square=True,                        # 정사각형 셀
    cmap=colormap,                      # 색상맵 적용
    linecolor='white',                  # 셀 구분선 색상
    annot=True,                         # 상관계수 숫자 표시
    annot_kws={'size': 10}              # 글자 크기 조정
)

plt.title('Correlation Heatmap of Titanic Variables')  # 히트맵 제목
plt.show()  # 히트맵 출력
