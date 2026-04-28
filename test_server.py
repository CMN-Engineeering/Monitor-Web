from flask import Flask, send_file, jsonify, request
import random
import time
from datetime import datetime

app = Flask(__name__, static_folder='.')

# Trạng thái hệ thống giả lập
device_state = {
    "connected": True,
    "ip": "192.168.1.100",
    "factory_id": "HCMUT-ESP32-CUONG",
    
    # Motor Control Flow (Sơ đồ: Web Motor Contrl Enable & Type)
    "Motor_Control_Enable": True,
    "Motor_Type": "inverter",  # "inverter" hoặc "relay"
    
    # Inverter Status & Config (Sơ đồ: ID, Address, Model, Baudrate)
    "Inv_state": False,
    "Inv_dir": True,
    "Inv_freq": "45",
    "Inv_id": "1",
    "Inv_model": "1",
    "Inv_addr": "1",
    "Inv_baudrate": "9600",
    
    # Relay Config (Sơ đồ: Num of Motor, Pin assigned, Open Time)
    "Relay_NumMotors": "1",
    "Relay_StartPin": "12",
    "Relay_StopPin": "13",
    "Relay_OpenTime": "5",

    # IO Status
    "input1_state": False, "input2_state": True, "input3_state": True, "input4_state": False,
    "output1_level": False, "output2_level": False, "output3_level": False, "output4_level": False,

    # WiFi & MQTT
    "ssid": "VietHarvest_Office", "pass": "88888888", "sta_enable": True, "is_static": False,
    "mqtt_link": "broker.hivemq.com", "mqtt_port": "1883"
}

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/status')
def get_status():
    now = datetime.now()
    return jsonify({
        "time": now.strftime("%H:%M:%S"),
        "connected": device_state["connected"],
        "ip": device_state["ip"],
        "Inv_state": device_state["Inv_state"],
        "Inv_dir": device_state["Inv_dir"],
        "Inv_freq": device_state["Inv_freq"],
        "ram_usage": str(random.randint(40, 55)),
        "cpu_load": str(random.randint(10, 20)),
        "output1_level": device_state["output1_level"],
        "output2_level": device_state["output2_level"],
        "error_code": "0"
    })

@app.route('/get-config')
def get_config():
    return jsonify(device_state)

# --- LUỒNG ĐIỀU KHIỂN THEO FLOWCHART ---

@app.route('/MotorEn')
def set_motor_en():
    val = request.args.get('val', type=int)
    m_type = request.args.get('type', default="inverter")
    device_state["Motor_Control_Enable"] = bool(val)
    device_state["Motor_Type"] = m_type
    print(f"👉 MOTOR ENABLE: {val}, TYPE: {m_type}")
    return "OK"

@app.route('/InvCfg')
def set_inv_cfg():
    device_state["Inv_id"] = request.args.get('id')
    device_state["Inv_model"] = request.args.get('model')
    device_state["Inv_addr"] = request.args.get('addr')
    device_state["Inv_baudrate"] = request.args.get('baud')
    print("👉 INVERTER CONFIG SAVED. PENDING REBOOT.")
    return "OK"

@app.route('/RelayCfg')
def set_relay_cfg():
    device_state["Relay_NumMotors"] = request.args.get('num')
    device_state["Relay_StartPin"] = request.args.get('start')
    device_state["Relay_StopPin"] = request.args.get('stop')
    device_state["Relay_OpenTime"] = request.args.get('time')
    print("👉 RELAY CONFIG SAVED. PENDING REBOOT.")
    return "OK"

@app.route('/InvSetStart')
def set_power():
    val = request.args.get('val', type=int)
    device_state["Inv_state"] = bool(val)
    return "OK"

@app.route('/reboot')
def reboot():
    print("🔄 SYSTEM REBOOTING... INITIALIZING DRIVERS...")
    # Tại đây ESP32 sẽ thực hiện Init Inverter hoặc Init Relay tùy theo Motor_Type
    return "OK"

if __name__ == '__main__':
    app.run(port=5000, debug=True)