import os
import time
import random
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from tqdm import tqdm

def fetch_and_extract_page(page_num: int):
    html_path = f"cf_page_{page_num}.html"
    start_rank = (page_num - 1) * 200 + 1
    all_data = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale=random.choice(["en-US", "en-GB", "zh-CN"])
            )
            page = context.new_page()

            url = f"https://codeforces.com/ratings/page/{page_num}"
            print(f"🌍 正在访问第 {page_num} 页: {url}")

            page.goto(url, timeout=20000)
            page.wait_for_selector("div.datatable.ratingsDatatable", timeout=10000)
            time.sleep(random.uniform(1.5, 3.5))
            html = page.content()
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
            browser.close()

        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        wrapper = soup.find("div", class_="datatable ratingsDatatable")
        if not wrapper:
            print(f"❌ 第 {page_num} 页未找到表格")
            return []

        table = wrapper.find("table")
        rows = table.find_all("tr")[1:]

        for i, row in enumerate(rows):
            cols = row.find_all("td")
            if len(cols) >= 4:
                all_data.append({
                    "Rank": start_rank + i,
                    "Handle": cols[1].text.strip(),
                    "Participations": cols[2].text.strip(),
                    "Rating": cols[3].text.strip()
                })

        os.remove(html_path)
        print(f"✅ 第 {page_num} 页处理完成")
        return all_data

    except Exception as e:
        print(f"❌ 第 {page_num} 页处理失败: {e}")
        return []

def scrape_codeforces_concurrent(from_page=1, to_page=10, max_threads=5, status_callback=None):
    all_results = []
    total_pages = to_page - from_page + 1
    finished_pages = 0

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {
            executor.submit(fetch_and_extract_page, page): page
            for page in range(from_page, to_page + 1)
        }
        for future in as_completed(futures):
            result = future.result()
            if result:
                all_results.extend(result)
            finished_pages += 1
            if status_callback:
                status_callback(finished_pages, total_pages)
            time.sleep(random.uniform(0.5, 1.5))

    df = pd.DataFrame(all_results)
    df = df.sort_values(by="Rank").reset_index(drop=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cf_ratings_{from_page}-{to_page}_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"\n🎉 共抓取 {len(df)} 条数据，已保存为 {filename}")
    return filename
