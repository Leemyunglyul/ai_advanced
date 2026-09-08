# NVIDIA (NVDA) — 최근 4일 주가 시각화 리포트

## 요약
- 기간: 2025-08-05 ~ 2025-08-08 (4거래일)
- 가격:
  - 2025-08-05: $178.26
  - 2025-08-06: $179.42
  - 2025-08-07: $180.77
  - 2025-08-08: $182.70
- 애널리스트 등급: Strong Buy (제공된 정보)
- 제공된 12개월 목표주가: $191.88

## 계산된 통계 (제공된 데이터 기준)
- 시작 → 종료 변동률: (182.70 - 178.26) / 178.26 × 100 = 2.4907% (약 2.49%)
  - 참고: 질문에 적으신 '약 2.44%'와는 소수점 반올림 차이로 약간의 차이가 있습니다.
- 현재가 → 12개월 목표주가 상승여력: (191.88 - 182.70) / 182.70 × 100 = 5.0246% (약 5.02%)
  - 참고: 질문의 7.8% 수치와는 입력된 가격(182.70)과 목표가(191.88)를 기준으로 계산하면 약 5.02%가 맞습니다.

## 시각화 파일
- 생성된 이미지 파일: nvidia_price_plot.png
- 파일 위치: 현재 작업 디렉터리 (저장 완료)
- 마크다운 저장 모드 결정: 'w' (새 파일로 저장) — 새로운 리포트 파일을 생성하는 방식으로 저장하였습니다.

## 사용한 파이썬 코드 (재생성/수정 가능)
```python
from datetime import datetime
import matplotlib.pyplot as plt

# Data
dates = ["2025-08-05", "2025-08-06", "2025-08-07", "2025-08-08"]
prices = [178.26, 179.42, 180.77, 182.7]

# Convert to datetime for plotting
x = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

# Stats
start = prices[0]
end = prices[-1]
percent_change = (end - start) / start * 100
target_price = 191.88
to_target_pct = (target_price - end) / end * 100

# Plot
plt.figure(figsize=(10, 5))
plt.plot(x, prices, marker='o', linestyle='-', color='#1f77b4', linewidth=2)
plt.fill_between(x, prices, alpha=0.1, color='#1f77b4')

# Target price line
plt.axhline(target_price, color='green', linestyle='--', linewidth=1.5, label=f'12개월 목표가 ${target_price}')

# Annotations
plt.annotate(f'시작: ${start:.2f}', xy=(x[0], prices[0]), xytext=(-60, -30), textcoords='offset points')
plt.annotate(f'종가: ${end:.2f}\\n변동: {percent_change:.2f}%', xy=(x[-1], prices[-1]), xytext=(10, 10), textcoords='offset points')
plt.annotate(f'목표가까지: {to_target_pct:.2f}%', xy=(x[-1], prices[-1]), xytext=(10, -30), textcoords='offset points')

plt.title('NVIDIA (NVDA) 최근 4일 주가 추이 (2025-08-05 ~ 2025-08-08)')
plt.xlabel('날짜')
plt.ylabel('주가 (USD)')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig('nvidia_price_plot.png', dpi=150)
plt.close()
```

## 비고 및 다음 단계 제안
- 원하시면:
  - 그래프 스타일(색상, 폰트, 한글 폰트 포함) 조정
  - 일별 거래량이나 이동평균 추가
  - 인터랙티브 차트(Plotly)로 변환
  - 이미지 파일 직접 첨부 또는 인라인 표시
- 현재까지 외부 검색은 사용하지 않았습니다 (검색 횟수: 0/4).

필요하시면 그래프를 다른 포맷으로 저장하거나, 추가 지표를 포함해 재생성해 드리겠습니다.
