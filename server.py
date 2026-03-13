from flask import Flask, send_file, jsonify, request
import random
import time
from datetime import datetime

app = Flask(__name__, static_folder='.')

# Giả lập bộ nhớ của ESP32 với các key khớp với bảng JSON
device_state = {
    # Status Variables
    "connected": True,
    "ip": "192.168.1.100",
    "Inv_state": True,
    "Inv_dir": True,
    "Inv_freq": "46",
    "input1_on_interval": "58", "input1_off_interval": "68","input1_state": False,
    "input2_on_interval": "75", "input2_off_interval": "90", "input2_state" : True,
    "input3_on_interval": "88", "input3_off_interval": "36","input3_state": True,
    "input4_on_interval": "15", "input4_off_interval": "75","input4_state": False,
    "output1_level": True, "output2_level": False,
    "output3_level": False, "output4_level": False,

    # WiFi Config Variables
    "ssid": "CMNIoT_WiFi",
    "pass": "12345678",
    "sta_enable": True,
    "is_static": False,
    "static_ip": "192.168.1.100",
    "gateway": "192.168.1.1",
    "netmask": "255.255.255.0",
    "ap_ssid": "ESP32_AP",
    "ap_pass": "12345678",
    "mqtt_name" : "cmn01",
    "mqtt_pass" : "1234",
    
    # GPIO & Timer Config Variables
    "gpios": "0",
    "timer1_en": True, "timer1_on": "00:00", "timer1_off": "08:00", "timer1_mask": "18",
    "timer2_en": True, "timer2_on": "05:00", "timer2_off": "13:00", "timer2_mask": "12",
    "timer3_en": False, "timer3_on": "00:00", "timer3_off": "00:00", "timer3_mask": "0",
    "timer4_en": False, "timer4_on": "00:00", "timer4_off": "00:00", "timer4_mask": "0",
    
    # Inverter Config Variables
    "Inv_enable": True,
    "Inv_baudrate": "9600",
    "Inv_model": "0",
    "Inv_addr": "1"
}

# --- ROUTE CHO GIAO DIỆN WEB ---
@app.route('/')
def home():
    return send_file('index.html')

# --- API GIẢ LẬP ESP32 ---

@app.route('/status')
def get_status():
    # Tạo dữ liệu động cho time, ram, cpu
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    # Trả về cục JSON cấu trúc y hệt như bảng yêu cầu
    status_data = {
        "time": current_time,
        "connected": device_state["connected"],
        "ip": device_state["ip"],
        "Inv_state": device_state["Inv_state"],
        "Inv_dir": device_state["Inv_dir"],
        "ram_usage": str(random.randint(30, 60)), # Sinh ngẫu nhiên RAM %
        "cpu_load": str(random.randint(5, 25)),   # Sinh ngẫu nhiên CPU %
        "Inv_freq": str(device_state["Inv_freq"]),
        "input1_on_interval": device_state["input1_on_interval"],
        "input1_off_interval": device_state["input1_off_interval"],
        "input1_state": device_state["input1_state"],
        "input2_on_interval": device_state["input2_on_interval"],
        "input2_off_interval": device_state["input2_off_interval"],
        "input2_state": device_state["input2_state"],
        "input3_on_interval": device_state["input3_on_interval"],
        "input3_off_interval": device_state["input3_off_interval"],
        "input3_state": device_state["input3_state"],
        "input4_on_interval": device_state["input4_on_interval"],
        "input4_off_interval": device_state["input4_off_interval"],
        "input4_state": device_state["input4_state"],
        "output1_level": device_state["output1_level"],
        "output2_level": device_state["output2_level"],
        "output3_level": device_state["output3_level"],
        "output4_level": device_state["output4_level"],
        "error_code": random.choice(["0", "1", "2", "3"])
    }

    return jsonify(status_data)
    
@app.route('/get-config')
def get_config():
    # Log current config for settings page
    config_data = {
        "ssid": device_state["ssid"],
        "pass": device_state["pass"],
        "sta_enable": device_state["sta_enable"],
        "is_static": device_state["is_static"],
        "static_ip": device_state["static_ip"],
        "gateway": device_state["gateway"],
        "netmask": device_state["netmask"],
        "ap_ssid": device_state["ap_ssid"],
        "ap_pass": device_state["ap_pass"],
        "Inv_state": device_state["Inv_state"],
        "Inv_dir": device_state["Inv_dir"],
        "Inv_freq": device_state["Inv_freq"],
        "gpios": device_state["gpios"],
        "input1_state": device_state["input1_state"],
        "input2_state": device_state["input2_state"],
        "input3_state": device_state["input3_state"],
        "input4_state": device_state["input4_state"],
        "timer1_en": device_state["timer1_en"],
        "timer1_on": device_state["timer1_on"],
        "timer1_off": device_state["timer1_off"],
        "timer1_mask": device_state["timer1_mask"],
        "timer2_en": device_state["timer2_en"],
        "timer2_on": device_state["timer2_on"],
        "timer2_off": device_state["timer2_off"],
        "timer2_mask": device_state["timer2_mask"],
        "timer3_en": device_state["timer3_en"],
        "timer3_on": device_state["timer3_on"],
        "timer3_off": device_state["timer3_off"],
        "timer3_mask": device_state["timer3_mask"],
        "timer4_en": device_state["timer4_en"],
        "timer4_on": device_state["timer4_on"],
        "timer4_off": device_state["timer4_off"],
        "timer4_mask": device_state["timer4_mask"],
        "Inv_enable": device_state["Inv_enable"],
        "Inv_baudrate": device_state["Inv_baudrate"],
        "Inv_model": device_state["Inv_model"],
        "Inv_addr": device_state["Inv_addr"],
        "mqtt_name" : device_state["mqtt_name"],
        "mqtt_pass" : device_state["mqtt_pass"]
    }
    print("👉 GET CONFIG CALLED")
    for key, value in config_data.items():
        print(f"   {key}: {value}")
    return jsonify(config_data)

