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
    "달마다(시간마다) 관객의 수가 어떻게 변해왔는지 "
    "한눈에 알기가 쉽다."
)


# ==================================================
# 그래프 2: 누적 관객 TOP 5 영화 비교
# ==================================================
st.divider()

st.header(
    "2. 누적 관객 TOP 5 영화의 일별 관객수 변화 비교"
)

# 기간 내 누적 일관객 합계 상위 5개 영화 추출
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index
    .tolist()
)

# 상위 5개 영화 데이터 필터링 및 날짜 정렬
top5_df = (
    df[df["영화명"].isin(top5_movies)]
    .sort_values("날짜")
)


# Plotly 다중 선 그래프 생성
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

# 툴팁 설정
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
    "누적관객 5위의 영화의 관객 변화를 한눈에 볼 수 있다."
)


# ==================================================
# 그래프 3: 일별 TOP 10 총관객 수 변화
# ==================================================
st.divider()

st.header(
    "3. 날짜별 TOP 10 영화 총 관객 수 변화 (영역 그래프)"
)

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
top3_days = daily_sum.nlargest(
    3,
    "일관객",
)

# 상위 3일 포인트 강조
fig3.add_trace(
    go.Scatter(
        x=top3_days["날짜"],
        y=top3_days["일관객"],
        mode="markers",
        marker=dict(
            size=10,
            color="red",
        ),
        name="관객 수 TOP 3일",
        hoverinfo="skip",
    )
)

# 상위 3개 날짜에 텍스트 주석 표시
for idx, row in top3_days.iterrows():

    date_str = row["날짜"].strftime(
        "%Y-%m-%d"
    )

    audience_cnt = f"{row['일관객']:,}명"

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"<b>{date_str}</b>"
            f"<br>({audience_cnt})"
        ),
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        ax=0,
        ay=-40,
        font=dict(
            size=12,
            color="crimson",
        ),
        bgcolor="white",
        bordercolor="red",
        borderwidth=1,
    )

# 영역 그래프의 hover 설정
fig3.update_traces(
    selector=dict(
        type="scatter",
        mode="lines",
    ),
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
    "날짜별 10위 영화의 총 관객수의 합이므로 "
    "특정 날짜에 얼마나 관객이 몰렸는지 알 수 있다."
)


# ==================================================
# 그래프 4: 누적 관객 TOP 10 영화
# ==================================================
st.divider()

st.header("4. 기간 내 누적 관객 TOP 10 영화")

# 영화별 총 관객 수 및 10위권 진입 날수 집계
top10_movies_df = (
    df.groupby("영화명")
    .agg(
        누적관객=("일관객", "sum"),
        진입일수=("날짜", "nunique"),
    )
    .reset_index()
    .nlargest(
        10,
        "누적관객",
    )
    .sort_values(
        "누적관객",
        ascending=True,
    )
)


# Plotly 가로 막대그래프 생성
fig4 = px.bar(
    top10_movies_df,
    x="누적관객",
    y="영화명",
    orientation="h",
    title="기간 내 누적 관객 수 TOP 10",
    labels={
        "누적관객": "총 관객 수 (명)",
        "영화명": "영화 제목",
    },
    hover_data={
        "진입일수": True,
        "누적관객": ":,",
    },
)

# 툴팁 설정
fig4.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "총 누적관객: %{x:,}명<br>"
        "10위권 진입일수: %{customdata[0]}일"
        "<extra></extra>"
    ),
    customdata=top10_movies_df[
        ["진입일수"]
    ].values,
    marker_color="teal",
)

fig4.update_layout(
    xaxis_title="총 누적관객 수 (명)",
    yaxis_title="영화 제목",
)

st.plotly_chart(
    fig4,
    use_container_width=True,
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.caption(
    "총 기간에 얼마나 특정 영화를 많이 본 건지 "
    "다른 영화와 비교하기가 쉽다."
)


# ==================================================
# 그래프 5: 월 × 요일별 일관객 합계
# ==================================================
st.divider()

st.header("5. 월 × 요일별 일관객 합계")

# --------------------------------------------------
# 날짜에서 월과 요일 추출
# --------------------------------------------------
heatmap_df = df.copy()

# 월 추출
heatmap_df["월"] = (
    heatmap_df["날짜"].dt.month
)

# 요일 순서
# pandas의 dayofweek:
# 월요일=0, 화요일=1, ..., 일요일=6
weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

weekday_map = dict(
    enumerate(weekday_order)
)

# 요일 추출
heatmap_df["요일"] = (
    heatmap_df["날짜"]
    .dt.dayofweek
    .map(weekday_map)
)


# --------------------------------------------------
# 월 × 요일별 일관객 합계 계산
# --------------------------------------------------
monthly_weekday_sum = (
    heatmap_df
    .groupby(
        ["월", "요일"]
    )["일관객"]
    .sum()
    .reset_index()
)


# --------------------------------------------------
# 히트맵용 피벗 테이블 생성
# --------------------------------------------------
heatmap_pivot = (
    monthly_weekday_sum
    .pivot(
        index="월",
        columns="요일",
        values="일관객",
    )
    .reindex(
        columns=weekday_order
    )
    .fillna(0)
)


# --------------------------------------------------
# 히트맵 생성
# --------------------------------------------------
fig5 = go.Figure(
    data=go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns,
        y=[
            f"{month}월"
            for month in heatmap_pivot.index
        ],
        colorscale="Blues",
        colorbar=dict(
            title="일관객 합계",
        ),
        hovertemplate=(
            "월: %{y}"
            "<br>요일: %{x}"
            "<br>일관객 합계: %{z:,}명"
            "<extra></extra>"
        ),
    )
)


fig5.update_layout(
    title="월 × 요일별 일관객 합계",
    xaxis_title="요일",
    yaxis_title="월",
)


st.plotly_chart(
    fig5,
    use_container_width=True,
)


st.markdown("**이 그래프로 알 수 있는 것**")
st.caption(
    "특정 달의 특정 요일에 얼마나 사람이 몰렸는지 "
    "한눈에 볼 수 있다."
)
