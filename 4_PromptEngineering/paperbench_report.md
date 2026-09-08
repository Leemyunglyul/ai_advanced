# PaperBench 실험 보고서

- 작성일: 2025-08-24
- 출처: OpenAI PaperBench (arXiv, GitHub), OpenAI 블로그, 보도자료 및 기술기사(Weigths & Biases, Medium 등)

---

## 1. 개요

PaperBench는 OpenAI가 제안한 벤치마크로, AI 에이전트들이 최신 ML 연구 논문(주로 ICML 2024의 Spotlight/Oral 논문 20편)을 "무에서부터" 재현(replicate)할 수 있는지를 평가합니다. 에이전트는 논문(마크다운+PDF)과 저자들이 제공한 추가설명(addendum)을 받고, 코드베이스를 직접 작성하고 reproduce.sh로 재현 스크립트를 만들어 결과를 깨끗한 환경에서 실행해 원래 논문의 실험 결과를 재생산해야 합니다.

주요 특징:
- 20편 논문, 총 8,316개의 세부 채점 기준(leaf nodes)으로 구성된 계층적 루브릭(rubric).
- 재현(reproduction) 단계: 제출된 repo의 reproduce.sh를 별도의 깨끗한 VM에서 실행해 산출물(reproduce.log, 결과 파일 등)을 생성.
- 채점: LLM 기반의 judge(주로 o3-mini 기반 SimpleJudge)를 사용해 각 leaf node를 0/1로 채점하고 가중평균을 냄.
- PaperBench Code-Dev: 실행/결과 확인 단계를 생략하고 코드 개발(Code Development) 노드만 채점하는 저비용 변형.

참고(원문): arXiv: https://arxiv.org/pdf/2504.01848
프로젝트 깃허브: https://github.com/openai/preparedness/tree/main/project/paperbench

---

## 2. 실험 설정(요약)

- 데이터셋: ICML 2024 Spotlight/Oral에서 선정된 20편 (저자와 협업하여 루브릭 제작)
- 에이전트 환경: Ubuntu 24.04 컨테이너, 인터넷 접근, A10 GPU (재현 단계에서 사용)
- 에이전트 스캐폴드: BasicAgent (ReAct 유사) 및 IterativeAgent(작업 종료 방지·단계적 유도)
- 채점자(Judge): SimpleJudge (o3-mini-high 권장), JudgeEval로 성능 검증
- 제한시간: 기본 12시간(실험에 따라 24h/36h 등 확장)

---

## 3. 평가 방식

- 루브릭: 각 논문별로 세부 조건을 계층적으로 분해. 최하위 leaf nodes는 코드 개발, 실행, 결과 일치 여부 등 유형으로 구분.
- 채점: 각 leaf는 0/1로 채점되고, 부모 노드는 자식의 가중평균으로 계산되어 루트 노드(논문)의 복제 점수 산출.
- 최종 지표: 20편에 대한 평균 Replication Score(%)
- Judge 신뢰성: JudgeEval에서 o3-mini를 사용한 SimpleJudge의 F1=0.83 보고

---

## 4. 주요 결과 (원문 요약)

아래 표는 OpenAI가 보고한 주요 모델 점수입니다 (BasicAgent 기준, 평균 Replication Score %):

| 모델 (설정) | 평균 Replication Score (%) |
|---:|---:|
| Claude 3.5 Sonnet (BasicAgent) | 21.0 ± 0.8 |
| o1 (BasicAgent, reasoning=high) | 13.2 ± 0.3 |
| DeepSeek-R1 (BasicAgent) | 6.0 ± 0.3 |
| GPT-4o (BasicAgent) | 4.1 ± 0.1 |
| Gemini 2.0 Flash (BasicAgent) | 3.2 ± 0.2 |
| o3-mini (BasicAgent) | 2.6 ± 0.2 |

IterativeAgent(종종 모델이 일찍 끝내지 않도록 강제하는 방식)를 사용했을 때의 일부 결과:
- o1 (IterativeAgent, 24h limit): 24.4 ± 0.7%
- o1 (IterativeAgent, 36h limit): 26.0 ± 0.3%
- o3-mini (IterativeAgent): 8.5 ± 0.8%
- Claude 3.5 Sonnet (IterativeAgent)은 일부 프롬프트에 민감하여 성능이 하락(16.1%)

PaperBench Code-Dev (코드 개발 노드만 채점):
- o1 (IterativeAgent): 43.4 ± 0.8% (Code-Dev 변형에서는 상대적으로 점수가 큼)

원문 README(깃허브)에도 동일한 leaderboard가 공개되어 있습니다.

---

## 5. 시각화 자료

### 5.1 상위 모델 막대그래프 (텍스트 기반 간단 시각화)

(막대 길이는 상대값이며 읽기 편의를 위해 0--30% 범위로 정규화)

