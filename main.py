import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")
st.write("KOBIS 일별 박스오피스 데이터를 이용해 영화의 시간에 따른 관객 변화를 살펴봅니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜 타입으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
    )

    return df


df = load_data()


# --------------------------------------------------
# 데이터 미리보기
# --------------------------------------------------
with st.expander("데이터 확인하기"):
    st.dataframe(df, use_container_width=True)


# ==================================================
# 그래프 1. 영화별 날짜별 일관객 변화
# ==================================================
st.header("1. 영화별 날짜별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
)


fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.caption("선택한 영화의 날짜별 일관객 변화를 시간의 흐름에 따라 확인할 수 있습니다.")


# ==================================================
# 앞으로 추가할 그래프 영역
# ==================================================
st.divider()

st.header("2. 다음 그래프")
st.info("여기에 두 번째 그래프를 추가하세요.")

# 예:
# st.subheader("2.1 영화별 누적관객 변화")
# ...
# st.caption("이 그래프로 알 수 있는 것: ...")


st.header("3. 다음 그래프")
st.info("여기에 세 번째 그래프를 추가하세요.")

# 예:
# st.subheader("3.1 영화별 스크린 수 변화")
# ...
# st.caption("이 그래프로 알 수 있는 것: ...")

streamlit
pandas
plotly


이 구성에서는 pd.to_datetime(..., format="%Y%m%d")로 20240101 같은 날짜를 실제 날짜 데이터로 변환하고, Plotly의 hover 설정으로 마우스를 올렸을 때 날짜와 일관객 수가 표시되도록 했습니다. @st.cache_data도 넣어서 데이터를 매번 다시 다운로드하지 않도록 했습니다.
