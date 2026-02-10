const http = require('http');
const fs = require('fs');
const path = require('path');
const mqtt = require('mqtt');
const { Server } = require('socket.io');

// 1. Configuration & Constants
const MQTT_BROKER = 'mqtt://192.168.1.120:1883';
const CONFIG_TOPIC = 'config'; // Topic for system settings
const STATUS_TOPIC = 'status'; // Topic for live sensor/motor data
const PORT = process.env.PORT || 3000;

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8'
};

// 2. Create HTTP Server (Existing file-serving logic)
const server = http.createServer((req, res) => {
  const urlPath = req.url.split('?')[0];
  let filePath = urlPath === '/' ? '/index.html' : urlPath;

  // Security: Do not serve server-side files
  if (filePath.endsWith('server.js') || filePath.endsWith('package.json')) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Not found');
    return;
  }

  filePath = path.join(__dirname, filePath);

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Not found');
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    const type = mimeTypes[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': type });
    fs.createReadStream(filePath).pipe(res);
  });
});

// 3. Initialize Socket.io
const io = new Server(server);

// 4. MQTT Client Logic
const mqttClient = mqtt.connect(MQTT_BROKER);

mqttClient.on('connect', () => {
  console.log('Connected to Mosquitto Broker at:', MQTT_BROKER);
  
  // Subscribe to the topics you want to use as configurations
  mqttClient.subscribe([CONFIG_TOPIC, STATUS_TOPIC], (err) => {
    if (!err) {
      console.log(`Subscribed to: ${CONFIG_TOPIC} and ${STATUS_TOPIC}`);
    }
  });
});

// 5. Bridge MQTT to WebSocket
mqttClient.on('message', (topic, message) => {
  try {
    const data = JSON.parse(message.toString());
    console.log(`MQTT [${topic}]:`, data);

    // Push the data to the browser dashboard via WebSockets
    if (topic === CONFIG_TOPIC) {
      io.emit('config_update', data);
    } else if (topic === STATUS_TOPIC) {
      io.emit('status_update', data);
    }
  } catch (e) {
    console.warn('Received non-JSON message on topic:', topic);
  }
});

// 6. Start the Server
server.listen(PORT, () => {
  console.log(`Monitor dashboard running on http://localhost:${PORT}`);
});