# temp_text_utils에 아래 코드 전체를 저장
# 모듈 레벨 변수
DEFAULT_ENCODING = 'utf-8'
VERSION = '1.0.0'

def count_syllables_korean(text):
    """한글 텍스트의 음절 수 계산"""
    import re
    # [가-힣] : 한글 완성형 음절(가~힣)에 해당하는 모든 문자 하나하나를 찾는 정규표현식 패턴
    korean_syllables = re.findall(r'[가-힣]', text)
    return len(korean_syllables)

def extract_numbers(text):
    """텍스트에서 숫자 추출"""
    import re  
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    result = []
    for num in numbers:
        if '.' in num:
            result.append(float(num))
        else:
            result.append(int(num))
    return result

def text_summary(text):
    """텍스트 요약 정보"""
    return {
        'length': len(text),
        'words': len(text.split()),
        'lines': len(text.split('\n')),
        'korean_syllables': count_syllables_korean(text),
        'numbers': extract_numbers(text)
    }
