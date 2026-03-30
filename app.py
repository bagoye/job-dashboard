import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="IT 채용 대시보드", layout="wide")

TECH_KEYWORDS = [
    "Python", "Java", "JavaScript", "TypeScript", "React", "Node.js",
    "Spring", "FastAPI", "Django", "Flask", "Kotlin", "Swift", "iOS",
    "Android", "AWS", "GCP", "Azure", "Docker", "Kubernetes", "DevOps",
    "AI", "ML", "딥러닝", "머신러닝", "LLM", "데이터", "SQL", "NoSQL",
    "백엔드", "프론트엔드", "풀스택", "보안", "QA", "인프라", "클라우드"
]

@st.cache_data
def load_data():
    jobs = pd.read_csv("data/jobs_all.csv", encoding="utf-8-sig")
    news = pd.read_csv("data/news.csv", encoding="utf-8-sig")
    return jobs, news

def extract_keywords(texts):
    counter = Counter()
    for text in texts:
        if pd.isna(text):
            continue
        for kw in TECH_KEYWORDS:
            if kw.lower() in str(text).lower():
                counter[kw] += 1
    return counter

jobs, news = load_data()

# 사이드바
st.sidebar.title("필터")
search = st.sidebar.text_input("🔍 검색", placeholder="회사명 또는 공고명 입력")
source_filter = st.sidebar.multiselect(
    "출처",
    options=jobs["source"].unique().tolist(),
    default=jobs["source"].unique().tolist()
)

# 키워드 클릭 필터링 상태
if "keyword_filter" not in st.session_state:
    st.session_state.keyword_filter = None

if st.sidebar.button("🔄 키워드 필터 초기화"):
    st.session_state.keyword_filter = None

if st.session_state.keyword_filter:
    st.sidebar.info(f"키워드 필터: **{st.session_state.keyword_filter}**")

# 데이터 필터링
filtered = jobs[jobs["source"].isin(source_filter)]

if search:
    filtered = filtered[
        filtered["title"].str.contains(search, case=False, na=False) |
        filtered["company"].str.contains(search, case=False, na=False)
    ]

if st.session_state.keyword_filter:
    filtered = filtered[
        filtered["title"].str.contains(st.session_state.keyword_filter, case=False, na=False)
    ]

# 탭
tab1, tab2 = st.tabs(["📊 채용 분석", "📰 IT 뉴스"])

with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 공고 수", len(filtered))
    col2.metric("사람인", len(filtered[filtered["source"] == "사람인"]))
    col3.metric("원티드", len(filtered[filtered["source"] == "원티드"]))

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🔧 기술 키워드 Top 15")
        st.caption("키워드를 클릭하면 해당 공고만 필터링돼요")
        kw_counter = extract_keywords(filtered["title"])
        kw_df = pd.DataFrame(kw_counter.most_common(15), columns=["키워드", "빈도"])

        # 키워드 버튼
        cols = st.columns(5)
        for i, row in kw_df.iterrows():
            with cols[i % 5]:
                if st.button(f"{row['키워드']} ({row['빈도']})", key=f"kw_{row['키워드']}"):
                    st.session_state.keyword_filter = row['키워드']
                    st.rerun()

        st.bar_chart(kw_df.set_index("키워드"))

    with col_right:
        st.subheader("🏢 출처별 공고 수")
        source_counts = filtered["source"].value_counts().reset_index()
        source_counts.columns = ["출처", "공고 수"]
        st.bar_chart(source_counts.set_index("출처"))

    st.divider()
    st.subheader(f"📋 공고 목록 ({len(filtered)}개)")

    # 링크 버튼 포함 테이블
    for _, row in filtered.iterrows():
        c1, c2, c3, c4 = st.columns([4, 2, 1, 1])
        c1.write(row["title"])
        c2.write(row["company"] if pd.notna(row["company"]) else "")
        c3.write(row["source"])
        c4.link_button("🔗 보기", row["link"])

with tab2:
    st.subheader("📰 최신 IT 뉴스")
    st.metric("수집된 기사 수", len(news))
    st.divider()

    # 카드형 뉴스
    for i in range(0, len(news), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(news):
                break
            row = news.iloc[idx]
            with col:
                with st.container(border=True):
                    st.markdown(f"**{row['title']}**")
                    st.caption(f"📅 {str(row['published_at'])[:10]} | {row['source']}")
                    st.link_button("기사 보기 →", row["link"])