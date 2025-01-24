import streamlit as st
import pandas as pd
import koreanize_matplotlib  # 한글 폰트 지원
import plotly.express as px

# 데이터 경로
DATA_PATH = "daily_temp.csv"

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_and_clean_data(path):
    data = pd.read_csv(path)
    # 날짜 열의 공백 제거 및 날짜 형식 변환
    data['날짜'] = pd.to_datetime(data['날짜'].str.strip(), format="%Y-%m-%d", errors='coerce')
    # 월 열 추가
    data['월'] = data['날짜'].dt.month
    # 결측치 처리
    data = data.dropna(subset=['평균기온(℃)'])
    return data

# 데이터 로드
data = load_and_clean_data(DATA_PATH)

# 제목과 설명 추가
st.title("12달의 기온 분포 인터랙티브 그래프")
st.write("12달의 평균 기온 분포를 한눈에 확인하세요. 그래프는 상호작용이 가능합니다.")

# 인터랙티브 박스플롯 생성
fig = px.box(
    data,
    x="월",  # X축: 월
    y="평균기온(℃)",  # Y축: 평균 기온
    points="all",  # 데이터 포인트 표시
    title="12달의 평균 기온 분포",
    labels={"평균기온(℃)": "기온 (℃)", "월": "월별"},
    template="plotly_white"  # 깔끔한 테마
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
