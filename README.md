🌦️ VnExpress Climate Change Data Crawler and Keyword Analyzer

This project automatically collects and analyzes news articles related to climate change from VnExpress.net, one of Vietnam’s largest online newspapers.
It consists of two main parts:

Crawler: Fetches all articles in the topic “Biến đổi khí hậu (Climate Change)” using VnExpress’s internal JSON API.

Keyword Counter: Reads a list of user-defined keywords and counts their occurrences within each article, exporting results to a structured CSV table.

📁 Project Structure
```
📦 Climate_Change_Project/
│
├── main.py                       # Crawl all climate change articles via JSON API
├── keyword_count.py              # Count keyword occurrences in each article
│
├── vnexpress_climate.json        # Output from crawler (article list)
├── vnexpress_climate.csv         # Output from crawler (same data, CSV format)
│
├── keywords.txt                  # List of keywords (one per line)
└── keyword_count.csv             # Output from analyzer (table of counts)
```

🚀 Features

Full automatic crawling via VnExpress’s hidden API endpoint (/microservice/topic/...)

Duplicate-free dataset (URL normalization & deduplication logic)

Accurate text extraction using BeautifulSoup

Keyword frequency analysis (case-insensitive, regex-based matching)

Export results in .json and .csv formats

Works entirely offline after crawling — perfect for data analysis or NLP tasks



🧭 Usage Guide
Step 1 — Crawl VnExpress Climate Change Articles

Run:

python main.py


The script will automatically crawl up to 200 pages of the topic:
https://timkiem.vnexpress.net/?q=biến%20đổi%20khí%20hậu&media_type=all&fromdate=0&todate=0&latest=&cate_code=&search_f=title,tag_list&date_format=all&page=

Data will be saved as:
vnexpress_climate.json
vnexpress_climate.csv

Example log:
> Accessing: https://timkiem.vnexpress.net/?q=biến%20đổi%20khí%20hậu&media_type=all&fromdate=0&todate=0&latest=&cate_code=&search_f=title,tag_list&date_format=all&page=1
> Accessing: https://timkiem.vnexpress.net/?q=biến%20đổi%20khí%20hậu&media_type=all&fromdate=0&todate=0&latest=&cate_code=&search_f=title,tag_list&date_format=all&page=2


Step 2 — Prepare Keywords

Create a simple text file named keywords.txt:

Step 3 — Count Keywords in Articles

Run:

python keyword_counter.py


The script will:

Read all URLs from vnexpress_climate.json
Fetch and process each article’s text
Count how often each keyword appears
Export the result as keyword_count.csv
Example output (excerpt):

url	climate change	emission	carbon	renewable	net zero
https://vnexpress.net/viet-nam-thuc-day-nang-luong-tai-tao-4808374.html
	3	2	1	4	0
https://vnexpress.net/gan-600-loai-moi-duoc-phat-hien-o-vung-tay-himalaya-4809827.html
	1	0	0	0	0
📊 Example Workflow

Crawl all articles

Define keywords in keywords.txt

Run the keyword analyzer

Load keyword_count.csv into Excel or Power BI for visualization


🧠 Future Improvements

Add sentiment analysis or TF-IDF scoring
Integrate keyword co-occurrence networks
Visualize keyword trends over time
Support multiple Vietnamese news sources
