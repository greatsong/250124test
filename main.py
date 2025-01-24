import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 한글 폰트 지원

# 데이터 경로
DATA_PATH = "daily_temp.csv"

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_and_clean_data(path):
    data = pd.read_csv(path)
    # 1. 날짜 열의 공백 제거 및 날짜 형식 변환
    data['날짜'] = pd.to_datetime(data['날짜'].str.strip(), format="%Y-%m-%d", errors='coerce')
    
    # 2. 월 열 추가
    data['월'] = data['날짜'].dt.month
    
    # 3. 결측치 처리 (평균기온이 없는 행 제거)
    data = data.dropna(subset=['평균기온(℃)'])
    
    return data

# 데이터 로드
data = load_and_clean_data(DATA_PATH)

# 제목과 설명 추가
st.title("월별 기온 분포 박스플롯")
st.write("월을 선택하면 해당 월의 평균 기온 분포를 박스플롯으로 확인할 수 있습니다.")

# 월 선택 위젯
selected_month = st.selectbox("월을 선택하세요:", sorted(data['월'].dropna().unique()))

# 선택한 월의 데이터 필터링
month_data = data[data['월'] == selected_month]

# 박스플롯 그리기
if not month_data.empty:
    fig, ax = plt.subplots(figsize=(8, 5))  # 그래프 크기 조정
    ax.boxplot(month_data['평균기온(℃)'], vert=True, patch_artist=True, labels=[f"{selected_month}월"])
    ax.set_title(f"{selected_month}월의 평균 기온 분포", fontsize=14)
    ax.set_ylabel("기온 (℃)", fontsize=12)
    st.pyplot(fig)  # Streamlit에서 그래프 출력
else:
    st.warning("선택한 월에 해당하는 데이터가 없습니다.")
