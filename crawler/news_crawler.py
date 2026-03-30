import requests
import xml.etree.ElementTree as ET
import pandas as pd

def fetch_geek_news():
    url = "https://news.hada.io/rss/news"  # URL 수정
    response = requests.get(url)
    response.encoding = "utf-8"

    root = ET.fromstring(response.content)

    # Atom 형식이라 네임스페이스 처리 필요
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    articles = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", namespaces=ns)
        link_el = entry.find("atom:link", ns)
        link = link_el.get("href") if link_el is not None else ""
        published = entry.findtext("atom:published", namespaces=ns)
        articles.append({
            "title": title,
            "link": link,
            "published_at": published,
            "source": "GeekNews"
        })

    return pd.DataFrame(articles)

if __name__ == "__main__":
    df = fetch_geek_news()
    print(df.head())
    df.to_csv("data/news.csv", index=False, encoding="utf-8-sig")
    print(f"\n총 {len(df)}개 기사 저장 완료!")