@app.route('/InvSetStart')
def set_power():
    val = request.args.get('val', type=int)
    device_state["Inv_state"] = bool(val)
    print(f"👉 MOTOR POWER: {'ON' if val else 'OFF'}")
    return "OK"

@app.route('/InvSetFreq')
def set_freq():
    val = request.args.get('val', type=int)
    device_state["Inv_freq"] = str(val)
    print(f"👉 SET FREQ: {val} Hz")
    return "OK"

@app.route('/InvCfg')
def set_inv_cfg():
    model = request.args.get('inverterOption', default="None")
    address = request.args.get('inverterAddress', default="0")
    baud = request.args.get('inverterBaudrate', default="9600")
    device_state["Inv_model"] = model
    device_state["Inv_addr"] = address
    device_state["Inv_baudrate"] = baud
    print(f"👉 SET INVERTER CONFIG: Model={model}, Address={address}, Baudrate={baud}")
    return "OK"

@app.route('/InvEn')
def set_inv_en():
    val = request.args.get('val', type=int)
    device_state["Inv_enable"] = bool(val)
    print(f"👉 INVERTER ENABLE: {'ON' if val else 'OFF'}")
    return "OK"

@app.route('/setTimer')
def set_timer():
    timer_id = request.args.get('timer', type=int)
    on_time = request.args.get('on', default="00:00")
    off_time = request.args.get('off', default="00:00")
    mask = request.args.get('mask', type=int, default=0)
    
    device_state[f"timer{timer_id}_on"] = on_time
    device_state[f"timer{timer_id}_off"] = off_time
    device_state[f"timer{timer_id}_mask"] = str(mask)
    
    print(f"👉 SET TIMER {timer_id}: ON={on_time}, OFF={off_time}, OUTPUT_MASK={mask}")
    return "OK"

@app.route('/setTimeren')
def set_timer_en():
    timer_id = request.args.get('timer', type=int)
    en = request.args.get('en', type=int, default=0)
    device_state[f"timer{timer_id}_en"] = bool(en)
    print(f"👉 SET TIMER {timer_id} ENABLE: {bool(en)}")
    return "OK"

@app.route('/InvSetDir')
def set_dir():
    val = request.args.get('val', type=int)
    device_state["Inv_dir"] = bool(val)
    print(f"👉 SET DIR: {'THUẬN' if val else 'NGHỊCH'}")
    return "OK"

@app.route('/setGpios')
def set_gpios():
    mask = request.args.get('m', default="0")
    device_state["gpios"] = mask
    print(f"👉 SET GPIOs with Mask = {mask}")
    return "OK"

@app.route('/setOutput1')
def set_out1():
    val = request.args.get('val', type=int)
    device_state["output1_level"] = bool(val)
    print(f"👉 OUTPUT 1: {val}")
    return "OK"

@app.route('/setOutput2')
def set_out2():
    val = request.args.get('val', type=int)
    device_state["output2_level"] = bool(val)
    print(f"👉 OUTPUT 2: {val}")
    return "OK"

@app.route('/setOutput3')
def set_out3():
    val = request.args.get('val', type=int)
    device_state["output3_level"] = bool(val)
    print(f"👉 OUTPUT 3: {val}")
    return "OK"

@app.route('/setOutput4')
def set_out4():
    val = request.args.get('val', type=int)
    device_state["output4_level"] = bool(val)
    print(f"👉 OUTPUT 4: {val}")
    return "OK"

@app.route('/saveWifi', methods=['POST'])
def save_wifi():
    print(f"📡 SAVE WIFI: {request.get_data(as_text=True)}")
    # Có thể extract ssid và pass ở đây để lưu vào device_state nếu cần
    return "OK"

@app.route('/saveMQTT', methods=['POST'])
def save_mqtt():
    print(f"📡 SAVE MQTT: {request.get_data(as_text=True)}")
    # Có thể extract broker, username, pass ở đây để lưu vào device_state nếu cần
    return "OK"

@app.route('/setAdcLimits')
def set_adc_limits():
    voltage = request.args.get('voltage', type=float)
    current = request.args.get('current', type=float)
    device_state["adc_voltage_limit"] = voltage
    device_state["adc_current_limit"] = current
    print(f"👉 SET ADC LIMITS: Voltage={voltage}V, Current={current}A")
    return "OK"

@app.route('/reboot')
def reboot():
    print("🔄 REBOOTING SYSTEM...")
    return "OK"

if __name__ == '__main__':
    print("🚀 Server đang chạy tại: http://localhost:5000")
    print("Mở trình duyệt và truy cập địa chỉ trên.")
    app.run(port=5000, debug=True)