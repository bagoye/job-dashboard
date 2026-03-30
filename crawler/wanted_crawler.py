import requests
import pandas as pd
import os
import time

IT_KEYWORDS = [
    "개발", "엔지니어", "engineer", "developer", "백엔드", "프론트엔드",
    "풀스택", "데이터", "data", "AI", "ML", "머신러닝", "딥러닝",
    "DevOps", "클라우드", "cloud", "Python", "Java", "iOS", "Android",
    "QA", "보안", "security", "DBA", "인프라", "서버", "SW", "software"
]

def fetch_wanted(total=500):
    url = "https://www.wanted.co.kr/api/v4/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "wanted-user-language": "ko",
    }

    jobs = []
    offset = 0
    limit = 100  # 한 번에 100개씩

    while offset < total:
        params = {
            "country": "kr",
            "job_sort": "job.latest_order",
            "limit": limit,
            "offset": offset,
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        items = data.get("data", [])

        if not items:  # 더 이상 데이터 없으면 종료
            break

        for item in items:
            company = item.get("company", {})
            position = item.get("position", {})
            title = position.get("name") if isinstance(position, dict) else str(item.get("position", ""))

            if not any(kw.lower() in title.lower() for kw in IT_KEYWORDS):
                continue

            jobs.append({
                "title": title,
                "company": company.get("name"),
                "industry": company.get("industry_name"),
                "link": f"https://www.wanted.co.kr/wd/{item.get('id')}",
                "source": "원티드"
            })

        print(f"  {offset + limit}개 수집 완료... (IT 공고 {len(jobs)}개)")
        offset += limit
        time.sleep(1)  # 서버 부하 방지

    return pd.DataFrame(jobs)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    print("원티드 IT 직군 크롤링 중...")
    df = fetch_wanted(total=500)
    print(f"\n총 {len(df)}개 IT 공고 저장 완료!")
    print(df.head(10))
    df.to_csv("data/jobs_wanted.csv", index=False, encoding="utf-8-sig")