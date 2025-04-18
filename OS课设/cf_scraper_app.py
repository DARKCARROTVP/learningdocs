import os
import time
import random
import json
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_and_extract_page(page_num: int):
    html_path = f"cf_page_{page_num}.html"
    start_rank = (page_num - 1) * 200 + 1
    all_data = []

    thread_start_time = time.time()
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

            page.goto(url, timeout=30000)
            page.wait_for_selector("div.datatable.ratingsDatatable", timeout=15000)
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
            return [], {}

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
        thread_end_time = time.time()
        duration = thread_end_time - thread_start_time
        print(f"✅ 第 {page_num} 页处理完成，用时 {duration:.2f} 秒")

        timing = {
            "page": page_num,
            "duration": round(duration, 2),
            "start": round(thread_start_time, 2),
            "end": round(thread_end_time, 2)
        }

        return all_data, timing

    except Exception as e:
        print(f"❌ 第 {page_num} 页处理失败: {e}")
        return [], {}

def scrape_codeforces_concurrent(start_page=1, end_page=10, max_threads=5, progress_callback=None):
    all_results = []
    thread_timings = []
    total_pages = end_page - start_page + 1
    finished_pages = 0

    task_start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {
            executor.submit(fetch_and_extract_page, page): page
            for page in range(start_page, end_page + 1)
        }
        for future in as_completed(futures):
            result, timing = future.result()
            if result:
                all_results.extend(result)
            if timing:
                thread_timings.append(timing)
            finished_pages += 1
            if progress_callback:
                progress_callback(finished_pages, total_pages)
            time.sleep(random.uniform(0.5, 1.0))

    df = pd.DataFrame(all_results)
    if df.empty:
        print("⚠️ 警告：没有抓取到任何数据")
        return None

    df = df.sort_values(by="Rank").reset_index(drop=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = "experiment_result_data"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"cf_ratings_{start_page}-{end_page}_{timestamp}.csv"
    full_path = os.path.join(output_dir, filename)
    df.to_csv(full_path, index=False, encoding="utf-8-sig")

    task_end_time = time.time()
    task_duration = task_end_time - task_start_time
    print(f"\n🎉 共抓取 {len(df)} 条数据，保存为 {full_path}")
    print(f"📊 总任务耗时：{task_duration:.2f} 秒")

    timing_file = os.path.join(output_dir, f"{filename.replace('.csv', '')}_timing.json")
    with open(timing_file, "w") as f:
        json.dump({
            "total_time": round(task_duration, 2),
            "task_start": round(task_start_time, 2),
            "task_end": round(task_end_time, 2),
            "pages": sorted(thread_timings, key=lambda x: x["page"])
        }, f, indent=2)
    print(f"📁 已保存线程耗时 JSON：{timing_file}")
    return filename