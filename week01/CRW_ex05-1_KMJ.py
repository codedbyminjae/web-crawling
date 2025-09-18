import urllib.request
import urllib.parse
import json
import datetime

# 네이버 API 키, 보안 설정 필요
client_id = "U_3jOQdQ6rrJDddqdX1M"
client_secret = "41AmRZ3CPR"

# [CODE 1] Request URL 실행
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print("[%s] Error for URL: %s" % (datetime.datetime.now(), url))
        print("Exception:", e)
        return None


# [CODE 2] 네이버 API 호출 함수
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


# [CODE 3] 데이터 가공 getPostData 함수
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']
    pDate = post['pubDate']

    # 날짜 변환
    pDate = datetime.datetime.strptime(pDate, '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({
        'cnt': cnt,
        'title': title,
        'description': description,
        'org_link': org_link,
        'link': link,
        'pDate': pDate
    })
    return


# [CODE 0] 메인 함수 설정
def main():
    node = 'news'
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)
    total = jsonResponse['total']

    while ((jsonResponse is not None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)

    print('전체 검색 : %d 건' % total)

    # JSON 저장 구조
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf-8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" % cnt)
    print('%s_naver_%s.json SAVED' % (srcText, node))


if __name__ == "__main__": # 현재 실행중인 프로세스의 이름 __이름__
    main()
