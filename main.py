import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 1 - 시간")
st.write(
    "KOBIS 일별 박스오피스 데이터를 이용해 "
    "영화의 시간에 따른 관객 변화를 살펴봅니다."
)


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

    # 날짜 열을 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
    )

    return df


df = load_data()


# ==================================================
# 데이터 확인
# ==================================================
with st.expander("데이터 확인하기"):
    st.dataframe(
        df,
        use_container_width=True,
    )


# ==================================================
# 그래프 1
# ==================================================
st.header("1. 영화별 날짜별 일관객 변화")

movie_list = sorted(
    df["영화명"].dropna().unique()
)

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


# 마우스를 올렸을 때 날짜와 관객 수 표시
fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
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


# 그래프 설명 문구
st.markdown("**이 그래프로 알 수 있는 것**")
st.caption(
    "선택한 영화의 날짜별 일관객 변화를 "
    "시간의 흐름에 따라 확인할 수 있습니다."
)


# ==================================================
# 그래프 2
# ==================================================
st.divider()

st.header("2. 다음 그래프")

st.info(
    "여기에 두 번째 그래프를 추가할 예정입니다."
)


# ==================================================
# 그래프 3
# ==================================================
st.divider()

st.header("3. 다음 그래프")

st.info(
    "여기에 세 번째 그래프를 추가할 예정입니다."
)


