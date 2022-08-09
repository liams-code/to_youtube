'''
OpenAPI를 이용한 논문, 기사, 글 요약 및 번역
https://jehyunlee.github.io/2022/07/02/Python-DS-106-aaicon/

API 키 발급
RapidAPI : https://rapidapi.com/developer/new
네이버 : https://developers.naver.com/apps/#/register?api=ppg_n2mt
'''

rapidapi_key = 'YOUR_API_KEY_HERE'
naver_client_id = 'YOUR_API_KEY_HERE'
naver_client_secret = 'YOUR_API_KEY_HERE'

import requests
from pprint import pprint

'''
TLDRThis
https://rapidapi.com/tldrthishq-tldrthishq-default/api/tldrthis/


요약의 종류
Abstractive(Human-like) summarization
Abstractive summarization(생성 요약)은 기존 Input text를 그대로 인용하지 않고, 기존의 내용을 새롭게 re-phrasing 하여 Summary를 생성하는 요약 모델입니다.

Extractive summarization
반면에 Extractive summarization(추출 요약)은 기존 Input text에 존재하는 중요한 단어를 그대로 사용하여 Summary를 생성하는 요약 모델입니다.

예시 논문
Attention Is All You Need

페이지 : https://arxiv.org/abs/1706.03762
본문(pdf) : https://arxiv.org/pdf/1706.03762.pdf
'''

# 요약
url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-url/"

payload = {
    "url": "https://arxiv.org/pdf/1706.03762.pdf", # 주소
    "min_length": 100, # 최소 길이
    "max_length": 300, # 최대 길이
    "is_detailed": False # 한 문장으로 반환할 것인지 여부
}

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": rapidapi_key,
    "X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

pprint(response.json())


# 번역  네이버 파파고 API
url = "https://openapi.naver.com/v1/papago/n2mt"

payload = {
    "source": "en",
    "target": "ko",
    "text": summary,
}

headers = {
    "content-type": "application/json",
    "X-Naver-Client-Id": naver_client_id,
    "X-Naver-Client-Secret": naver_client_secret,
}

response = requests.request("POST", url, json=payload, headers=headers)

pprint(response.json())
#요약
print(response.json()['message']['result']['translatedText'])
