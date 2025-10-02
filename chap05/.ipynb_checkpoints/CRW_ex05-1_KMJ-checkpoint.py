import urllib.request
import urllib.parse
import json
import datetime

# [CODE 1]
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", "U_3jOQdQ6rrJDddqdX1M")
    req.add_header("X-Naver-Client-Secret", "41AmRZ3CPR")

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print("[%s] Error for URL: %s" % (datetime.datetime.now(), url))
        print("Exception:", e)
        return None

# [CODE 2]
def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    nodePath = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (
        urllib.parse.quote(srcText), start, display
    )

    url = base + nodePath + parameters
    responseDecode = getRequestUrl(url)

    if responseDecode is None:
        return None
    else:
        return json.loads(responseDecode)

# [CODE 3]
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    bloggerlink = post['bloggerlink']  # 블로그 주소로 변경
    link = post['link']
    postdate = post['postdate']

    # 날짜 형식을 뉴스와 동일하게 변환
    pDate = datetime.datetime.strptime(postdate, '%Y%m%d')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({
        'cnt': cnt,
        'title': title,
        'description': description,
        'bloggerlink': bloggerlink,
        'link': link,
        'pDate': pDate
    })
    return

# [CODE 0]
def main():
    node = 'blog'  # 블로그 검색으로 변경
    srcText = '월드컵'  # 검색어를 월드컵으로 고정
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)
    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)

        start = jsonResponse['start'] + jsonResponse['display']
        # if start == 1001: break  ← 네이버 검색 API는 무조건 1000건까지만 제공하기에 주석

        jsonResponse = getNaverSearch(node, srcText, start, 100)

    print('전체 검색 : %d 건' % total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" % (cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))

if __name__ == "__main__":
    main()
