import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from itertools import count
import xml.etree.ElementTree as ET
import ssl

# 요청 함수
def get_request_url(url, enc='utf-8'):
    req = urllib.request.Request(url)
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                ret = response.read().decode(enc)
            except UnicodeDecodeError:
                ret = response.read().decode(enc, 'replace')
            return ret
    except Exception as e:
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


# 페이지별 매장 정보 크롤링
def CheogajipAddress(result):
    for page_idx in range(1, 26):  # 마지막 페이지까지
        Cheogajip_URL = 'http://www.cheogajip.co.kr/bbs/board.php?bo_table=store&page=%s' % str(page_idx)
        print(Cheogajip_URL)

        response = urllib.request.urlopen(Cheogajip_URL)
        soupData = BeautifulSoup(response, 'html.parser')
        tbody_tag = soupData.find('tbody')

        for store_tr in tbody_tag.findAll('tr'):
            t_tag = list(store_tr.strings)
            store_name = t_tag[1].strip()
            store_address = t_tag[3].strip()
            store_sido_gu = store_address.split()[0:2]
            store_phone = t_tag[5].strip()
            result.append([store_name] + store_sido_gu + [store_address, store_phone])


# 전체 실행 및 저장
def cswin_Cheogajip():
    result = []

    print("CHEOGAJIP ADDRESS CRAWLING START")
    CheogajipAddress(result)

    cheogajip_table = pd.DataFrame(result, columns=('store', 'sido', 'gungu', 'store_address', 'store_phone'))
    cheogajip_table.to_csv('./cheogajip.csv', encoding='cp949', mode='w', index=True)
    del result

    print("FINISHED!")


# 실행
if __name__ == '__main__':
    cswin_Cheogajip()
