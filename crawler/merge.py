import pandas as pd
import os

def merge_jobs():
    # 각 파일 불러오기
    df_saramin = pd.read_csv("data/jobs_saramin.csv", encoding="utf-8-sig")
    df_wanted = pd.read_csv("data/jobs_wanted.csv", encoding="utf-8-sig")

    print(f"사람인 공고: {len(df_saramin)}개")
    print(f"원티드 공고: {len(df_wanted)}개")

    # 컬럼 통일 (사람인엔 condition이 있고 원티드엔 없음)
    df_saramin["condition"] = df_saramin.get("condition", "")
    df_wanted["condition"] = ""

    # 공통 컬럼만 사용
    cols = ["title", "company", "condition", "link", "source"]
    df_saramin = df_saramin[cols]
    df_wanted = df_wanted[cols]

    # 중복 제거 - 회사명+제목 기준, 사람인 우선
    # 사람인 먼저 쌓고, 원티드에서 중복 제거
    saramin_keys = set(
        df_saramin["company"].str.strip() + "|" + df_saramin["title"].str.strip()
    )

    df_wanted_dedup = df_wanted[
        ~(df_wanted["company"].str.strip() + "|" + df_wanted["title"].str.strip()).isin(saramin_keys)
    ]

    removed = len(df_wanted) - len(df_wanted_dedup)
    print(f"중복 제거된 원티드 공고: {removed}개")

    # 합치기
    df_all = pd.concat([df_saramin, df_wanted_dedup], ignore_index=True)
    print(f"최종 전체 공고: {len(df_all)}개")

    # 저장
    df_wanted_dedup.to_csv("data/jobs_wanted.csv", index=False, encoding="utf-8-sig")
    df_all.to_csv("data/jobs_all.csv", index=False, encoding="utf-8-sig")
    print("\n저장 완료!")
    print("  - data/jobs_saramin.csv (사람인)")
    print("  - data/jobs_wanted.csv (원티드, 중복제거)")
    print("  - data/jobs_all.csv (전체 합본)")

if __name__ == "__main__":
    merge_jobs()