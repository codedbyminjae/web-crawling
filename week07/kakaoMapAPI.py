import os
import requests
import pandas as pd
import folium
import webbrowser

API_KEY = "7bfb068876a482e5ec256a7340ec1e61"

# API 요청 부분
def search_places(keyword, page=1, size=15):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    params = {"query": keyword, "page": page, "size": size}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

def docs_to_df(documents):
    rows = []
    for d in documents:
        rows.append({
            'id': d.get('id'),
            'place_name': d.get('place_name'),
            'category_name': d.get('category_name'),
            'phone': d.get('phone'),
            'address': d.get('address_name'),
            'road_address': d.get('road_address_name'),
            'x': float(d.get('x')) if d.get('x') else None,
            'y': float(d.get('y')) if d.get('y') else None,
            'place_url': d.get('place_url'),
        })
    return pd.DataFrame(rows)

# 실행 코드, 키워드 입력 받기
if __name__ == "__main__":
    keyword = input("검색할 키워드를 입력하세요: ")
    dfs = []
    page = 1

    while True:
        res = search_places(keyword, page=page, size=10)
        df = docs_to_df(res['documents'])
        dfs.append(df)

        if res['meta']['is_end']:
            break
        page += 1

    # 결과 합치기
    result = pd.concat(dfs, ignore_index=True)
    print(result.shape)
    print(result.head())

    # CSV 저장 코드
    csv_name = f"{keyword}_places.csv"
    result.to_csv(csv_name, index=False, encoding="utf-8-sig")
    print(f"CSV 저장 완료: {csv_name}")

    df = pd.read_csv(csv_name)
    center = [37.561498, 127.0134]  # 서울 중심 좌표
    m = folium.Map(location=center, zoom_start=12)

    for _, row in df.dropna(subset=["y", "x"]).iterrows():
        folium.Marker(
            [row["y"], row["x"]],
            popup=f"{row['place_name']}<br>{row['category_name']}",
            tooltip=row["place_name"]
        ).add_to(m)

    # 자동 열기
    fname = f"{keyword}_places_map.html"
    m.save(fname)
    print(f"Saved: {fname}")

    path = os.path.abspath(fname)
    url = "file:///" + path
    webbrowser.open(url, new=2)
