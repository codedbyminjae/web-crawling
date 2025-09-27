import requests
from urllib.parse import unquote
import pandas as pd

# 인증키 디코딩 (requests에서 자동 인코딩되기 때문에), 해당 부분은 검색 후 오류 해결
API_KEY = unquote("69ygK8xCFR0bB3nUN%2B87B8av%2F52PlPZlivyf%2Blzd%2BnR3wKkEtGdI5xrdAJM4NsqM")

# 공공데이터포털의 오류로 인해 교통사고정보 개방 시스템에서 추출
BASE_URL = "https://opendata.koroad.or.kr/data/rest/frequentzone/bicycle"

params = {
    "authKey": API_KEY, # 인증키
    "searchYearCd": "2023", # 연도코드
    "siDo": "11", # 시도코드
    "guGun": "680", #시군구 코드
    "type": "json", # 데이터 유형
    "numOfRows": "10", # 검색 건수
    "pageNo": "1" # 페이지 번호
}

response = requests.get(BASE_URL, params=params)
data = response.json()
items = data['items']['item']
df = pd.DataFrame(items)

df.to_csv("자전거_사고_강남구_2023.csv", index=False, encoding='utf-8')

print("교통사고정보개방시스템에서 자전거 사고 다발지역 데이터를 정상적으로 수신 후 CSV 파일 저장.")
