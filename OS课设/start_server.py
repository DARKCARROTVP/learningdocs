import os
import subprocess
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

def start_flask():
    print("🚀 正在启动 Flask Web Server...")

    # 🔧 设置环境变量，指向 flask_web.app
    os.environ["FLASK_APP"] = "flask_web.app"
    os.environ["FLASK_ENV"] = "development"

    subprocess.call(["flask", "run"])

if __name__ == "__main__":
    Timer(1, open_browser).start()
    start_flask()
