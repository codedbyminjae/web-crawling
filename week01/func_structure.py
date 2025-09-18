# func_structure.py
import json
import urllib.request
import urllib.parse

def getNaverSearch(node, srcText, start, display):
    base = "https://openapi.naver.com/v1/search"
    nodePath = "/%s.json" % node
    url = base + nodePath + "?query=" + urllib.parse.quote(srcText)
    url += "&start=%s&display=%s" % (start, display)

    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        return json.loads(response.read().decode('utf-8'))
    else:
        print("Error Code:", rescode)
        return None


def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']
    pubDate = post['pubDate']

    data = {
        'cnt': cnt,
        'title': title,
        'description': description,
        'org_link': org_link,
        'link': link,
        'pubDate': pubDate
    }
    jsonResult.append(data)