Claude 3.5 Sonnet | ████████████████████ 21.0%
O1 (basic)       | ███████████ 13.2%
O1 (iterative 36h)| █████████████ 26.0% (iterative, extended)
DeepSeek-R1       | ████ 6.0%
GPT-4o            | █ 4.1%
Gemini 2.0 Flash  | █ 3.2%
O3-mini           | █ 2.6%

(참고: PaperBench Code-Dev에서 o1 IterativeAgent는 43.4%를 기록 — Code-Dev는 실행/결과검증을 제외한 코드 품질 중심 평가)

### 5.2 요약 표(재차)

- 최고 성능 모델(공식 실험, BasicAgent): Claude 3.5 Sonnet — 21.0%
- IterativeAgent 튜닝으로 o1 점수 상승: 최대 26.0%(36시간 한도)
- 인간(ML PhD) 베이스라인: 4-paper subset에서 best-of-3 평균 41.4%(48시간)

---

## 6. 해석 및 시사점

1. 현재의 최첨단 LLM/에이전트들은 "논문을 읽고, 설계하고, 코드로 구현하고, 실험을 완전히 재현하는" 장기적·공학적 작업에서 여전히 인간에 비해 크게 뒤처집니다. 최고 모델도 평균 21% 수준입니다.
2. 모델 성능은 단순 능력 차이뿐 아니라 에이전트 프롬프트/스캐폴딩(예: IterativeAgent)과 시간 한도에 민감합니다. 적절한 스캐폴드만으로도 o1 점수가 크게 올라감.
3. Code-Dev 변형이 제시하는 높은 점수(예: o1 43.4%)는 "코드를 잘 작성하는지"를 평가하지만, 실제 재현(실행·결과 일치)까지는 장담하지 못합니다. 즉, 코드 작성 능력은 있되 통합·실행·디버깅에 약함.
4. 비용·시간 문제: 전체 PaperBench 평가는 비용·인프라(평가용 GPU, LLM 토큰 비용 등) 소모가 큼. OpenAI는 채점 비용을 낮추기 위해 Code-Dev와 pruned-grading 등 기법을 실험함.

---

## 7. 업데이트(2025-08-24 기준)

제가 확인한 공개 자료(원문 arXiv, OpenAI GitHub repo 및 OpenAI 페이지, 보도자료/기사들)는 2025년 4월 초 발표 이후 다음과 같은 주요 추가/명확화가 있음을 보여줍니다:

- 깃허브 공개: OpenAI preparedness 저장소 내 project/paperbench 경로에 code, 데이터셋, 루브릭 및 leaderboard가 공개되어 있어 누구나 로컬에서 재현 가능(README와 leaderboard 포함).
- IterativeAgent와 Code-Dev 변형이 공개되어 있으며, IterativeAgent가 특정 모델에 대해 성능을 올리는 사례(o1) 보고.
- Judge(평가자) 성능 관련 보완: JudgeEval로 자동화 judge의 성능을 측정했고 o3-mini 기반 SimpleJudge가 F1≈0.83을 달성했다고 보고됨.
- 비용 절감 시도: grading pruning, Code-Dev, 더 저렴한 judge 모델 등 여러 접근을 통해 비용을 낮추려는 시도가 깃허브 문서에 설명되어 있음.

현재(2025-08-24)까지 발표된 문헌/깃허브에서 "PaperBench 자체의 추가 논문 버전(예: PaperBench v2)", 또는 데이터셋 확장(20편 → 더 큰 셋) 같은 대형 업데이트는 확인되지 않았습니다. 다만 프로젝트가 오픈소스로 공개되어 있어 커뮤니티 기여/포크를 통해 발전 가능성은 열려 있습니다.

---

## 8. 참고 링크

- arXiv (원문): https://arxiv.org/pdf/2504.01848
- GitHub (OpenAI Preparedness / PaperBench): https://github.com/openai/preparedness/tree/main/project/paperbench
- OpenAI 공식 페이지: https://openai.com/index/paperbench/
- Weights & Biases 및 다수 기사(요약/해설): WandB, Medium, 뉴스 기사들

---

## 9. 결론(한 문장)

PaperBench는 "AI가 연구를 자율적으로 재현할 수 있는가"를 엄격하게 측정하는 중요한 벤치마크이며, 2025년 초 기준 최고 모델(Claude 3.5 Sonnet)도 평균 21%로 인간 수준(주어진 평가 절차·시간 기준)에는 아직 미치지 못합니다. 다만 프롬프트/스캐폴딩·평가 방식의 변화로 단기간 내 성능 향상이 가능함을 보여주었습니다.


---

(이 보고서는 PaperBench의 공개 자료(arXiv, GitHub, OpenAI 문서, 보도자료)를 바탕으로 작성되었습니다. 추가로 시각화 이미지나 표를 원하시면 알려주십시오.)
