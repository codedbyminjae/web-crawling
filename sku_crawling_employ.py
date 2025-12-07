import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs
import re

# 게시글 번호 추출
def extract_post_id(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if "document_srl" in query:
        return query["document_srl"][0]

    tail = parsed.path.split("/")[-1]
    if tail.isdigit():
        return tail

    return None


# 상세페이지 크롤링
def crawl_detail(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.select_one(
        "#content > div.fbox.content-box.job > article > div > div.viewDocument > div > div.boardReadHeader > div.titleArea > h3 > a"
    ).get_text(strip=True)

    writer = soup.select_one(
        "#content > div.fbox.content-box.job > article > div > div.viewDocument > div > div.boardReadHeader > div.authorArea > a"
    ).get_text(strip=True)

    date = soup.select_one(
        "#content > div.fbox.content-box.job > article > div > div.viewDocument > div > div.boardReadHeader > div.titleArea > span > span.date"
    ).get_text(strip=True)
    date = date.split()[0]

    body_div = soup.select_one(
        "#content > div.fbox.content-box.job > article > div > div.viewDocument > div > div.boardReadBody > div"
    )

    if body_div:
        raw = body_div.get_text(" ", strip=True)
        body = re.sub(r"\s+", " ", raw)
    else:
        body = ""

    return title, body, writer, date


# 페이지 이동하며 2021년까지 수집
BASE_URL = "https://cs.skuniv.ac.kr/index.php?mid=cs_job&page="
page = 0

seen_ids = set()
results = []

while True:
    url = BASE_URL + str(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    raw_links = soup.select("td.title a")

    if not raw_links:
        break

    stop_flag = False

    for a in raw_links:
        href = a.get("href", "")

        if not href or href.startswith("#"):
            continue

        if (href.startswith("/") and href[1:].isdigit()) or ("document_srl=" in href):
            detail_url = "https://cs.skuniv.ac.kr" + href if href.startswith("/") else href
            post_id = extract_post_id(detail_url)

            if not post_id:
                continue

            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)

            title, body, writer, date = crawl_detail(detail_url)

            # 2021년 이전이면 종료
            if (date.startswith("2020") or
                date.startswith("2019") or
                date.startswith("2018") or
                date.startswith("2017")):
                stop_flag = True
                break

            results.append([post_id, title, body, writer, date, "취업정보"])

    if stop_flag:
        break

    page += 1


# CSV 저장
with open("employ_until_2021_clean.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "title", "body", "writer", "date", "type"])
    writer.writerows(results)

print("크롤링 완료. 총", len(results), "개 수집됨.")
