import serial
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rcParams
import sys
import queue
import time

rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

SERIAL_PORT = 'COM4'   # 你的实际串口号
BAUD_RATE = 115200

data_queue = queue.Queue()
log_filename = 'data_log.txt'

def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        with open(log_filename, 'a') as f:
            while True:
                line = ser.readline().decode(errors='ignore').strip()
                if line:
                    try:
                        value = float(line)
                        data_queue.put(value)
                        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{value}\n")
                        f.flush()  # 立即写入文件
                    except ValueError:
                        continue
    except serial.SerialException as e:
        print(f"无法打开串口: {e}")
        sys.exit(1)

def map_y(value):
    if value == 0:
        return 100
    elif 50000 <= value <= 55000:
        return 200 + (value - 50000) * (200) / (55000 - 50000)
    else:
        if value < 50000:
            return 100 + (value/50000)*100
        else:
            return 400 + (value-55000)/1000

def animate(i, xs, ys):
    while not data_queue.empty():
        value = data_queue.get()
        xs.append(xs[-1] + 1 if xs else 0)
        ys.append(map_y(value))
# 只保留最近100个点用于显示
        xs[:] = xs[-100:]
        ys[:] = ys[-100:]
    ax.clear()
    ax.plot(xs, ys, marker='o')
    ax.set_title("血氧与心率")
    ax.set_xlabel("采样")
    ax.set_ylabel("IR")
    ax.grid(True)
# Y轴刻度定制
    ax.set_yticks([100, 200, 300, 400, 500])
    ax.set_yticklabels(['y=0', 'y=50000', 'y=52500', 'y=55000', ''])

if __name__ == '__main__':
    xs, ys = [], []
    fig, ax = plt.subplots()

    t = threading.Thread(target=read_serial, daemon=True)
    t.start()

    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)
    plt.tight_layout()
    plt.show()
