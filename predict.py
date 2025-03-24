import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import streamlit as st

# 한글 폰트 설정 (윈도우용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 엑셀 파일 불러오기 (공백 포함된 이름 주의!)
df = pd.read_excel('sales_data .xlsx', engine='openpyxl')

# 2. 전처리 - 공백제거, NaN 제거
df['제품명'] = df['제품명'].astype(str).str.strip()
df = df.dropna()

# 3. 월을 날짜로 변환 후 숫자로 추출
df['월'] = pd.to_datetime(df['월'], errors='coerce')
df['월숫자'] = df['월'].dt.month
df = df.dropna()

# 4. Streamlit 앱 시작
st.title('제품명 입력 기반 판매량 예측 앱')

# 사용자로부터 제품명 입력받기
user_input = st.text_input('예측할 제품명을 입력하세요 (예: 김치, 계란, 우유 등)')

if user_input:
    # 입력된 제품명 기준으로 필터링
    selected_df = df[df['제품명'] == user_input.strip()]

    if not selected_df.empty:
        # X = 월, y = 판매량
        X = selected_df[['월숫자']]
        y = selected_df['판매량']

        # 선형 회귀 모델 학습
        model = LinearRegression()
        model.fit(X, y)

        # 1~12월 예측
        future_months = pd.DataFrame({'월숫자': list(range(1, 13))})
        predictions = model.predict(future_months)

        # 예측 결과 출력
        st.subheader(f"'{user_input}' 월별 예측 판매량")
        for m, p in zip(range(1, 13), predictions):
            st.write(f"{m}월: {int(p)}개")

        # 그래프 출력
        fig, ax = plt.subplots()
        ax.scatter(X, y, label='실제 판매량')
        ax.plot(future_months['월숫자'], predictions, color='red', label='예측 추세선')
        ax.set_title(f"{user_input} 월별 판매량 예측")
        ax.set_xlabel("월")
        ax.set_ylabel("판매량")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    else:
        st.warning(f"'{user_input}'에 대한 데이터를 찾을 수 없습니다.")
