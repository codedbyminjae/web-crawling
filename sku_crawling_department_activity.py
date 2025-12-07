import requests
from bs4 import BeautifulSoup
import csv

URL = "https://cs.skuniv.ac.kr/cs_department_activities"

res = requests.get(URL)
soup = BeautifulSoup(res.text, "html.parser")

# 제목 (카테고리명)
title_elem = soup.select_one("#coda-slider > div > div:nth-child(2) > div > h3")
category = title_elem.get_text(strip=True) if title_elem else "산학연협력"

# 테이블
table = soup.select_one("#coda-slider > div > div:nth-child(2) > div > table")
rows = table.select("tr") if table else []

data = []

for tr in rows:
    cols = tr.select("td")
    if len(cols) != 4:
        continue  # 4개 컬럼이 아닌 행은 스킵

    period = cols[0].get_text(strip=True)
    partner = cols[1].get_text(strip=True)
    description = cols[2].get_text(strip=True)
    result = cols[3].get_text(strip=True)

    data.append([category, period, partner, description, result])

# CSV 저장
with open("industry_cooperation.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["category", "period", "partner", "description", "result"])
    writer.writerows(data)

print("산학연협력 크롤링 완료. 총", len(data), "행 저장됨.")
