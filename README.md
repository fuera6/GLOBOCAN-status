# GLOBOCAN_tool
GLOBOCAN 트렌드 분석 툴과 논문 현황 정리

## Usage
* GLOBOCAN CANCER OVER TIME을 이용한 트렌드 분석 툴
* CI5 Plus를 이용한 트렌드 분석 툴
* GLOBOCAN과 CI5 Plus를 이용한 논문 현황 정리

## Time
* 2024.07

## Directories & Files
* CANCER OVER TIME trend
  * CANCER OVER TIME crolling.py: CANCER OVER TIME에서 데이터를 크롤링해서 longterm age-standardized rate와 age-specific rate를 구하는 코드
  * CANCER OVER TIME age-standardized shortterm.py: CANCER OVER TIME crolling.py를 돌려서 나온 *_age-standardized rate_trend.csv 파일을 이용해 최근 연속된 n년간의 데이터만 추출하는 코드
  * CANCER OVER TIME age-specific shortterm.py: CANCER OVER TIME crolling.py를 돌려서 나온 *_age-specific rate_trend.csv 파일을 이용해 최근 연속된 n년간의 데이터만 추출하는 코드
  * CANCER OVER TIME table maker.py: Joinpoint를 돌려서 나온 결과를 이용해 manuscript용 테이블을 만드는 코드
  * CANCER OVER TIME 참고자료.xlsx: CANCER OVER TIME에 등록되어 있는 cancer ID, 국가 데이터 정리본
* CI5 Plus trend
  * longterm trend.py: CI5plus_Detailed_Legacy 또는 CI5plus_Summary_Legacy에서 age-standardized incidence rate를 구하는 코드
  * shortterm trend.py: CI5plus_Detailed_Legacy 또는 CI5plus_Summary_Legacy에서 최근 연속된 n년간의 age-standardized incidence rate를 구하는 코드
  * longterm trend_graph.py: longterm trend.py를 돌려서 나온 longterm_trend.csv 파일을 이용해 국가별 트렌드 그래프를 그리는 코드
  * longterm trend_table.py: Joinpoint를 돌려서 나온 결과를 이용해 manuscript용 테이블을 만드는 코드
  * CI5 Plus 참고자료.xlsx: CI5 Plus에 등록되어 있는 cancer ID, 국가 데이터 정리본
* GLOBOCAN 현황.xlsx: GLOBOCAN 논문 현황 정리 파일
