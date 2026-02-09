(function(){
const STORAGE='monitor_state';
function load(){
  try{return JSON.parse(localStorage.getItem(STORAGE)||'{}')}catch(e){return {}}
}
function save(o){localStorage.setItem(STORAGE,JSON.stringify(o))}

let state=load();
if(!state.io){
  state.io={
    inputMaster:0,
    outputMaster:0,
    inputs:[
      {on:0,timer:0,onSince:0},
      {on:0,timer:0,onSince:0},
      {on:0,timer:0,onSince:0},
      {on:0,timer:0,onSince:0}
    ],
    outputs:[
      {on:0,timer:0},
      {on:0,timer:0},
      {on:0,timer:0},
      {on:0,timer:0}
    ]
  };
}
state.io.inputs.forEach(function(inp){if(inp.onSince===undefined)inp.onSince=0;});
state.io.outputs.forEach(function(out){if(out.timer===undefined)out.timer=0;});
if(!state.motor){state.motor={running:0,speed:50,speedPending:50,direction:'forward'};}
if(!state.timers){
  state.timers=[
    {enabled:0,start:'08:00',end:'12:00',outputs:[]},
    {enabled:0,start:'12:00',end:'18:00',outputs:[]},
    {enabled:0,start:'18:00',end:'22:00',outputs:[]},
    {enabled:0,start:'22:00',end:'23:59',outputs:[]}
  ];
}
state.timers.forEach(function(t){if(!t.outputs)t.outputs=[];});
if(!state.network){
  state.network={ssid:'',password:'',ip:''};
}

function persist(){save(state);}

document.querySelectorAll('.nav-btn').forEach(function(btn){
  btn.onclick=function(){
    document.querySelectorAll('.nav-btn').forEach(function(b){b.classList.remove('active');});
    document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active');});
    btn.classList.add('active');
    document.getElementById(btn.dataset.page).classList.add('active');
  };
});

function formatRunTime(ms){
  if(!ms||ms<=0)return '0:00';
  var s=Math.floor(ms/1000),m=Math.floor(s/60),h=Math.floor(m/60);
  s%=60;m%=60;
  return (h?h+':':'')+(m<10&&h?'0':'')+m+':'+(s<10?'0':'')+s;
}

function renderIODash(){
  var el=document.getElementById('io-status-dash');
  var io=state.io;
  var now=Date.now();
  var html='';
  var inputLabels=['Input1','Input2','Input3','Input4'];
  var outputLabels=['Output1','Output2','Output3','Output4'];
  var inputs=io.inputMaster?io.inputs:io.inputs.map(function(){return {on:0,onSince:0};});
  inputs.forEach(function(inp,i){
    var on=inp.on;
    var runStr=on&&inp.onSince?formatRunTime(now-inp.onSince):'';
    html+='<div class="status-row"><span class="dot '+(on?'on':'off')+'"></span><span>'+inputLabels[i]+': '+(on?'ON':'OFF')+'</span>'+(runStr?'<span class="io-run-time">Running: '+runStr+'</span>':'')+'</div>';
  });
  var outputs=io.outputMaster?io.outputs:io.outputs.map(function(){return {on:0};});
  outputs.forEach(function(out,i){
    var on=out.on;
    html+='<div class="status-row"><span class="dot '+(on?'on':'off')+'"></span><span>'+outputLabels[i]+': '+(on?'ON':'OFF')+'</span></div>';
  });
  el.innerHTML=html;
}

function renderMotor(){
  var m=state.motor;
  var circle=document.getElementById('motor-circle');
  var label=document.getElementById('motor-label');
  circle.className='motor-circle '+(m.running?'running':'stopped');
  label.textContent=m.running?'Running':'Stopped';
  document.getElementById('motor-speed-big').textContent=m.speed;
  document.getElementById('speed-slider').value=m.speedPending;
  document.getElementById('speed-display').textContent=m.speed;
  document.getElementById('btn-forward').style.background=m.direction==='forward'?'#0d7377':'#2d3139';
  document.getElementById('btn-forward').style.color=m.direction==='forward'?'#fff':'#e4e6eb';
  document.getElementById('btn-backward').style.background=m.direction==='backward'?'#0d7377':'#2d3139';
  document.getElementById('btn-backward').style.color=m.direction==='backward'?'#fff':'#e4e6eb';
}

var speedSlider=document.getElementById('speed-slider');
if(speedSlider){
  speedSlider.oninput=function(){
    state.motor.speedPending=+this.value;
    document.getElementById('speed-display').textContent=this.value;
  };
}
var confirmSpeed=document.getElementById('btn-confirm-speed');
if(confirmSpeed){
  confirmSpeed.onclick=function(){
    state.motor.speed=state.motor.speedPending;
    renderMotor();
    persist();
  };
}
var btnStart=document.getElementById('btn-start');
if(btnStart){
  btnStart.onclick=function(){
    state.motor.running=1;
    renderMotor();
    persist();
  };
}
var btnStop=document.getElementById('btn-stop');
if(btnStop){
  btnStop.onclick=function(){
    state.motor.running=0;
    renderMotor();
    persist();
  };
}

var btnForward=document.getElementById('btn-forward');
if(btnForward){
  btnForward.onclick=function(){
    if(state.motor.running){
      document.getElementById('dir-warn').classList.add('show');
      return;
    }
    document.getElementById('dir-warn').classList.remove('show');
    state.motor.direction='forward';
    renderMotor();
    persist();
  };
}
var btnBackward=document.getElementById('btn-backward');
if(btnBackward){
  btnBackward.onclick=function(){
    if(state.motor.running){
      document.getElementById('dir-warn').classList.add('show');
      return;
    }
    document.getElementById('dir-warn').classList.remove('show');
    state.motor.direction='backward';
    renderMotor();
    persist();
  };
}

function renderTimerDash(){
  var el=document.getElementById('timer-dash');
  var html='';
  state.timers.forEach(function(t,i){
    if(!t.enabled)return;
    var outList=(t.outputs||[]).length?(t.outputs||[]).map(function(o){return 'Output'+(o+1);}).join(', '):'—';
    html+='<div class="timer-item enabled"><span class="dot on"></span><span>Timer '+(i+1)+': '+t.start+' – '+t.end+'</span><span class="timer-outputs"> → '+outList+'</span></div>';
  });
  if(!html)el.innerHTML='<div class="timer-item">No timers enabled</div>';
  else el.innerHTML=html;
}

function renderIOSettings(){
  var el=document.getElementById('io-settings');
  var io=state.io;
  var html='<div class="io-grid">';
  ['Input1','Input2','Input3','Input4'].forEach(function(l,i){
    var item=io.inputs[i]||{on:0,timer:0};
    html+='<div class="io-item"><label>'+l+'</label><div class="switch '+(item.on?'on':'')+'" data-type="input" data-i="'+i+'" data-f="on"></div><button class="btn" data-type="input" data-i="'+i+'" data-f="timer">Timer</button></div>';
  });
  ['Output1','Output2','Output3','Output4'].forEach(function(l,i){
    var item=io.outputs[i]||{on:0,timer:0};
    html+='<div class="io-item"><label>'+l+'</label><div class="switch '+(item.on?'on':'')+'" data-type="output" data-i="'+i+'" data-f="on"></div><button class="btn" data-type="output" data-i="'+i+'" data-f="timer">Timer</button></div>';
  });
  el.innerHTML=html+'</div>';
  el.querySelectorAll('.switch[data-type]').forEach(function(sw){
    sw.onclick=function(){
      if(sw.dataset.f!=='on')return;
      var arr=sw.dataset.type==='input'?state.io.inputs:state.io.outputs;
      var i=+sw.dataset.i;
      var master=sw.dataset.type==='input'?state.io.inputMaster:state.io.outputMaster;
      if(!master)return;
      arr[i]=arr[i]||{on:0,timer:0,onSince:0};
      var isInput=sw.dataset.type==='input';
      if(arr[i].on){arr[i].on=0;if(isInput)arr[i].onSince=0;}
      else{arr[i].on=1;if(isInput)arr[i].onSince=Date.now();}
      sw.classList.toggle('on',!!arr[i].on);
      persist();
      renderIODash();
    };
  });
  el.querySelectorAll('.btn[data-f="timer"]').forEach(function(btn){
    var arr=btn.dataset.type==='input'?state.io.inputs:state.io.outputs;
    var i=+btn.dataset.i;
    btn.style.background=arr[i].timer?'#0d7377':'';
    btn.style.color=arr[i].timer?'#fff':'';
    btn.onclick=function(){
      arr[i].timer=arr[i].timer?0:1;
      this.style.background=arr[i].timer?'#0d7377':'';
      this.style.color=arr[i].timer?'#fff':'';
      persist();
    };
  });
}

var inputMaster=document.getElementById('input-master');
if(inputMaster){
  inputMaster.onclick=function(){
    state.io.inputMaster=state.io.inputMaster?0:1;
    this.dataset.on=state.io.inputMaster;
    this.classList.toggle('on',!!state.io.inputMaster);
    if(!state.io.inputMaster){
      state.io.inputs.forEach(function(item){item.on=0;item.onSince=0;});
      renderIOSettings();
    }
    persist();
    renderIODash();
  };
  inputMaster.classList.toggle('on',!!state.io.inputMaster);
}

var outputMaster=document.getElementById('output-master');
if(outputMaster){
  outputMaster.onclick=function(){
    state.io.outputMaster=state.io.outputMaster?0:1;
    this.dataset.on=state.io.outputMaster;
    this.classList.toggle('on',!!state.io.outputMaster);
    if(!state.io.outputMaster){
      state.io.outputs.forEach(function(item){item.on=0;});
      renderIOSettings();
    }
    persist();
    renderIODash();
  };
  outputMaster.classList.toggle('on',!!state.io.outputMaster);
}

function renderTimerSettings(){
  var el=document.getElementById('timer-settings');
  el.innerHTML=state.timers.map(function(t,i){
    var outputs=(t.outputs||[]).slice();
    var outHtml=['<div class="time-row"><label>Outputs</label><span class="timer-outputs">'];
    [0,1,2,3].forEach(function(o){
      var checked=outputs.indexOf(o)>=0?' checked':'';
      outHtml.push('<label><input type="checkbox" data-i="'+i+'" data-o="'+o+'"'+checked+'> Output'+(o+1)+'</label> ');
    });
    outHtml.push('</span></div>');
    return '<div class="timer-block"><h4>Timer '+(i+1)+'</h4><div class="time-row"><label>Start</label><input type="time" value="'+t.start+'" data-i="'+i+'" data-f="start"></div><div class="time-row"><label>End</label><input type="time" value="'+t.end+'" data-i="'+i+'" data-f="end"></div><div class="toggle-row"><label>Enable</label><div class="switch '+(t.enabled?'on':'')+'" data-i="'+i+'"></div></div>'+outHtml.join('')+'</div>';
  }).join('');
  el.querySelectorAll('input[type=time]').forEach(function(inp){
    inp.onchange=function(){
      state.timers[+this.dataset.i][this.dataset.f]=this.value;
      persist();
      renderTimerDash();
    };
  });
  el.querySelectorAll('.timer-block .switch').forEach(function(sw){
    sw.onclick=function(){
      var i=+this.dataset.i;
      state.timers[i].enabled=state.timers[i].enabled?0:1;
      this.classList.toggle('on',!!state.timers[i].enabled);
      persist();
      renderTimerDash();
    };
  });
  el.querySelectorAll('.timer-block input[type=checkbox]').forEach(function(cb){
    cb.onchange=function(){
      var i=+this.dataset.i,o=+this.dataset.o;
      var arr=state.timers[i].outputs=state.timers[i].outputs||[];
      var idx=arr.indexOf(o);
      if(this.checked){if(idx<0)arr.push(o);}
      else if(idx>=0)arr.splice(idx,1);
      persist();
      renderTimerDash();
      applyTimers();
      renderIODash();
    };
  });
}

function timeToMinutes(str){
  var p=str.split(':');
  return (parseInt(p[0],10)||0)*60+(parseInt(p[1],10)||0);
}

function applyTimers(){
  var now=new Date();
  var min=now.getHours()*60+now.getMinutes();
  var outputActive={};
  state.timers.forEach(function(t){
    if(!t.enabled||!t.outputs||!t.outputs.length)return;
    var startM=timeToMinutes(t.start);
    var endM=timeToMinutes(t.end);
    var active=startM<=endM?(min>=startM&&min<endM):(min>=startM||min<endM);
    t.outputs.forEach(function(o){
      if(active)outputActive[o]=true;
    });
  });
  for(var o=0;o<4;o++){
    var controlled=state.timers.some(function(t){
      return t.enabled&&t.outputs&&t.outputs.indexOf(o)>=0;
    });
    if(controlled){
      state.io.outputs[o]=state.io.outputs[o]||{on:0,timer:0};
      state.io.outputs[o].on=outputActive[o]?1:0;
    }
  }
}

function updateTime(){
  var el=document.getElementById('current-time');
  if(el)el.textContent=new Date().toLocaleTimeString();
  applyTimers();
  renderIODash();
}
setInterval(updateTime,1000);

function initWifi(){
  var ssidEl=document.getElementById('wifi-ssid');
  if(!ssidEl)return;
  var pwdEl=document.getElementById('wifi-password');
  var ipEl=document.getElementById('wifi-ip');
  var statusEl=document.getElementById('wifi-status');
  ssidEl.value=state.network.ssid||'';
  pwdEl.value=state.network.password||'';
  if(state.network.ip){
    ipEl.value=state.network.ip;
  }else{
    var host=window.location.hostname||window.location.host||'';
    ipEl.value=host;
    state.network.ip=host;
  }
  var saveBtn=document.getElementById('wifi-save');
  if(saveBtn){
    saveBtn.onclick=function(){
      state.network.ssid=ssidEl.value.trim();
      state.network.password=pwdEl.value;
      state.network.ip=ipEl.value.trim();
      persist();
      if(statusEl)statusEl.textContent='WiFi settings saved locally in this browser.';
    };
  }
}

updateTime();
renderIODash();
renderMotor();
renderTimerDash();
renderIOSettings();
renderTimerSettings();
initWifi();
})();
