import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# -----------------------------
# 1️⃣ Đọc danh sách keyword
# -----------------------------
def load_keywords(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        keywords = [line.strip().lower() for line in f if line.strip()]
    print(f"🔑 Đã load {len(keywords)} keyword.")
    return keywords

# -----------------------------
# 2️⃣ Đọc danh sách URL bài báo
# -----------------------------
def load_article_links(filepath):
    if filepath.endswith(".json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        urls = [item["link"] for item in data]
    elif filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
        urls = df["link"].dropna().tolist()
    else:
        raise ValueError("File phải là .json hoặc .csv")

    print(f"📰 Đã load {len(urls)} bài báo.")
    return urls

# -----------------------------
# 3️⃣ Hàm lấy nội dung bài báo
# -----------------------------
def get_article_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"⚠️ Không truy cập được: {url}")
            return ""
        soup = BeautifulSoup(resp.text, "html.parser")

        # Lấy phần nội dung chính
        paragraphs = soup.select("article p")
        text = " ".join(p.get_text(separator=" ", strip=True) for p in paragraphs)
        return text.lower()
    except Exception as e:
        print(f"⚠️ Lỗi khi đọc {url}: {e}")
        return ""

# -----------------------------
# 4️⃣ Đếm số lần keyword xuất hiện
# -----------------------------
def count_keywords_in_text(text, keywords):
    counts = {}
    for kw in keywords:
        # Regex để tìm chính xác từ, không phân biệt hoa thường
        pattern = r"\b" + re.escape(kw) + r"\b"
        counts[kw] = len(re.findall(pattern, text, flags=re.IGNORECASE))
    return counts

# -----------------------------
# 5️⃣ Chạy toàn bộ pipeline
# -----------------------------
def main():
    keyword_file = "keywords.txt"            # file chứa keyword (mỗi dòng 1 từ)
    article_file = "vnexpress_climate.json"  # file chứa danh sách bài báo
    output_file = "keyword_count.csv"

    keywords = load_keywords(keyword_file)
    urls = load_article_links(article_file)

    results = []

    for idx, url in enumerate(urls, start=1):
        print(f"📄 [{idx}/{len(urls)}] Đang xử lý: {url}")
        text = get_article_text(url)
        if not text:
            continue
        kw_counts = count_keywords_in_text(text, keywords)
        row = {"url": url, **kw_counts}
        results.append(row)

    # Xuất kết quả ra CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"\n✅ Hoàn tất! Kết quả được lưu vào '{output_file}' ({len(results)} bài).")

if __name__ == "__main__":
    main()
