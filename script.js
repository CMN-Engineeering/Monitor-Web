// --- Navigation Logic ---
function showTab(tabName) {
    // Hide all views
    document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
    
    // Show selected
    document.getElementById('view-' + tabName).classList.add('active');
    
    // Highlight nav button
    if(tabName === 'dashboard') document.getElementById('nav-dash').classList.add('active');
    else document.getElementById('nav-set').classList.add('active');
}

// --- Core Functions ---
let isFwd = true;

function startMotor() { fetch('/setPower?val=1').then(r => { if(r.ok) alert("Inverter Power: ON"); }); }
function stopMotor() { fetch('/setPower?val=0').then(r => { if(r.ok) alert("Inverter Power: OFF"); }); }

function toggleDir() {
    isFwd = !isFwd;
    document.getElementById('dirLabel').innerText = isFwd ? "Quay Thuận" : "Quay Nghịch";
    const btn = document.getElementById('dirBtn');
    btn.className = isFwd ? "btn mt-2 medium dir-fwd" : "btn mt-2 medium dir-rev";
    fetch('/setDir?val=' + (isFwd ? 1 : 0));
}

function setFrequency() {
    let val = document.getElementById('freqSlider').value;
    fetch('/setFreq?val=' + val).then(r => { if(r.ok) alert("Đã đặt tần số: " + val + " Hz"); });
}

function updateOutputButton(btnId, state) {
    const btn = document.getElementById(btnId);
    btn.dataset.state = state ? '1' : '0';
    btn.innerHTML = state ? '<i class="fas fa-power-off"></i> BẬT' : '<i class="fas fa-power-off"></i> TẮT';
    btn.style.backgroundColor = state ? '#2ecc71' : '#e94560';
}

function toggleOutput1() {
    let s = document.getElementById('output1ToggleBtn').dataset.state === '1' ? 0 : 1;
    fetch('/setOutput1?val=' + s).then(r => { if(r.ok) updateOutputButton('output1ToggleBtn', s); });
}

function toggleOutput2() {
    let s = document.getElementById('output2ToggleBtn').dataset.state === '1' ? 0 : 1;
    fetch('/setOutput2?val=' + s).then(r => { if(r.ok) updateOutputButton('output2ToggleBtn', s); });
}

function computeGpioMask() {
    let m = 0;
    if (document.getElementById('input1Toggle').checked) m |= 1;
    if (document.getElementById('input2Toggle').checked) m |= 2;
    if (document.getElementById('output1Toggle').checked) m |= 4;
    if (document.getElementById('output2Toggle').checked) m |= 8;
    return m;
}

function confirmGpios() {
    let m = computeGpioMask();
    if(confirm('Xác nhận thay đổi GPIO?')) fetch('/setGpios?m=' + m);
}

function saveWifi() {
    let s = document.getElementById('wifi_name').value;
    let p = document.getElementById('wifi_pass').value;
    if(confirm("Lưu WiFi: " + s)) fetch('/saveWifi', { method: 'POST', body: `wifi_name=${s}&wifi_pass=${p}` });
}
function saveIP() {
    let s = document.getElementById('ap_name').value;
    let p = document.getElementById('ap_pass').value;
    if(confirm("Lưu Access Point: " + s)) fetch('/saveIP', { method: 'POST', body: `ap_name=${s}&ap_pass=${p}` });
}

function saveTimers() {
    let timers = [];
    for(let i=1; i<=4; i++) {
        let en = document.getElementById(`timer${i}_en`).checked ? 1 : 0;
        let on = document.getElementById(`timer${i}_on`).value;
        let off = document.getElementById(`timer${i}_off`).value;
        let out = (document.getElementById(`timer${i}_out1`).checked ? 1 : 0) | (document.getElementById(`timer${i}_out2`).checked ? 2 : 0);
        timers.push({id: i, en, on, off, out});
    }
    if(confirm("Lưu cài đặt 4 bộ hẹn giờ?")) {
        fetch('/saveTimers', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({timers}) });
    }
}

