import paho.mqtt.client as mqtt
import time
import ssl

# --- Configuration ---
# REMOVE 'https://' and any trailing slashes
BROKER = "acf0f61e3365448686a08d6ba9f418d7.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "test/topic"  # Change this to the topic you want to watch
USER = "esp8266"  # Replace with your HiveMQ Cloud credentials
PASS = "Esp123456"  # Replace with your HiveMQ Cloud credentials
OUTPUT_FILE = "hivemq_cloud_log.txt"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Success! Connected to HiveMQ Cloud.")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Connection failed. Code: {rc}")
        if rc == 5:
            print("Hint: Check your Username and Password!")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    log_entry = f"[{time.strftime('%H:%M:%S')}] {msg.topic}: {payload}\n"
    print(log_entry, end="")
    with open(OUTPUT_FILE, "a") as f:
        f.write(log_entry)

# Setup Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

# --- CLOUD SPECIFIC SECURITY ---
client.username_pw_set(USER, PASS)
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2) # Required for Cloud
# -------------------------------

print(f"Connecting to {BROKER} on port {PORT}...")

try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"🛑 Error: {e}")