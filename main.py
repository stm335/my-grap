# ==================================================
# 그래프 2
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

# 그래프 설명 문구
st.markdown("**이 그래프로 알 수 있는 것**")
st.caption(
    "해당 기간 동안 누적 관객 수가 가장 많았던 상위 5개 영화의 일별 관객 수 추이를 한눈에 비교할 수 있습니다. "
    "범례 항목을 클릭하면 특정 영화의 선을 켜거나 끌 수 있습니다."
)
