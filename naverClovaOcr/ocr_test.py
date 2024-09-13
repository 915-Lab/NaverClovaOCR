import requests
import json
import base64
import time
import uuid
import os
#%%
from dotenv import load_dotenv

load_dotenv('.env')

# 네이버 클라우드 플랫폼에서 발급받은 Secret Key를 입력하세요
secret_key = os.getenv("NAVER_API_KEY")

# OCR Document API 엔드포인트 URL
url = os.getenv("NAVER_API_URL")

# 요청 헤더 설정
headers = {
    'Content-Type': 'application/json',
    'X-OCR-SECRET': secret_key,
}

# 분석할 PDF 파일 경로
pdf_path = 'data/ocr_2.pdf'

# 요청 바디 설정
# request_json = {
#     'version': 'V1',
#     'requestId': str(uuid.uuid4()),  # 고유한 요청 ID 생성
#     'timestamp': int(round(time.time() * 1000)),  # 현재 시간을 밀리초로 표현
#     'lang': 'ko',  # 문서의 언어 설정 (한국어)
#     'images': [
#         {
#             'format': 'pdf',
#             'name': 'sample_pdf',
#             'data': "data/ocr_2.pdf"  # PDF 파일의 Base64 인코딩 데이터가 들어갈 자리
#         }
#     ]
# }

request_json = {
    'version': 'V2',
    'requestId': "string",  # 고유한 요청 ID 생성
    'timestamp': 0,
    'lang': 'ko',  # 문서의 언어 설정 (한국어)
    'images': [
        {
            'format': 'pdf',
            'name': 'sample_pdf',
            'url': url  # PDF 파일의 Base64 인코딩 데이터가 들어갈 자리
        }
    ]
}

# PDF 파일을 읽고 Base64 인코딩
with open(pdf_path, 'rb') as f:
    pdf_data = f.read()
    encoded_pdf = base64.b64encode(pdf_data).decode('utf-8')

# 인코딩된 데이터를 요청 바디에 추가
request_json['images'][0]['data'] = encoded_pdf

try:
    response = requests.post(url, headers=headers, data=json.dumps(request_json))
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print("요청 중 에러 발생:", e)
    exit()

# 응답 결과 확인
if response.status_code == 200:
    result = response.json()
    print("분석 결과:")
    print(json.dumps(result, indent=4, ensure_ascii=False))
else:
    print("요청에 실패했습니다. 상태 코드:", response.status_code)
    print("에러 메시지:", response.text)
