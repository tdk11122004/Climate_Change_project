import requests
from bs4 import BeautifulSoup
import json
import time
import sys
import pandas as pd
import os

# Đảm bảo in tiếng Việt ra terminal không bị lỗi
sys.stdout.reconfigure(encoding='utf-8')

def crawl_topic_page(page=1):
    """
    Crawl 1 trang trong chủ đề 'Biến đổi khí hậu' từ VnExpress
    """
    base_url = "https://timkiem.vnexpress.net/?q=biến%20đổi%20khí%20hậu&media_type=all&fromdate=0&todate=0&latest=&cate_code=&search_f=title,tag_list&date_format=all&page="
    url = f"{base_url}{page}"
    print(f"> Truy cập: {url}")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print("   ❌ Lỗi khi truy cập:", resp.status_code)
        return None
    return BeautifulSoup(resp.text, "html.parser")

def parse_articles_from_page(soup):
    """
    Lấy danh sách bài báo từ 1 trang (chuẩn hóa link + bỏ trùng)
    """
    items = []
    seen_links = set()
    for tag in soup.find_all(["h2", "h3"], class_="title-news"):
        a = tag.find("a")
        if a and a.get("href"):
            link = a["href"].split("#")[0].strip()
            if link.startswith("/"):
                link = "https://vnexpress.net" + link
            if link not in seen_links:
                seen_links.add(link)
                title = a.get_text(strip=True)
                items.append({"title": title, "link": link})
    return items

def crawl_article_summary(article_url):
    """
    Vào từng bài để lấy phần mô tả đầu tiên
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(article_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return ""
        soup = BeautifulSoup(resp.text, "html.parser")
        desc = soup.find("p", class_="description")
        if desc:
            return desc.get_text(strip=True)
        p = soup.find("p")
        return p.get_text(strip=True) if p else ""
    except Exception as e:
        print("   ⚠️ Lỗi khi lấy nội dung:", e)
        return ""

def crawl_all_pages(max_pages=200, delay=0.5):
    """
    Crawl toàn bộ chủ đề từ trang 1 đến hết (tự dừng khi không còn bài)
    """
    all_articles = []
    seen = set()

    for page in range(1, max_pages + 1):
        soup = crawl_topic_page(page)
        if not soup:
            break

        articles = parse_articles_from_page(soup)
        if not articles:
            print(f"⚠️ Trang {page} không có bài nào, dừng.")
            break

        for art in articles:
            if art["link"] in seen:
                continue
            art["summary"] = crawl_article_summary(art["link"])
            all_articles.append(art)
            seen.add(art["link"])
            time.sleep(delay)

        time.sleep(delay)

    return all_articles

def main():
    print("🚀 Bắt đầu crawl chủ đề 'Biến đổi khí hậu'...\n")

    # Crawl toàn bộ
    data = crawl_all_pages(max_pages=200, delay=0.1)
    print(f"\n✅ Crawl xong, thu được {len(data)} bài!\n")

    # Lọc trùng toàn bộ (nếu có)
    unique_data = {item["link"]: item for item in data}
    data = list(unique_data.values())
    print(f"✅ Sau khi lọc trùng, còn lại {len(data)} bài duy nhất.")

    # Lưu ra JSON
    with open("vnexpress_climate.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Lưu ra CSV
    df = pd.DataFrame(data)
    df.to_csv("vnexpress_climate.csv", index=False, encoding="utf-8-sig")

    print("📄 Đã lưu dữ liệu vào 'vnexpress_climate.json' và 'vnexpress_climate.csv'.")
    print("🎯 Hoàn tất!")

if __name__ == "__main__":
    main()
