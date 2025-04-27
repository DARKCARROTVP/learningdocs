from flask import Flask, request, jsonify, render_template, send_from_directory
import threading
from cf_scraper_app import scrape_codeforces_concurrent
import os
import json

app = Flask(__name__)

progress_lock = threading.Lock()
progress = {
    "current": 0,
    "total": 0,
    "filename": ""
}

benchmark_status = {
    "current": 0,
    "total": 0,
    "done": False,
    "result": []
}

def update_progress_callback(current, total):
    with progress_lock:
        progress["current"] = current
        progress["total"] = total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_task():
    start_page = int(request.form['start'])
    end_page = int(request.form['end'])
    thread_num = int(request.form['threads'])

    def run_scraper():
        filename = scrape_codeforces_concurrent(
            start_page=start_page,
            end_page=end_page,
            max_threads=thread_num,
            progress_callback=update_progress_callback
        )
        with progress_lock:
            progress["filename"] = filename

    threading.Thread(target=run_scraper).start()

    return jsonify({
        "message": "任务已启动",
        "filename": None
    })

@app.route('/progress')
def get_progress():
    with progress_lock:
        return jsonify(progress)

@app.route('/data/<path:filename>')
def download_file(filename):
    directory = os.path.abspath('experiment_result_data')
    return send_from_directory(directory, filename)

@app.route('/timing/<path:filename>')
def get_timing(filename):
    json_path = os.path.join('experiment_result_data', filename.replace('.csv', '') + '_timing.json')
    if not os.path.exists(json_path):
        return jsonify({"error": "timing file not found"}), 404
    with open(json_path, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/benchmark_progress')
def benchmark_progress():
    return jsonify({
        "current": benchmark_status["current"],
        "total": benchmark_status["total"],
        "done": benchmark_status["done"]
    })

@app.route('/benchmark_result')
def benchmark_result():
    return jsonify(benchmark_status["result"])

@app.route('/benchmark_threads')
def benchmark_threads():
    import time
    import matplotlib.pyplot as plt

    start_page = int(request.args.get("start", 1))
    end_page = int(request.args.get("end", 20))
    max_threads = int(request.args.get("max_threads", 10))

    def run_benchmark():
        benchmark_status["current"] = 0
        benchmark_status["total"] = max_threads
        benchmark_status["done"] = False
        benchmark_status["result"] = []

        increasing_count = 0
        last_duration = None

        for threads in range(1, max_threads + 1):
            print(f"🧪 Benchmarking with {threads} threads")
            t0 = time.time()
            scrape_codeforces_concurrent(
                start_page=start_page,
                end_page=end_page,
                max_threads=threads,
                progress_callback=lambda cur, total: None
            )
            t1 = time.time()
            duration = round(t1 - t0, 2)

            benchmark_status["result"].append({
                "threads": threads,
                "duration": duration
            })
            benchmark_status["current"] = threads

            if last_duration is not None and duration > last_duration:
                increasing_count += 1
            else:
                increasing_count = 0
            last_duration = duration

            if increasing_count >= 2:
                print("⚠️ 提前停止：连续两次耗时增加")
                break

        # 保存图像
        x = [r["threads"] for r in benchmark_status["result"]]
        y = [r["duration"] for r in benchmark_status["result"]]
        plt.figure(figsize=(8, 5))
        plt.plot(x, y, marker='o')
        plt.xlabel("线程数")
        plt.ylabel("总耗时（秒）")
        plt.title("最优线程数")
        plt.grid(True)
        image_path = os.path.join("experiment_result_data", "benchmark_threads.png")
        plt.savefig(image_path)
        plt.close()

        benchmark_status["done"] = True

    threading.Thread(target=run_benchmark).start()

    return jsonify({"message": "Benchmark started"})
