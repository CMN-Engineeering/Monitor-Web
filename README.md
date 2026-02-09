# Monitor Dashboard (Web UI)

Small, self-contained monitoring dashboard for a single device. Everything runs in the browser, with optional Node.js static server.

## Features

- **Dashboard**
  - Input/Output status with colored dots.
  - Per-input **run time counter** showing how long each input has been ON.
  - Motor control card with speed slider, direction, and a large status circle (Running/Stopped).
  - Timer display showing enabled timers and which outputs they control.

- **Settings**
  - **Input / Output settings** with master switches and per-channel toggles.
  - **Timers (4)** with start/end times and assigned outputs; timers can drive outputs ON/OFF based on the current time.
  - **WiFi configuration**: SSID, password, and device IP, stored locally in the browser via `localStorage` (no real network configuration is performed).

- **Persistence**
  - All state (IO, motor, timers, WiFi form) is saved in `localStorage` under the key `monitor_state`.

## Project structure

- `index.html` – single-page app markup and main script.
- `styles.css` – layout and visual styles.
- `server.js` – tiny Node.js static file server for local hosting.

Total project size is kept well under **100 KB** (no external libraries or `node_modules`).

## Running the app

From the project directory (`/home/cmn01/monitor-web`):

### Node.js server (recommended)

```bash
node server.js
```

Then open `http://localhost:3000` in your browser.

## Notes

- WiFi settings in the Settings page are **purely UI** and stored only in the browser; they do **not** actually configure real WiFi on any hardware.
- To reset everything, clear the browser’s `localStorage` for this origin.
