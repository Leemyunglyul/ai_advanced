import os
import json
import re
# 정규 표현식 라이브러리

from datetime import datetime

# datetime 모듈에서 datetime.datetime를 가져옵니다.

import random

print(random.randint(1, 100))
# 1~100 사이의 랜덤 정수 생성

print(datetime.now())
# 현재 시간 출력

print(re.findall(r'\b\d+(?:\.\d+)?\b', '어제의 종합주가지수는 3395.54 입니다.'))
# 정규표현식을 이용한 숫자 추출
# 현재 시간을 이용한 파일명 생성
def generate_filename(prefix="output", extension="txt"):
    """타임스탬프를 포함한 파일명 생성"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

# 정규표현식을 이용한 텍스트 처리
def extract_emails(text):
    """텍스트에서 이메일 주소 추출"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # 이메일 패턴 정의(정규표현식)
    
    return re.findall(email_pattern, text)

def extract_korean_words(text):
    """한글 단어만 추출"""
    korean_pattern = r'[가-힣]+'
    return re.findall(korean_pattern, text)

# 테스트
print(f"생성된 파일명: {generate_filename('analysis', 'json')}")

sample_text = "연락처: hong@company.com, kim.dev@gmail.com, Python과 데이터분석을 배우세요!"
emails = extract_emails(sample_text)
korean_words = extract_korean_words(sample_text)

print(f"추출된 이메일: {emails}")
print(f"한글 단어: {korean_words}")