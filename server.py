from flask import Flask, send_file, jsonify, request
import random
import time
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='.')

STATE_FILE = 'device_state.json'

# Default simulated memory of ESP32
default_device_state = {
    # Status Variables
    "connected": True,
    "ip": "192.168.1.100",
    "factory_id" : "1233213",
    "Inv_state": False,
    "Inv_dir": False,
    "Inv_freq": "46",
    "input1_state": False, "input2_state" : True,
    "input3_state": True, "input4_state": False,
    "output1_level": True, "output2_level": False,
    "output3_level": False, "output4_level": False,
    "in1_thr_en" : False, "in1_input_thr" : 11, "in1_scale_factor" : 111,
    "in2_thr_en" : True, "in2_input_thr" : 22, "in2_scale_factor" : 222,
    "in3_thr_en" : False, "in3_input_thr" : 33, "in3_scale_factor" : 333,
    "in4_thr_en" : True, "in4_input_thr" : 44, "in4_scale_factor" : 444,

    # Real-time hardware values (simulated)
    "adc_voltage": 12.5,
    "adc_current": 2.1,
    
    # Config Variables
    "adc_enable": True,
    "io_enable": True,
    "Inv_enable": True,
    "adc_voltage_limit": 24,
    "adc_current_limit": 5,
    
    "motor_mode": "3", # 1: Inverter, 2: Contactor, 3: Both
    "Inv_model": "1",
    "Inv_addr": "1",
    "Inv_baudrate": "9600",
    
    "Motor1_state" : True,
    "Motor2_state" : False,    
    
    "motor1_en": True, "motor1_on_pin": "1", "motor1_off_pin": "2",
    "motor2_en": False, "motor2_on_pin": "3", "motor2_off_pin": "4",

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
    "mqtt_link" : "12.332.32.21",
    "mqtt_topic": "device/data",
    "mqtt_id" : "asc",
    "mqtt_port" : "1883",
    
    "gpios": "100",
    "timer1_en": True, "timer1_on": "00:00", "timer1_off": "08:00", "timer1_mask": "1",
    "timer2_en": True, "timer2_on": "05:00", "timer2_off": "13:00", "timer2_mask": "12",
    "timer3_en": False, "timer3_on": "00:00", "timer3_off": "00:00", "timer3_mask": "0",
    "timer4_en": False, "timer4_on": "00:00", "timer4_off": "00:00", "timer4_mask": "0",
}

