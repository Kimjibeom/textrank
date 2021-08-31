# -*- coding: utf-8 -*-
"""키워드 네트워크분석.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pH6IzJTSqi4lS0kptSXNzuqrcKgjnPlG

# Google Drive 마운트 하기
"""

from google.colab import drive
drive.mount('/content/drive')

#경로 설정
import os
os.chdir('/content/drive/My Drive/')

# Commented out IPython magic to ensure Python compatibility.
# -*- coding: utf-8 -*-

# %matplotlib inline

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

pip install konlpy

"""# 키워드 추출

텍스트 데이터 전처리
"""

df = pd.read_csv('/content/drive/MyDrive/data/book_data_analysis.csv', encoding='cp949')
df.head()

import re

# 텍스트 정제 함수 : 한글 이외의 문자는 전부 제거합니다.
def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글의 정규표현식을 나타냅니다.
    result = hangul.sub('', text)
    return result

# ‘id’ 피처에 이를 적용합니다.
df['ko_id'] = df['id'].apply(lambda x: text_cleaning(x))
df.head()

# ‘title’ 피처에 이를 적용합니다.
df['ko_title'] = df['title'].apply(lambda x: text_cleaning(x))
df.head()

# ‘title’ 피처에 이를 적용합니다.
df['ko_intro'] = df['intro'].apply(lambda x: text_cleaning(x))
df.head()

from konlpy.tag import Okt
from collections import Counter

# 한국어 약식 불용어사전
korean_stopwords_path = "/content/drive/MyDrive/data/stopword.txt"
with open(korean_stopwords_path, encoding='utf8') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords]

def get_nouns(x):
    nouns_tagger = Okt()
    nouns = nouns_tagger.nouns(x)
    
    # 한글자 키워드를 제거합니다.
    nouns = [noun for noun in nouns if len(noun) > 1]
    
    # 불용어를 제거합니다.
    nouns = [noun for noun in nouns if noun not in stopwords]
    
    return nouns

df['nouns'] = df['ko_intro'].apply(lambda x: get_nouns(x))
print(df.shape)
df.head()

"""# 연관 분석을 이용한 키워드 분석

연관 키워드 추출
"""

pip install apyori

from apyori import apriori

# 지지도 (supprot): P(A∩B)
result=(list(apriori(df['nouns'], min_support=0.01)))
df=pd.DataFrame(result)
df['length'] = df['items'].apply(lambda x: len(x))

# 두 단어의 연관성을 나타내며 0.01 지지도 이상 추출
df = df[(df['length'] == 2) &
        (df['support'] >= 0.01)].sort_values(by='support', ascending=False)

df.head(10)

pip install networkx

# networkx 그래프 정의
import networkx as nx
G = nx.Graph()
ar = (df['items']); G.add_edges_from(ar)

# 페이지 랭크
pr = nx.pagerank(G)
nsize = np.array([v for v in pr.values()])
nsize = 2000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))

# 레이아웃
pos = nx.circular_layout(G) # 원형
# pos = nx.dodecahedral_layout(G)
# pos = nx.rescale_layout(G)

# 네트워크 그래프
plt.figure(figsize=(16,12)); plt.axis('off')
nx.draw_networkx(G, font_family='KoPubDotum', font_size=16,
                 pos=pos, node_color=list(pr.values()), node_size=nsize,
                 alpha=0.7, edge_color='0.5', cmap=plt.cm.YlGn)
plt.savefig('/content/networkx.png', bbox_inches='tight')