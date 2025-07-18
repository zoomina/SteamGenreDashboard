# 🎮 Steam Genre Dashboard

**Streamlit 기반의 스팀 게임 장르 분석 대시보드**

> 2018년부터 2020년까지의 Steam 게임 유저 수 추정 데이터를 활용하여,  
> 장르별 유저 분포, 시장 점유율, 시간대별 활동, 트렌드 패턴 등을 시각화한 대시보드입니다.

---

## 데이터 정보

- **출처**: [Mendeley Data - Steam Game Dataset](https://data.mendeley.com/datasets/ycy3sy3vj2/1)
- **데이터 설명**:
  - 상위 1,000개 게임의 **5분 간격 플레이어 수(Player Count)** 기록
  - **2017-12-14 ~ 2020-08-12** 기간 동안의 시간대별 유저 수 포함
  - 게임별 `UTC timestamp`, 플레이어 수, 가격 이력, 제작사, 장르, 지원 언어 등 다양한 **메타데이터 포함**
  - 데이터 수집 경로: **SteamDB 그래프** 및 **Steamworks API**

---

## 분석 주제

> **장르 단위의 유저 패턴 분석**

- 장르별 유저 수 추이 및 이상치 감지
- 장르별 시장 점유율, 언어/제작사 분포
- 요일 및 시간대별 사용자 활동 패턴
- 장르별 트렌드 및 클러스터링 (DTW 기반)
- 시장 독점도(HHI) 분석

---

## 대시보드 기능

대시보드는 두 개의 탭으로 구성되어 있습니다:

### 1. 전체 장르 오버뷰
> 모든 장르를 기준으로 유저 패턴을 통합 분석하는 페이지

- **장르별 색상 범례**
- **장르별 주간 전체 유저 수 및 이상치 탐지**
- **장르 점유율 분석** (도넛 차트):
  - 게임 수 기준
  - 유저 수 기준
  - 언어 비중
  - 제작사 비중
- **요일/시간대별 사용자 비율 (heatmap)**
- **시장 집중도 (HHI) 추이**
- **장르별 점유율 Top 5 게임 시각화**
- **장르별 트렌드 클러스터링 (기울기 vs peak timing)**

---

### 2. 장르별 대시보드
> 특정 장르를 선택해 세부 분석하는 페이지

- 여러 장르를 선택한 뒤, 하단에서 특정 장르 하나를 선택해 상세 보기 가능
- **주간 유저 수 및 이상치 시계열**
- **시장 독점도(HHI) 변화 추이**
- **언어별 / 제작사별 점유율**
- **요일-시간대별 사용자 활동 Heatmap**
- **장르별 점유율 상위 5개 게임의 월간 추이 (Stacked Bar)**

---

## 실행 방법

```bash
# 라이브러리 설치
pip install -r requirements.txt

# Streamlit 실행
streamlit run app.py
