import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# =========================
# TASK 6: Retry logic
# =========================
def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                timeout=5,
                headers={"User-Agent": "SimpleCrawler/1.0"}
            )
            if response.status_code == 200:
                return response.text
        except:
            time.sleep(1)
    return None


# =========================
# TASK 3 + TASK 4
# Filter useless links + same-domain only
# =========================
def extract_links(base_url, html, seed_domain):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"]

        # TASK 3: filter useless links
        if href.startswith(("mailto:", "javascript:", "#", "tel:")):
            continue

        full_url = urljoin(base_url, href)

        if not full_url.startswith(("http://", "https://")):
            continue

        # TASK 4: same-domain crawling
        if urlparse(full_url).netloc != seed_domain:
            continue

        links.add(full_url)

    return links


# =========================
# TASK 1: Basic crawler
# TASK 2: Save pages in pages/
# TASK 5: Save visited URLs
# =========================
def crawl(seed_url, max_pages=10):
    print(f"\nStarting crawl for: {seed_url}")

    seed_domain = urlparse(seed_url).netloc
    queue = [seed_url]
    visited = set()
    successful_pages = 0

    start_time = time.time()

    # TASK 2: create pages folder
    if not os.path.exists("pages"):
        os.mkdir("pages")

    while queue and successful_pages < max_pages:
        url = queue.pop(0)

        if url in visited:
            continue

        print(f"[Crawling] {url}")
        html = fetch_page(url)

        if html is None:
            visited.add(url)
            continue

        # TASK 2: save HTML pages
        file_name = f"pages/page_{successful_pages + 1}.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[Saved] {file_name}")

        successful_pages += 1
        visited.add(url)

        links = extract_links(url, html, seed_domain)
        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)

        time.sleep(0.3)

    end_time = time.time()

    # TASK 5: save visited URLs
    with open("visited.txt", "w") as f:
        for link in visited:
            f.write(link + "\n")

    print("\n=========== SUMMARY ===========")
    print(f"Total Time Taken : {end_time - start_time:.2f} seconds")
    print(f"Pages Crawled    : {successful_pages}")
    print(f"Unique URLs      : {len(visited)}")
    print(f"Duplicate URLs   : 0 (fully filtered)")
    print("================================")


# =========================
# Program start
# =========================
if __name__ == "__main__":
    crawl("https://coursera.org", max_pages=30)
