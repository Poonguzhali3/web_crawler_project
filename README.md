Web Crawler Project

This project is a simple Python-based web crawler.

Features:
- Crawls web pages starting from a seed URL
- Saves crawled HTML pages into pages/ folder
- Filters useless links (mailto, javascript, tel, #)
- Prevents duplicate URLs
- Crawls only same-domain links
- Saves visited URLs into visited.txt
- Includes retry logic for failed URLs

Technologies Used:
- Python
- requests
- BeautifulSoup

How to Run:
python crawler.py
