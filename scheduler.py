# scheduler.py 만들어서
import schedule, time
from crawler.saramin_crawler import fetch_saramin
from crawler.job_crawler import fetch_wanted
from crawler.news_crawler import fetch_geek_news
from crawler.merge import merge_jobs
import pandas as pd, os

def run_all():
    print("자동 수집 시작...")
    os.makedirs("data", exist_ok=True)
    fetch_saramin(pages=5).to_csv("data/jobs_saramin.csv", index=False, encoding="utf-8-sig")
    fetch_wanted(total=500).to_csv("data/jobs_wanted.csv", index=False, encoding="utf-8-sig")
    fetch_geek_news().to_csv("data/news.csv", index=False, encoding="utf-8-sig")
    merge_jobs()
    print("완료!")

schedule.every().day.at("09:00").do(run_all)
while True:
    schedule.run_pending()
    time.sleep(60)