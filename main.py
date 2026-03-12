import paho.mqtt.client as mqtt

# --- Configuration ---
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "#" 
OUTPUT_FILE = "hivemq_log.txt"

# --- Callbacks ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully to {BROKER}")
        client.subscribe(TOPIC)
        print(f"Subscribed to: {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    log_entry = f"Topic: {msg.topic} | Message: {payload}\n"
    
    # Print to console so you see it live
    print(log_entry, end="")
    
    # Append to the text file
    with open(OUTPUT_FILE, "a") as f:
        f.write(log_entry)

# --- Setup Client ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER, PORT, 60)

# Keep the script running
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnecting...")
    client.disconnect()