from flask import Flask, render_template, request, jsonify
import threading
import time
import uuid
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import cf_scraper_app

app = Flask(__name__)

# ✅ 多任务池
task_pool = {}

def background_scrape(task_id, from_page, to_page, threads):
    task_pool[task_id]["status"] = "running"
    task_pool[task_id]["progress"] = {"done": 0, "total": to_page - from_page + 1}
    task_pool[task_id]["filename"] = None
    task_pool[task_id]["error"] = None

    def progress_callback(done, total):
        task_pool[task_id]["progress"] = {"done": done, "total": total}

    try:
        filename = cf_scraper_app.scrape_codeforces_concurrent(
            from_page=from_page,
            to_page=to_page,
            max_threads=threads,
            status_callback=progress_callback
        )
        task_pool[task_id]["status"] = "done"
        task_pool[task_id]["filename"] = filename
    except Exception as e:
        task_pool[task_id]["status"] = "error"
        task_pool[task_id]["error"] = str(e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_scraper():
    from_page = int(request.form.get("from_page", 1))
    to_page = int(request.form.get("to_page", 10))
    threads = int(request.form.get("threads", 5))
    task_id = str(uuid.uuid4())

    task_pool[task_id] = {
        "status": "pending",
        "progress": {"done": 0, "total": to_page - from_page + 1},
        "filename": None,
        "error": None
    }

    threading.Thread(
        target=background_scrape,
        args=(task_id, from_page, to_page, threads)
    ).start()

    return jsonify({"task_id": task_id})

@app.route("/task_status")
def task_status():
    task_id = request.args.get("task_id")
    task = task_pool.get(task_id)
    if not task:
        return jsonify({"error": "任务不存在"}), 404
    return jsonify(task)

@app.route("/read_csv")
def read_csv():
    filename = request.args.get("filename")
    if not filename or not os.path.exists(filename):
        return jsonify({"error": "CSV 文件不存在"}), 400
    df = pd.read_csv(filename)
    return df.to_json(orient="records", force_ascii=False)

if __name__ == "__main__":
    app.run(debug=True)
