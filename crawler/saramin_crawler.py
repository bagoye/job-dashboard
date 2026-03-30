import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

IT_KEYWORDS = [
    "개발", "엔지니어", "engineer", "developer", "백엔드", "프론트엔드",
    "풀스택", "데이터", "data", "AI", "ML", "머신러닝", "딥러닝",
    "DevOps", "클라우드", "cloud", "Python", "Java", "iOS", "Android",
    "QA", "보안", "security", "DBA", "인프라", "서버", "SW", "software"
]

def fetch_saramin(pages=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }

    jobs = []

    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=개발자&recruitPage={page}&recruitSort=reg_dt&recruitPageCount=40"

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select(".item_recruit")

        if not items:
            print(f"  {page}페이지 데이터 없음, 종료")
            break

        for item in items:
            # 제목
            title_el = item.select_one(".job_tit a")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)

            # IT 키워드 필터링
            if not any(kw.lower() in title.lower() for kw in IT_KEYWORDS):
                continue

            # 회사명
            company_el = item.select_one(".corp_name a")
            company = company_el.get_text(strip=True) if company_el else ""

            # 링크
            link = "https://www.saramin.co.kr" + title_el.get("href", "")

            # 조건 (경력, 학력 등)
            conditions = item.select(".job_condition span")
            condition_text = " | ".join([c.get_text(strip=True) for c in conditions])

            jobs.append({
                "title": title,
                "company": company,
                "condition": condition_text,
                "link": link,
                "source": "사람인"
            })

        print(f"  {page}페이지 완료 (누적 {len(jobs)}개)")
        time.sleep(1)

    return pd.DataFrame(jobs)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    print("사람인 크롤링 중...")
    df = fetch_saramin(pages=5)
    print(f"\n총 {len(df)}개 IT 공고 저장 완료!")
    print(df.head(10))
    df.to_csv("data/jobs_saramin.csv", index=False, encoding="utf-8-sig")