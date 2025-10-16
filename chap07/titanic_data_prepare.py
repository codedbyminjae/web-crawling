import pandas as pd

# 타이타닉 데이터 로드
titanic = sns.load_dataset("titanic")

# chap07/titanic+survival/ 에 csv로 저장
titanic.to_csv('titanic.csv', index=False)
print("✔ titanic.csv 저장 완료")

print(titanic.head())   # 상위 5개 행 확인
print(titanic.info())   # 결측값, 열 타입 등 확인

# 1. CSV 파일 로드
titanic = pd.read_csv('titanic.csv')  # 현재 작업 디렉토리에 titanic.csv 파일이 있어야 함

# 2. 결측치 확인
print(titanic.isnull().sum())

# 3. 'age' 컬럼의 결측치는 중앙값으로 채움
titanic['age'] = titanic['age'].fillna(titanic['age'].median())

# 4. 'embarked' 컬럼의 값 분포 확인 (결측치 대체 위한 값 확인)
print(titanic['embarked'].value_counts())

# 5. 'embarked' 컬럼의 결측치는 최빈값 'S'로 채움
titanic['embarked'] = titanic['embarked'].fillna('S')

# 6. 'embark_town' 컬럼의 값 분포 확인
print(titanic['embark_town'].value_counts())

# 7. 'embark_town' 컬럼의 결측치도 최빈값 'Southampton'으로 채움
titanic['embark_town'] = titanic['embark_town'].fillna('Southampton')

# 8. 'deck' 컬럼의 값 분포 확인
print(titanic['deck'].value_counts())

# 9. 'deck' 컬럼의 결측치는 가장 많은 값인 'C'로 채움
titanic['deck'] = titanic['deck'].fillna('C')

# 10. 최종 결측치 확인 (모든 NaN이 처리되었는지 확인)
print(titanic.isnull().sum())

# 11. 처리된 데이터를 새 파일로 저장
titanic.to_csv('titanic2.csv', index=False)  # 새 파일로 저장 (titanic2.csv)
