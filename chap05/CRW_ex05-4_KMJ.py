import requests
import xml.etree.ElementTree as ET
import pandas as pd

# 공공데이터포털 화재로 인해 정상 접속이 불가하여,
# 서울시 열린데이터광장 API와 엑셀 자료를 활용한 코드입니다.

# 서울시 전기차 충전소 정보 API
API_KEY = "466979656e6d696e3736535561464f"
url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/xml/evChargingStation/1/310"

# API 요청 코드
response = requests.get(url)
root = ET.fromstring(response.content.decode("utf-8"))

# 충전소 정보 추출
rows = []
for item in root.findall(".//row"):
    row_data = {
        "운영기관": item.findtext("OPER_INST_NM", default=""),
        "충전소명": item.findtext("CHARGING_STATION", default=""),
        "충전기ID": item.findtext("CHARGER_ID", default=""),
        "충전기유형": item.findtext("CHARGER_TYPE", default=""),
        "시설대분류": item.findtext("FCLT_SE_L", default=""),
        "시설소분류": item.findtext("FCLT_SE_S", default=""),
        "주소": item.findtext("ADDR", default=""),
        "시군구": item.findtext("SGG", default="").strip(),
        "이용가능시간": item.findtext("UTZTN_PSBLTY_TM", default=""),
        "충전용량": item.findtext("CHARGING_CAPACITY", default="")
    }
    rows.append(row_data)

df_info = pd.DataFrame(rows)

# 엑셀에서 충전량 불러오기 - 파일 위치 중요
excel_path = "서울시_전기차충전량.xlsx"
df_charge = pd.read_excel(excel_path, skiprows=3)

# 충전소명을 기준으로 병합 - 원하는 열에 맞는 배치 방법. 해당 코드는 참조
df_merged = pd.merge(df_info, df_charge, how='left', left_on="충전소명", right_on="충전소명")

# 결과 저장
df_merged.to_csv("서울시_전기차_통합정보.csv", index=False, encoding="utf-8")
print("통합 CSV 저장 완료")