# --- JSON SAVE/LOAD LOGIC ---
def load_state():
    """Load device state from JSON file or create with defaults if it doesn't exist."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading state from {STATE_FILE}: {e}")
    return default_device_state.copy()

@app.route('/saveSettings')
def save_state():
    """Save the current device state to the JSON file by deleting the old one first."""
        # 1. Delete the existing file if it exists
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    
    # 2. Create a new file and write the fresh state
    with open(STATE_FILE, 'w') as f:
        json.dump(device_state, f, indent=4) 
    return "OK"           

# Initialize state on startup
device_state = load_state()
save_state()  # Ensure file is created on first run

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/status')
def get_status():
    now = datetime.now()
    status_data = {
        "time": now.strftime("%H:%M:%S"),
        "connected": device_state["connected"],
        "mqtt_connected": random.choice([True, False]), # Random simulation
        "ip": device_state["ip"],
        
        "adcEn" : device_state["adc_enable"],
        "ioEn" : device_state["io_enable"],
        "Inv_state": device_state["Inv_state"],
        "Motor1_state" : device_state["Motor1_state"],
        "Motor2_state" : device_state["Motor2_state"],
        "Inv_dir": device_state["Inv_dir"],
        "Inv_freq": device_state["Inv_freq"],
        "ram_usage": str(random.randint(30, 60)), 
        "cpu_load": str(random.randint(5, 25)),
        "adc_voltage": round(random.uniform(10.0, 24.0), 2),
        "adc_current": round(random.uniform(0.5, 4.5), 2),
        "input1_state": device_state["input1_state"],
        "input2_state": device_state["input2_state"],
        "input3_state": device_state["input3_state"],
        "input4_state": device_state["input4_state"],
        
        "input1_on_interval": 12,
        "input2_on_interval": 24,
        "input3_on_interval": 44,
        "input4_on_interval": 22,
        
        "input1_off_interval": 35,
        "input2_off_interval": 25,
        "input3_off_interval": 77,
        "input4_off_interval": 21,
        
        "output1_level": device_state["output1_level"],
        "output2_level": device_state["output2_level"],
        "output3_level": device_state["output3_level"],
        "output4_level": device_state["output4_level"],
        "error_code": str(random.randint(0, 11))
    }
    return jsonify(status_data)
    
@app.route('/get-config')
def get_config():
    for i in device_state.keys():
        print(f"{i} : {device_state[i]}")
    print("👉 GET CONFIG CALLED")
    return jsonify(device_state)

# --- REWRITTEN ENDPOINTS CATCHING SAVESETTINGS DATA ---

@app.route('/MotorConf')
def motor_conf():
    en = request.args.get('en', type=int, default=0)
    device_state["Inv_enable"] = bool(en)
    
    if en:
        mode = request.args.get('mode', type=int, default=0)
        device_state["motor_mode"] = str(mode)
        
        # Mode 1 (Inverter) or Mode 3 (Both)
        if mode == 1 or mode == 3:
            device_state["Inv_model"] = request.args.get('model', default=device_state["Inv_model"])
            device_state["Inv_addr"] = request.args.get('addr', default=device_state["Inv_addr"])
            device_state["Inv_baudrate"] = request.args.get('baud', default=device_state["Inv_baudrate"])
            
        # Mode 2 (Contactor) or Mode 3 (Both)
        if mode == 2 or mode == 3:
            device_state["motor1_en"] = bool(request.args.get('Mot1En', type=int, default=0))
            device_state["motor1_on_pin"] = request.args.get('StartPin1', default="0")
            device_state["motor1_off_pin"] = request.args.get('StopPin1', default="0")
            
            device_state["motor2_en"] = bool(request.args.get('Mot2En', type=int, default=0))
            device_state["motor2_on_pin"] = request.args.get('StartPin2', default="0")
            device_state["motor2_off_pin"] = request.args.get('StopPin2', default="0")
    print(f"👉 MOTOR CONFIG UPDATED: Mode={device_state['motor_mode']}, Enabled={device_state['Inv_enable']}")
    return "OK"

@app.route('/adcEn')
def enable_adc():
    device_state["adc_enable"] = bool(request.args.get('en', type=int))
    return "OK"

@app.route('/gpioEn')
def enable_gpio():
    device_state["io_enable"] = bool(request.args.get('en', type=int))
    return "OK"    

@app.route('/setAdcLimits')
def set_adc_limits():
    device_state["adc_voltage_limit"] = request.args.get('voltage', type=float, default=0.0)
    device_state["adc_current_limit"] = request.args.get('current', type=float, default=0.0)
    print(f"👉 ADC LIMITS: V={device_state['adc_voltage_limit']}, A={device_state['adc_current_limit']}")
    return "OK"

@app.route('/setGpios')
def set_gpios():
    device_state["gpios"] = request.args.get('m', default="0")
    for i in range(1,5):
        device_state[f"in{i}_thr_en"] = request.args.get(f"in{i}_thr_en",type = int, default = 0) 
        device_state[f"in{i}_input_thr"] = request.args.get(f"in{i}_input_thr",type = int, default = 0) 
        device_state[f"in{i}_scale_factor"] = request.args.get(f"in{i}_scale_factor",type = int, default = 0)
        print(f"Input {i} threshold enabled : ", device_state[f"in{i}_thr_en"])
        print(f"Input {i} threshold input : ", device_state[f"in{i}_input_thr"])
        print(f"Input {i} scale factor : ", device_state[f"in{i}_scale_factor"])
            
    print(f"👉 GPIO MASK: {device_state['gpios']}")
    
    return "OK"

@app.route('/setTimer')
def set_timer():
    t_id = request.args.get('timer', type=int)
    device_state[f"timer{t_id}_on"] = request.args.get('on', default="00:00")
    device_state[f"timer{t_id}_off"] = request.args.get('off', default="00:00")
    device_state[f"timer{t_id}_mask"] = request.args.get('mask', default="0")
    return "OK"

@app.route('/setTimeren')
def set_timer_en():
    t_id = request.args.get('timer', type=int)
    device_state[f"timer{t_id}_en"] = bool(request.args.get('en', type=int, default=0))
    return "OK"

@app.route('/saveWifi', methods=['POST'])
def save_wifi():
    device_state["sta_enable"] = bool(int(request.form.get('sta_enable', 0)))
    device_state["ssid"] = request.form.get('ssid', '')
    device_state["pass"] = request.form.get('pass', '')
    device_state["is_static"] = bool(int(request.form.get('isStatic', 0)))
    device_state["static_ip"] = request.form.get('ip', '')
    device_state["gateway"] = request.form.get('gateway', '')
    device_state["netmask"] = request.form.get('netmask', '')
    print(f"📡 WIFI UPDATED: {device_state['ssid']}")
    return "OK"

@app.route('/saveAP', methods=['POST'])
def save_ap():
    device_state["ap_ssid"] = request.form.get('ap_name', '')
    device_state["ap_pass"] = request.form.get('ap_pass', '')
    return "OK"

@app.route('/saveMQTT', methods=['POST'])
def save_mqtt():
    device_state["mqtt_name"] = request.form.get('mqtt_name', '')
    device_state["mqtt_pass"] = request.form.get('mqtt_pass', '')
    device_state["mqtt_link"] = request.form.get('mqtt_link', '')
    device_state["mqtt_topic"] = request.form.get('mqtt_topic', '')
    device_state["mqtt_id"] = request.form.get('mqtt_id', '')
    device_state["mqtt_port"] = request.form.get('mqtt_port', '')
    print(f"📡 MQTT UPDATED: Link={device_state['mqtt_link']}")
    return "OK"

# --- INTERACTIVE CONTROL ENDPOINTS ---

@app.route('/InvSetFreq')
def set_freq():
    val = request.args.get('val', type=int)
    device_state["Inv_freq"] = str(val)
    return "OK"

@app.route('/InvSetDir')
def set_dir():
    device_state["Inv_dir"] = bool(request.args.get('val', type=int))
    return "OK"

@app.route('/MotorStart')
def motor_start():
    num = request.args.get('num', type=int)
    if num == 0:
        device_state["Inv_state"] = True
    if num in [1,2]: 
        device_state[f"Motor{num}_state"] = True
    return "OK"

@app.route('/MotorStop')
def motor_stop():
    num = request.args.get('num', type=int)
    if num == 0:
        device_state["Inv_state"] = False
    if num in [1,2]: 
        device_state[f"Motor{num}_state"] = False
    return "OK"

@app.route('/MotorSetDir')
def motor_set_dir():
    device_state["Inv_dir"] = bool(request.args.get('dir', type=int))
    return "OK"

@app.route('/setOutput<int:num>')
def set_out(num):
    device_state[f"output{num}_level"] = bool(request.args.get('val', type=int))
    return "OK"

@app.route('/reboot')
def reboot():
    print("🔄 REBOOTING...")
    return "OK"

if __name__ == '__main__':
    print("🚀 Server is running at: http://localhost:5000")
    app.run(port=5000, debug=True)
    get_config()