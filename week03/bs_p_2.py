from bs4 import BeautifulSoup

html = ('<h1 id="title">한빛출판네트워크</h1> <div class="top"> <ul class="menu"> <li><a '
        'href="http://www.hanbit.co.kr/member/login.html" class="login">로그인</a></li> </ul> '
        '<ul class="brand"> <li><a href="http://www.hanbit.co.kr/media/">한빛미디어</a></li> '
        '<li><a href="http://www.hanbit.co.kr/academy/">한빛아카데미</a></li> </ul> </div>')

soup = BeautifulSoup(html, 'html.parser')

tag_h1 = soup.h1
tag_div = soup.div
tag_ul = soup.ul
tag_li = soup.li
tag_a = soup.a

# 태그 여러 개 모두 찾기
tag_ul_all = soup.find_all("ul")
tag_li_all = soup.find_all("li")
tag_a_all = soup.find_all("a")

tag_a = soup.a

# class 속성으로 태그 찾기
tag_ul_2 = soup.find('ul', attrs={'class': 'brand'})

# id 속성으로 태그 찾기
title = soup.find(id="title")

li_list = soup.select("div>ul.brand>li")
for li in li_list:
    print(li.string)