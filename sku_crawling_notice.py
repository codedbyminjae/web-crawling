import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs
import re

# 1) PK 추출 함수
def extract_post_id(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # index.php?document_srl=12353
    if "document_srl" in query:
        return query["document_srl"][0]

    # /12353
    tail = parsed.path.split("/")[-1]
    if tail.isdigit():
        return tail

    return None

# 2) 상세 페이지 크롤링
def crawl_detail(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 제목
    title = soup.select_one(
        "#content > div.fbox.content-box.notice > article > div > div.viewDocument > div > div.boardReadHeader > div.titleArea > h3 > a"
    ).get_text(strip=True)

    # 작성자
    writer = soup.select_one(
        "#content > div.fbox.content-box.notice > article > div > div.viewDocument > div > div.boardReadHeader > div.authorArea > a"
    ).get_text(strip=True)

    # 날짜 (시간 제거)
    date = soup.select_one(
        "#content > div.fbox.content-box.notice > article > div > div.viewDocument > div > div.boardReadHeader > div.titleArea > span > span.date"
    ).get_text(strip=True)
    date = date.split()[0]  # ← 날짜만 남기기

    # 본문 (줄바꿈 제거 + 하나의 문장으로 정리)
    body_div = soup.select_one(
        "#content > div.fbox.content-box.notice > article > div > div.viewDocument > div > div.boardReadBody > div"
    )

    if body_div:
        raw = body_div.get_text(" ", strip=True)
        body = re.sub(r"\s+", " ", raw)  # 공백 여러 개 → 하나로
    else:
        body = ""

    return title, body, writer, date

# 3) 페이지 자동 이동하며 2021년까지 수집
BASE_URL = "https://cs.skuniv.ac.kr/index.php?mid=cs_notice&page="
page = 0

seen_ids = set()
results = []

while True:
    print(f"\n페이지 {page} 크롤링 중...")

    url = BASE_URL + str(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    raw_links = soup.select("td.title a")

    if not raw_links:
        print("더 이상 페이지가 없음 → 종료")
        break

    stop_flag = False  # 2021년 이전이면 종료

    for a in raw_links:
        href = a.get("href", "")

        # 스팸 링크 제거
        if not href or href.startswith("#"):
            continue

        # 글 링크 필터링
        if (href.startswith("/") and href[1:].isdigit()) or ("document_srl=" in href):

            detail_url = "https://cs.skuniv.ac.kr" + href if href.startswith("/") else href
            post_id = extract_post_id(detail_url)

            if not post_id:
                continue

            # 중복 제거
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)

            # 상세 페이지 크롤링
            print(f"- 크롤링 중: {detail_url}")
            title, body, writer, date = crawl_detail(detail_url)

            # 🛑 2021년 이전 게시글이면 STOP
            if (date.startswith("2020") or
                date.startswith("2019") or
                date.startswith("2018") or
                date.startswith("2017") or
                date.startswith("2016")):
                print("🛑 2021년 이전 게시글 도달 → 종료")
                stop_flag = True
                break

            results.append([post_id, title, body, writer, date, "공지사항"])

    if stop_flag:
        break

    page += 1

# 4) CSV 저장
with open("notice_until_2021.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "body", "writer", "date", "type"])
    writer.writerows(results)

print("\n크롤링 완료. notice_until_2021.csv 생성됨.")
print(f"총 {len(results)}개 게시글 수집됨.")
