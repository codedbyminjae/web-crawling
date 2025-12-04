# 8장 영어 단어 빈도 분석

# nltk 경로 추가
import nltk
nltk.data.path.append("C:/Users/minja/AppData/Roaming/nltk_data")

# 라이브러리 로드
import pandas as pd
import glob
import re
from functools import reduce
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS, WordCloud

# 엑셀 파일 불러오기
all_files = glob.glob('8장_data/myCabinetExcelData*.xls')
print(all_files)

# 파일 읽기
all_files_data = []
for file in all_files:
    df = pd.read_excel(file)
    all_files_data.append(df)

# 데이터 합치기
all_files_data_concat = pd.concat(all_files_data, axis=0, ignore_index=True)
print(all_files_data_concat)

# CSV 저장
all_files_data_concat.to_csv('8장_data/riss_bigdata.csv', encoding='utf-8', index=False)

# 제목 컬럼 가져오기
all_title = all_files_data_concat['제목']
print(all_title)

# 정지단어, 표제어 설정
stopWords = set(stopwords.words("english"))
lemma = WordNetLemmatizer()

# 단어 전처리
words = []
for title in all_title:
    EnWords = re.sub(r"[^a-zA-Z]+", " ", str(title))
    EnWordsToken = word_tokenize(EnWords.lower())
    EnWordsTokenStop = [w for w in EnWordsToken if w not in stopWords]
    EnWordsTokenStopLemma = [lemma.lemmatize(w) for w in EnWordsTokenStop]
    words.append(EnWordsTokenStopLemma)

# 단일 리스트로 변환
words2 = list(reduce(lambda x, y: x + y, words))
print(words2)

# 단어 빈도 계산
count = Counter(words2)
print(count)

# 상위 단어 추출
word_count = {}
for tag, counts in count.most_common(50):
    if len(str(tag)) > 1:
        word_count[tag] = counts
        print(f"{tag} : {counts}")

# 히스토그램 1
sorted_Keys = sorted(word_count, key=word_count.get, reverse=True)
sorted_Values = sorted(word_count.values(), reverse=True)

plt.figure()
plt.bar(range(len(word_count)), sorted_Values)
plt.xticks(range(len(word_count)), sorted_Keys, rotation=85)
plt.show()

# big, data 제거
word_count2 = dict(word_count)
word_count2.pop('big', None)
word_count2.pop('data', None)

# 히스토그램 2
sorted_Keys = sorted(word_count2, key=word_count2.get, reverse=True)
sorted_Values = sorted(word_count2.values(), reverse=True)

plt.figure()
plt.bar(range(len(word_count2)), sorted_Values)
plt.xticks(range(len(word_count2)), sorted_Keys, rotation=85)
plt.show()

# 연도별 문서 수 계산
all_files_data_concat['doc_count'] = 0
summary_year = all_files_data_concat.groupby('출판일', as_index=False)['doc_count'].count()
print(summary_year)

# 연도별 그래프
plt.figure(figsize=(12, 5))
plt.plot(range(len(summary_year)), summary_year['doc_count'])
plt.xticks(range(len(summary_year)), summary_year['출판일'])
plt.xlabel("year")
plt.ylabel("doc-count")
plt.grid(True)
plt.show()

# 워드클라우드 생성
stopwords_wc = set(STOPWORDS)
wc = WordCloud(background_color='ivory', stopwords=stopwords_wc, width=800, height=600)
cloud = wc.generate_from_frequencies(word_count)

plt.figure(figsize=(8, 8))
plt.imshow(cloud)
plt.axis('off')
plt.show()

# 이미지 저장
cloud.to_file("8장_data/riss_bigdata_wordCloud.jpg")
print("워드클라우드 저장 완료!")
