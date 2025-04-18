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