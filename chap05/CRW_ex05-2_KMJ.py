import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd

# 인증키 및 요청 파라미터, KEY는 발급받은 인증키
API_KEY = "6d646750656d696e38394b4e4f646e"
TYPE = "xml"
SERVICE = "ChunmanFreeSuggestions"
START_INDEX = 1
END_INDEX = 100  # 최대 100건으로 제한

# 요청 URL
url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}"

# API 요청
response = urllib.request.urlopen(url)
res = response.read().decode("utf-8")

# XML 파싱 과정, 해당 부분은 검색 후 사용
root = ET.fromstring(res)
rows = root.findall("row")

# 데이터 저장용 리스트 생성
data = []

# 필요한 항목 추출 및 저장 후 변수명에 맞게 지정
for row in rows:
    sn = row.find("SN").text if row.find("SN") is not None else ""
    title = row.find("TITLE").text if row.find("TITLE") is not None else ""
    content = row.find("CONTENT").text if row.find("CONTENT") is not None else ""
    reg_date = row.find("REG_DATE").text if row.find("REG_DATE") is not None else ""
    vision = row.find("VISIOIN_TXT").text if row.find("VISIOIN_TXT") is not None else ""
    comment_cnt = row.find("USER_COMMENT_CNT").text if row.find("USER_COMMENT_CNT") is not None else ""
    vote_cnt = row.find("VOTE_CNT").text if row.find("VOTE_CNT") is not None else ""
    vote_dis = row.find("VOTE_DIS_CNT").text if row.find("VOTE_DIS_CNT") is not None else ""
    reply_yn = row.find("REPLY_YN").text if row.find("REPLY_YN") is not None else ""

    data.append({
        "제안번호": sn,
        "제안제목": title,
        "제안내용": content,
        "제안등록일자": reg_date,
        "정책분류": vision,
        "시민의견수": comment_cnt,
        "공감수": vote_cnt,
        "비공감수": vote_dis,
        "답변여부": reply_yn
    })

# pandas로 DataFrame 구성, 해당 부분으로 정리
df = pd.DataFrame(data)

# CSV로 파일 저장
df.to_csv("자유제안_정리본.csv", index=False, encoding="utf-8-sig")

print("complete")
