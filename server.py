from flask import Flask, send_file, jsonify, request
import random
import time
from datetime import datetime

app = Flask(__name__, static_folder='.')

# Giả lập bộ nhớ của ESP32
device_state = {
    "pwr": 0,
    "freq": 0,
    "dir": 1,
    "output1": 0,
    "output2": 0,
    "ssid": "MyWiFi",
    "pass": "12345678",
    "input1_on_interval": 10, "input1_off_interval": 5,
    "input2_on_interval": 10, "input2_off_interval": 5,
    # Dữ liệu timer giả lập (chưa có gì)
    "t1_en": 0, "t1_on": "07:00", "t1_off": "17:00", "t1_out": 0,
    "t2_en": 0, "t2_on": "00:00", "t2_off": "00:00", "t2_out": 0,
    "t3_en": 0, "t3_on": "00:00", "t3_off": "00:00", "t3_out": 0,
    "t4_en": 0, "t4_on": "00:00", "t4_off": "00:00", "t4_out": 0
}

# --- ROUTE CHO GIAO DIỆN WEB ---
@app.route('/')
def home():
    return send_file('index.html')

# --- API GIẢ LẬP ESP32 ---

@app.route('/status')
def get_status():
    # Tạo dữ liệu ngẫu nhiên cho RAM/CPU để thấy giao diện nhảy số
    return jsonify({
        "connected": True,
        "time": datetime.now().strftime("%H:%M:%S"),
        "ip": "192.168.1.100",
        "ram_usage": random.randint(30, 60),
        "cpu_load": random.randint(5, 20),
        "pwr": device_state["pwr"],
        "freq": device_state["freq"],
        "dir": device_state["dir"],
        "output1": device_state["output1"],
        "output2": device_state["output2"],
        # Timer inputs
        "timer_en": 1,
        "input1_on_interval": device_state["input1_on_interval"],
        "input1_off_interval": device_state["input1_off_interval"],
        "input2_on_interval": device_state["input2_on_interval"],
        "input2_off_interval": device_state["input2_off_interval"]
    })

@app.route('/get-config')
def get_config():
    # Trả về toàn bộ config để điền vào form settings
    return jsonify(device_state)

@app.route('/setPower')
def set_power():
    val = request.args.get('val', type=int)
    device_state["pwr"] = val
    print(f"👉 MOTOR POWER: {'ON' if val else 'OFF'}")
    return "OK"

@app.route('/setFreq')
def set_freq():
    val = request.args.get('val', type=int)
    device_state["freq"] = val
    print(f"👉 SET FREQ: {val} Hz")
    return "OK"

@app.route('/setDir')
def set_dir():
    val = request.args.get('val', type=int)
    device_state["dir"] = val
    print(f"👉 SET DIR: {'THUẬN' if val else 'NGHỊCH'}")
    return "OK"

@app.route('/setOutput1')
def set_out1():
    val = request.args.get('val', type=int)
    device_state["output1"] = val
    print(f"👉 OUTPUT 1: {val}")
    return "OK"

@app.route('/setOutput2')
def set_out2():
    val = request.args.get('val', type=int)
    device_state["output2"] = val
    print(f"👉 OUTPUT 2: {val}")
    return "OK"

@app.route('/saveWifi', methods=['POST'])
def save_wifi():
    print(f"📡 SAVE WIFI: {request.get_data(as_text=True)}")
    return "OK"

@app.route('/saveTimers', methods=['POST'])
def save_timers():
    data = request.json
    print("⏰ RECEIVED TIMERS JSON:")
    print(data)
    
    # Cập nhật state giả lập để khi reload trang settings vẫn thấy dữ liệu
    if 'timers' in data:
        for t in data['timers']:
            tid = t['id']
            device_state[f"t{tid}_en"] = t['en']
            device_state[f"t{tid}_on"] = t['on']
            device_state[f"t{tid}_off"] = t['off']
            device_state[f"t{tid}_out"] = t['out']
            
    return "OK"

@app.route('/reboot')
def reboot():
    print("🔄 REBOOTING SYSTEM...")
    return "OK"

if __name__ == '__main__':
    print("🚀 Server đang chạy tại: http://localhost:5000")
    print("Mở trình duyệt và truy cập địa chỉ trên.")
    app.run(port=5000, debug=True)