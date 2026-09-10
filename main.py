import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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
# 그래프 1: 단일 영화 날짜별 일관객 변화
# ==================================================
st.header("1. 영화별 날짜별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")


fig1 = px.line(
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
fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
)

st.plotly_chart(
    fig1,
    use_container_width=True,
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.caption(
    "선택한 영화의 날짜별 일관객 변화를 "
    "시간의 흐름에 따라 확인할 수 있습니다."
)


# ==================================================
# 그래프 2: 누적 관객 TOP 5 영화 비교 (다중 선 그래프)
# ==================================================
st.divider()

st.header("2. 누적 관객 TOP 5 영화의 일별 관객수 변화 비교")

# 기간 내 누적 일관객 합계 상위 5개 영화 추출
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index
    .tolist()
)

# 상위 5개 영화 데이터 필터링 및 날짜 정렬
top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

# Plotly 다중 선 그래프 생성 (color 옵션으로 영화 구분)
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="누적 관객 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화 제목",
    },
)

# 툴팁 및 레이아웃 설정
fig2.update_traces(
    hovertemplate=(
        "영화명: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    legend_title_text="영화 목록",
)

st.plotly_chart(
    fig2,
    use_container_width=True,
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.caption(
    "해당 기간 동안 누적 관객 수가 가장 많았던 상위 5개 영화의 일별 관객 수 추이를 한눈에 비교할 수 있습니다. "
    "오른쪽 범례 항목을 클릭하면 특정 영화의 선을 켜거나 끌 수 있습니다."
)


# ==================================================
# 그래프 3: 일별 TOP 10 총관객 수 변화 (영역 그래프)
# ==================================================
st.divider()

st.header("3. 날짜별 TOP 10 영화 총 관객 수 변화 (영역 그래프)")

# 날짜별 일관객 합계 계산
daily_sum = (
    df.groupby("날짜")["일관객"]
    .sum()
    .reset_index()
    .sort_values("날짜")
)

# 영역 그래프 생성
fig3 = px.area(
    daily_sum,
    x="날짜",
    y="일관객",
    title="날짜별 TOP 10 영화 일관객 합계 변화",
    labels={
        "날짜": "날짜",
        "일관객": "TOP 10 일관객 합계",
    },
)

# 관객 수 합계 상위 3개 날짜 추출
top3_days = daily_sum.nlargest(3, "일관객")

# 상위 3일 포인트를 강조 강조 포인트로 추가
fig3.add_trace(
    go.Scatter(
        x=top3_days["날짜"],
        y=top3_days["일관객"],
        mode="markers",
        marker=dict(size=10, color="red"),
        name="관객 수 TOP 3일",
        hoverinfo="skip",
    )
)

# 상위 3개 날짜에 텍스트 주석(Annotation) 표시
for idx, row in top3_days.iterrows():
    date_str = row["날짜"].strftime("%Y-%m-%d")
    audience_cnt = f"{row['일관객']:,}명"
    
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=f"<b>{date_str}</b><br>({audience_cnt})",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        ax=0,
        ay=-40,
        font=dict(size=12, color="crimson"),
        bgcolor="white",
        bordercolor="red",
        borderwidth=1,
    )

fig3.update_traces(
    selector=dict(type="scatter", mode="lines"),
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "TOP 10 일관객 합계: %{y:,}명"
        "<extra></extra>"
    ),
)

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="TOP 10 일관객 합계",
)

st.plotly_chart(
    fig3,
    use_container_width=True,
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.caption(
    "날짜별 TOP 10 영화의 전체 관객 수 합계 변화를 영역 그래프 형태로 보여줍니다. "
    "붉은색으로 표시된 날짜는 해당 기간 중 전체 관객 동원력이 가장 높았던 상위 3일입니다."
)
