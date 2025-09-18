# 프로그램 5-2 openapi_tour.py

import urllib.request
import datetime
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

ServiceKey = "Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D"

# [CODE 1]
def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print('[%s] Url Request Success' % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print('[%s] Error for URL: %s' % (datetime.datetime.now(), url))
        return None

# [CODE 2]
def getTourismStatsItem(yyyymm, national_code, ed_cd):
    service_url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    parameters = '?_type=json&serviceKey=' + ServiceKey
    parameters += '&YM=' + yyyymm
    parameters += '&NAT_CD=' + national_code
    parameters += '&ED_CD=' + ed_cd

    url = service_url + parameters
    print(url)

    responseDecode = getRequestUrl(url)
    if responseDecode == None:
        return None
    else:
        return json.loads(responseDecode)

# [CODE 3]
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    natName = ''
    dataEND = "{0}{1:0>2}".format(str(nEndYear), str(12))
    isDataEnd = 0

    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13):
            if isDataEnd == 1:
                break

            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)

            if jsonData['response']['header']['resultMsg'] == 'OK':
                if jsonData['response']['body']['items'] == '':
                    isDataEnd = 1
                    if (month - 1) == 0:
                        year = year - 1
                        month = 13
                    dataEND = "{0}{1:0>2}".format(str(year), str(month - 1))
                    print("데이터 없음....\n제공되는 통계 데이터는 %s년 %s월까지입니다."
                          % (str(year), str(month - 1)))
                    jsonData = getTourismStatsItem(dataEND, nat_cd, ed_cd)
                    break

                print(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))
                natName = jsonData['response']['body']['items']['item']['natKorNm'].replace(' ', '')
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item']['ed']

                print('[ %s_%s : %s ]' % (natName, yyyymm, num))
                print('-' * 70)

                jsonResult.append({'nat_name': natName, 'nat_cd': nat_cd, 'yyyymm': yyyymm, 'visit_cnt': num})
                result.append([natName, nat_cd, yyyymm, num])

                print('마지막 jsonData\n', json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))

    return (jsonResult, result, natName, ed, dataEND)

# [CODE 0]
def main():
    jsonResult = []
    result = []
    natName = ''

    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >>")
    nat_cd = input("국가 코드를 입력하세요 (중국: 112 / 일본: 130 / 미국: 275): ")
    nStartYear = int(input("데이터를 몇 년부터 수집할까요? : "))
    nEndYear = int(input("데이터를 몇 년까지 수집할까요? : "))
    ed_cd = "E"  # E: 방한외래관광객, D: 해외 출국

    jsonResult, result, natName, ed, dataEND = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)

    if natName == '':
        print("데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인해 주시기 바랍니다.")
    else:
        # JSON 저장
        with open('./%s_%s_%d_%s.json' % (natName, ed, nStartYear, dataEND), 'w', encoding='utf8') as outfile:
            jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(jsonFile)

        # CSV 저장
        columns = ['입국국가명', '국가코드', '입국연월', '입국자 수']
        result_df = pd.DataFrame(result, columns=columns)
        result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND), index=False, encoding='cp949')

        # ---------- 그래프 시각화 ----------
        visitCnt = []
        visitYM = []
        index = []
        i = 0
        for item in jsonResult:
            index.append(i)
            visitCnt.append(item['visit_cnt'])
            visitYM.append(item['yyyymm'])
            i += 1

        rc('font', family='Malgun Gothic')
        plt.xticks(index, visitYM)
        plt.plot(index, visitCnt, marker='o')
        plt.xlabel('방문월')
        plt.xticks(rotation=45)
        plt.ylabel(natName + '에서 온 방문객 수')
        plt.title(f'{natName} 방문객 통계 ({nStartYear} ~ {dataEND[:4]})')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    main()