// --- UI Helpers ---
function togglePass() {
    let x = document.getElementById("pass");
    x.type = (x.type === "password") ? "text" : "password";
}
function toggleInput1Details() { document.getElementById('input1Details').style.display = document.getElementById('input1Toggle').checked ? 'block' : 'none'; }
function toggleInput2Details() { document.getElementById('input2Details').style.display = document.getElementById('input2Toggle').checked ? 'block' : 'none'; }
function toggleOutput1Controls() { document.getElementById('output1Controls').style.display = document.getElementById('output1Toggle').checked ? 'flex' : 'none'; }
function toggleOutput2Controls() { document.getElementById('output2Controls').style.display = document.getElementById('output2Toggle').checked ? 'flex' : 'none'; }

function updateBar(id, pct) {
    let bar = document.getElementById(id);
    bar.style.width = pct + '%';
    bar.className = pct > 80 ? 'progress-fill high' : (pct > 60 ? 'progress-fill warning' : 'progress-fill');
}

// --- Polling Loop (Runs forever) ---
setInterval(() => {
    fetch('/status')
    .then(r => r.json())
    .then(d => {
        // Connection Status
        document.getElementById('statusBadge').className = "badge online";
        document.getElementById('statusBadge').innerHTML = '<i class="fas fa-check-circle"></i> Đã kết nối';
        document.getElementById('ipDisplay').innerText = "IP: " + d.ip;
        document.getElementById('clock').innerText = d.time;

        // Dashboard Updates
        if(d.pwr) {
            document.getElementById('motorStatusLight').className = 'indicator-light running';
            document.getElementById('motorStatusText').innerText = 'CHẠY';
        } else {
            document.getElementById('motorStatusLight').className = 'indicator-light stopped';
            document.getElementById('motorStatusText').innerText = 'DỪNG';
        }
        
        isFwd = d.dir;
        document.getElementById('dirLabel').innerText = isFwd ? "Quay Thuận" : "Quay Nghịch";
        document.getElementById('dirBtn').className = isFwd ? "btn mt-2 medium dir-fwd" : "btn mt-2 medium dir-rev";
        
        document.getElementById('freqVal').innerText = d.freq;
        document.getElementById('memoryPercent').innerText = " " + d.ram_usage + " %";
        updateBar('memoryBar', d.ram_usage);
        document.getElementById('cpuPercent').innerText = " " + d.cpu_load + " %";
        updateBar('cpuBar', d.cpu_load);

        // Settings Updates (Sync if changed externally)
        updateOutputButton('output1ToggleBtn', d.output1);
        updateOutputButton('output2ToggleBtn', d.output2);
    })
    .catch(() => {
        document.getElementById('statusBadge').className = "badge offline";
        document.getElementById('statusBadge').innerHTML = '<i class="fas fa-times-circle"></i> Mất tín hiệu';
    });
}, 2000);

// --- Init (Load Config Once) ---
window.onload = function() {
    fetch('/get-config').then(r=>r.json()).then(d => {
        // Fill Settings Fields
        document.getElementById('ssid').value = d.ssid || "";
        document.getElementById('pass').value = d.pass || "";
        document.getElementById('freqSlider').value = d.freq;
        document.getElementById('freqSlider_val').innerText = d.freq;

        let mask = d.gpios ? parseInt(d.gpios) : 0;
        document.getElementById('input1Toggle').checked = !!(mask & 1);
        document.getElementById('input2Toggle').checked = !!(mask & 2);
        document.getElementById('output1Toggle').checked = !!(mask & 4);
        document.getElementById('output2Toggle').checked = !!(mask & 8);

        // Fill Timers
        for(let i=1; i<=4; i++) {
            if(d[`t${i}_en`] !== undefined) document.getElementById(`timer${i}_en`).checked = d[`t${i}_en`];
            if(d[`t${i}_on`]) document.getElementById(`timer${i}_on`).value = d[`t${i}_on`];
            if(d[`t${i}_off`]) document.getElementById(`timer${i}_off`).value = d[`t${i}_off`];
            let out = d[`t${i}_out`] || 0;
            document.getElementById(`timer${i}_out1`).checked = !!(out & 1);
            document.getElementById(`timer${i}_out2`).checked = !!(out & 2);
        }

        // Initial Visibility Toggle
        toggleInput1Details(); toggleInput2Details();
        toggleOutput1Controls(); toggleOutput2Controls();
    });
};