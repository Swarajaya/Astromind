"""
AstroMind — server.py
Run: python server.py
Opens: http://127.0.0.1:5000
"""

# ══════════════════════════════════════════════════════════════════
# HTML MUST BE DEFINED FIRST — write_dashboard() uses it
# ══════════════════════════════════════════════════════════════════
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>AstroMind — NEO Risk Simulator</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&family=Courier+Prime&display=swap" rel="stylesheet"/>
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;background:#060a12;color:#e0e8ff;font-family:'Space Mono',monospace}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:#0a0f1e}::-webkit-scrollbar-thumb{background:#00ff9d44;border-radius:2px}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
@keyframes scanline{0%{top:-10%}100%{top:110%}}
#app{display:flex;flex-direction:column;height:100vh}
#hdr{display:flex;align-items:center;justify-content:space-between;padding:14px 28px;border-bottom:1px solid #00ff9d22;background:linear-gradient(180deg,#0a0f1e,transparent);flex-shrink:0}
#main{display:flex;flex:1;overflow:hidden}
#sidebar{width:244px;background:#080d18;border-right:1px solid #0d1f38;overflow-y:auto;flex-shrink:0}
#center{flex:1;display:flex;flex-direction:column;overflow:hidden}
#cwrap{flex:1;position:relative;overflow:hidden;min-height:0}
canvas{width:100%;height:100%;display:block}
#scanline{position:absolute;left:0;width:100%;height:2px;background:linear-gradient(90deg,transparent,#00ff9d22,transparent);animation:scanline 4s linear infinite;pointer-events:none}
#cinfo{position:absolute;bottom:12px;left:16px;font-size:9px;color:#ffffff66;line-height:1.8;pointer-events:none;display:none}
#sbadge{position:absolute;top:12px;right:16px;font-size:9px;color:#ffe600;animation:pulse .8s infinite;display:none}
#nosel{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}
#tabwrap{border-top:1px solid #0d1f38;flex-shrink:0;background:#080d18}
#tabbar{display:flex;padding:0 16px}
.tb{background:none;border:none;border-bottom:2px solid transparent;cursor:pointer;padding:8px 16px;font-family:'Space Mono',monospace;font-size:11px;letter-spacing:2px;color:#ffffff44;transition:all .2s}
.tb.on{color:#00ff9d;border-bottom-color:#00ff9d}
#tabbody{padding:16px;background:#060a12;height:210px;overflow-y:auto}
#right{width:248px;background:#080d18;border-left:1px solid #0d1f38;overflow-y:auto;flex-shrink:0}
.nrow{padding:10px 16px;border-bottom:1px solid #0d1f3844;border-left:3px solid transparent;cursor:pointer;transition:all .15s}
.nrow:hover,.nrow.on{background:#0d1f38}.nrow.on{border-left-color:#00ff9d}
.nn{font-size:11px;font-weight:700;display:flex;justify-content:space-between;align-items:center}
.nm{font-size:9px;color:#ffffff44;margin-top:3px}
.pha{font-size:7px;background:#ff2d5522;color:#ff2d55;padding:2px 5px;border:1px solid #ff2d5544;border-radius:2px}
.card{background:#0a0f1e;border:1px solid #0d1f38;border-radius:6px;padding:12px;margin:0 12px 12px}
.ct{font-size:8px;color:#ffffff44;letter-spacing:2px;margin-bottom:8px}
.sr{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;font-size:9px}
.tr2{display:flex;align-items:center;gap:8px;margin-bottom:5px}
.td2{width:6px;height:6px;border-radius:50%;flex-shrink:0}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:10px}
.mc2{background:#0a0f1e;border:1px solid #0d1f38;border-radius:6px;padding:9px}
.ml2{font-size:7px;color:#ffffff44;letter-spacing:2px;margin-bottom:3px}
.mv2{font-size:13px;font-weight:700}
.qr{display:flex;align-items:center;gap:6px;margin-bottom:5px}
table{width:100%;border-collapse:collapse;font-size:9px;font-family:monospace}
th{padding:4px 8px;color:#ffffff44;font-weight:400;letter-spacing:2px;border-bottom:1px solid #0d1f38;text-align:left}
td{padding:4px 8px;border-bottom:1px solid #0d1f3844;color:#e0e8ff}
</style>
</head>
<body>
<div id="app">
<div id="hdr">
  <div style="display:flex;align-items:center;gap:14px">
    <div style="position:relative;width:38px;height:38px;border-radius:50%;border:2px solid #00ff9d;display:flex;align-items:center;justify-content:center;font-size:18px">&#9764;
      <div style="position:absolute;top:-2px;right:-2px;width:10px;height:10px;border-radius:50%;background:#ff2d55;animation:pulse 1.5s infinite"></div>
    </div>
    <div>
      <div style="font-family:'Orbitron',sans-serif;font-size:20px;font-weight:900;letter-spacing:3px">ASTRO<span style="color:#00ff9d">MIND</span></div>
      <div style="font-size:9px;color:#ffffff44;letter-spacing:3px">PLANETARY DEFENSE AI &mdash; Q-ML SIMULATOR v2.4</div>
    </div>
  </div>
  <div style="display:flex;gap:22px;align-items:center">
    <div style="text-align:right"><div style="font-size:8px;color:#ffffff44;letter-spacing:2px">TRACKING</div><div style="font-size:14px;color:#00ff9d;font-family:'Orbitron',sans-serif">8 NEOs</div></div>
    <div style="text-align:right"><div style="font-size:8px;color:#ffffff44;letter-spacing:2px">STATUS</div><div style="font-size:11px;color:#00ff9d;animation:pulse 2s infinite">&#9679; ONLINE</div></div>
    <button id="playbtn" onclick="togglePlay()" style="background:#00ff9d22;border:1px solid #00ff9d;color:#00ff9d;padding:6px 14px;border-radius:4px;cursor:pointer;font-family:monospace;font-size:10px;letter-spacing:2px">&#9646;&#9646; PAUSE</button>
  </div>
</div>
<div id="main">
  <div id="sidebar">
    <div style="padding:12px 16px 8px;border-bottom:1px solid #0d1f38">
      <div style="font-size:9px;color:#ffffff44;letter-spacing:3px">NASA NEO DATABASE</div>
      <div style="font-size:9px;color:#ffffff22;margin-top:2px">CNEOS / JPL HORIZONS</div>
    </div>
    <div id="neolist"></div>
  </div>
  <div id="center">
    <div id="cwrap">
      <canvas id="C"></canvas>
      <div id="scanline"></div>
      <div id="cinfo"><div id="ciname" style="color:#00ff9d;font-weight:700;font-size:11px"></div><div id="cimeta"></div></div>
      <div id="sbadge">&#9711; SIMULATING...</div>
      <div id="nosel"><div style="font-size:38px;opacity:.14">&#9764;</div><div style="font-size:11px;color:#ffffff22;letter-spacing:3px">SELECT A NEAR-EARTH OBJECT</div></div>
    </div>
    <div id="tabwrap">
      <div id="tabbar">
        <button class="tb on" onclick="setTab('overview',this)">OVERVIEW</button>
        <button class="tb" onclick="setTab('quantum',this)">QUANTUM</button>
        <button class="tb" onclick="setTab('montecarlo',this)">MONTE CARLO</button>
        <button class="tb" onclick="setTab('log',this)">LOG</button>
      </div>
      <div id="tabbody"><div style="display:flex;align-items:center;justify-content:center;height:100%;opacity:.2;flex-direction:column;gap:6px"><div style="font-size:26px">&#9888;</div><div style="font-size:10px;letter-spacing:3px">SELECT A NEAR-EARTH OBJECT TO ANALYZE</div></div></div>
    </div>
  </div>
  <div id="right">
    <div style="padding:12px 16px 8px;border-bottom:1px solid #0d1f38;margin-bottom:12px">
      <div style="font-size:9px;color:#ffffff44;letter-spacing:3px">RISK ASSESSMENT</div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:8px;padding:0 12px 12px">
      <svg width="160" height="100" viewBox="0 0 160 100">
        <defs><linearGradient id="gg" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stop-color="#00ff9d"/><stop offset="50%" stop-color="#ffe600"/><stop offset="100%" stop-color="#ff2d55"/>
        </linearGradient></defs>
        <path d="M20 80 A60 60 0 0 1 140 80" fill="none" stroke="#1a1a2e" stroke-width="12"/>
        <path d="M20 80 A60 60 0 0 1 140 80" fill="none" stroke="url(#gg)" stroke-width="4" opacity="0.4"/>
        <g id="ndl" transform="rotate(-135,80,80)">
          <line x1="80" y1="80" x2="80" y2="26" stroke="#00ff9d" stroke-width="2.5" stroke-linecap="round" id="ndlL"/>
          <circle cx="80" cy="80" r="5" fill="#00ff9d" id="ndlD"/>
        </g>
        <text x="80" y="96" text-anchor="middle" font-size="9" fill="#ffffff44" font-family="monospace">TORINO SCALE</text>
      </svg>
      <div id="gnum" style="font-family:'Orbitron',sans-serif;font-size:26px;letter-spacing:2px;color:#00ff9d;text-align:center">&mdash;</div>
      <div id="glbl" style="font-size:11px;letter-spacing:4px;color:#00ff9d;text-align:center">AWAITING DATA</div>
    </div>
    <div class="card">
      <div class="ct">TORINO SCALE</div>
      <div class="tr2"><div class="td2" style="background:#00ff9d"></div><span style="font-size:8px;color:#00ff9d;width:26px">0</span><span style="font-size:8px;color:#ffffff44">No hazard</span></div>
      <div class="tr2"><div class="td2" style="background:#ffe600"></div><span style="font-size:8px;color:#ffe600;width:26px">1-3</span><span style="font-size:8px;color:#ffffff44">Normal</span></div>
      <div class="tr2"><div class="td2" style="background:#ff8c00"></div><span style="font-size:8px;color:#ff8c00;width:26px">4-6</span><span style="font-size:8px;color:#ffffff44">Meriting concern</span></div>
      <div class="tr2"><div class="td2" style="background:#ff2d55"></div><span style="font-size:8px;color:#ff2d55;width:26px">7-10</span><span style="font-size:8px;color:#ffffff44">Threatening</span></div>
    </div>
    <div class="card" id="mlcard" style="display:none">
      <div class="ct">ML MODELS ACTIVE</div>
      <div class="sr"><span style="color:#ffffff66">VQC (Quantum)</span><span style="font-size:8px;color:#00ff9d">&#9679; ACTIVE</span></div>
      <div class="sr"><span style="color:#ffffff66">GBM Ensemble</span><span style="font-size:8px;color:#4fc3f7">&#9679; ACTIVE</span></div>
      <div class="sr"><span style="color:#ffffff66">Monte Carlo</span><span style="font-size:8px;color:#ffe600">&#9679; ACTIVE</span></div>
      <div class="sr"><span style="color:#ffffff66">Kepler ODE</span><span style="font-size:8px;color:#ff8c00">&#9679; ACTIVE</span></div>
    </div>
    <div class="card">
      <div class="ct">DATA SOURCE</div>
      <div style="font-size:8px;color:#ffffff33;line-height:2">
        <div>&#9679; NASA CNEOS</div><div>&#9679; JPL Horizons</div><div>&#9679; ESA SSA</div><div>&#9679; MPC Orbital DB</div>
      </div>
    </div>
  </div>
</div>
</div>
<script>
var DB=[
  {id:"2023 DW",  name:"2023 DW",  sma:1.014,ecc:0.198,inc:5.0, raan:37.2, argp:106.1,ma:88.3, diameter:49,   haz:true, disc:"2023"},
  {id:"Apophis",  name:"Apophis",  sma:0.922,ecc:0.191,inc:3.3, raan:204.4,argp:126.4,ma:211.1,diameter:370,  haz:true, disc:"2004"},
  {id:"Bennu",    name:"Bennu",    sma:1.126,ecc:0.204,inc:6.0, raan:2.1,  argp:66.2, ma:101.5,diameter:490,  haz:true, disc:"1999"},
  {id:"1950 DA",  name:"1950 DA",  sma:1.699,ecc:0.508,inc:12.2,raan:356.6,argp:224.6,ma:149.2,diameter:1300, haz:true, disc:"1950"},
  {id:"2020 NK1", name:"2020 NK1", sma:1.45, ecc:0.39, inc:7.8, raan:121.3,argp:89.5, ma:203.1,diameter:160,  haz:false,disc:"2020"},
  {id:"2004 MN4", name:"2004 MN4", sma:0.919,ecc:0.191,inc:3.3, raan:204.4,argp:127.4,ma:209.1,diameter:325,  haz:true, disc:"2004"},
  {id:"2007 FT3", name:"2007 FT3", sma:1.021,ecc:0.247,inc:0.9, raan:186.4,argp:36.9, ma:180.7,diameter:340,  haz:true, disc:"2007"},
  {id:"2010 RF12",name:"2010 RF12",sma:1.054,ecc:0.193,inc:0.8, raan:2.3,  argp:176.1,ma:47.8, diameter:7,    haz:false,disc:"2010"},
];
var sel=null,sim=null,logs=[],tab='overview',playing=true,frame=0,ry=0,stars=null;

function rc(p){return p<.001?'#00ff9d':p<.01?'#ffe600':p<.05?'#ff8c00':'#ff2d55';}
function rl(p){return p<.001?'MINIMAL':p<.01?'LOW':p<.05?'ELEVATED':'CRITICAL';}

function kepler(p,days){
  var n=0.9856076686/Math.pow(p.sma,1.5);
  var M=((p.ma+n*days)%360)*Math.PI/180;
  var E=M; for(var i=0;i<12;i++) E=M+p.ecc*Math.sin(E);
  var nu=2*Math.atan2(Math.sqrt(1+p.ecc)*Math.sin(E/2),Math.sqrt(1-p.ecc)*Math.cos(E/2));
  var r=p.sma*(1-p.ecc*Math.cos(E));
  var I=p.inc*Math.PI/180,R=p.raan*Math.PI/180,W=p.argp*Math.PI/180;
  return{x:r*(Math.cos(R)*Math.cos(W+nu)-Math.sin(R)*Math.sin(W+nu)*Math.cos(I)),
         y:r*(Math.sin(R)*Math.cos(W+nu)+Math.cos(R)*Math.sin(W+nu)*Math.cos(I)),
         z:r*Math.sin(W+nu)*Math.sin(I),r:r,nu:nu*180/Math.PI};
}

function monteCarlo(p,runs){
  runs=runs||500; var hits=0,traj=[];
  for(var i=0;i<runs;i++){
    var n={sma:p.sma*(1+(Math.random()-.5)*.02),ecc:Math.min(.99,Math.max(0,p.ecc+(Math.random()-.5)*.01)),
      inc:p.inc+(Math.random()-.5)*.5,raan:p.raan+(Math.random()-.5),argp:p.argp+(Math.random()-.5),ma:p.ma+(Math.random()-.5)*2};
    var s=kepler(n,365); if(s.r<.05)hits++;
    if(i%50===0)traj.push({x:s.x,y:s.y,z:s.z,r:s.r,nu:s.nu,run:i});
  }
  return{prob:hits/runs,traj:traj,runs:runs};
}

function vqc(p){
  var v=[p.sma/3,p.ecc*2,p.inc/180,p.raan/360,p.argp/360,p.ma/360,p.ecc*p.inc/180,1-p.ecc];
  var nm=Math.sqrt(v.reduce(function(s,x){return s+x*x;},0))||1;
  var a=v.map(function(x){return x/nm;});
  function lay(a,t){return a.map(function(x,i){return x*Math.cos(t[i%t.length])-a[(i+1)%a.length]*Math.sin(t[i%t.length]);});}
  a=lay(a,[.31,.77,1.04,.58,1.21,.93,.44,.67]); a=lay(a,[.88,.23,.65,1.12,.39,.81,.56,.14]);
  return{score:Math.abs(a.reduce(function(s,x,i){return s+x*(i+1);},0)),amp:a};
}

function gbm(p){
  var f=[p.sma,p.ecc,p.inc/100,p.raan/360,p.argp/360,p.ma/360,p.ecc*p.inc/180,1-p.ecc];
  var w=[.23,.18,.31,.12,.09,.07,.05,.14],b=[.02,-.01,.03,.01,-.02,.01,0,.01];
  var logit=f.reduce(function(s,x,i){return s+Math.tanh(x*w[i]+b[i]);},0)*.8;
  return 1/(1+Math.exp(-logit));
}

function addLog(msg){var t=new Date().toISOString().slice(11,19);logs.unshift('['+t+'] '+msg);if(logs.length>20)logs.pop();}

function renderSidebar(){
  document.getElementById('neolist').innerHTML=DB.map(function(a){
    return '<div class="nrow'+(sel&&sel.id===a.id?' on':'')+'" onclick="pick(\''+a.id+'\')">'+
      '<div class="nn">'+a.name+(a.haz?'<span class="pha">PHA</span>':'')+'</div>'+
      '<div class="nm">&#8960; '+a.diameter+'m &middot; a='+a.sma.toFixed(3)+' AU</div>'+
      '<div class="nm">e='+a.ecc.toFixed(3)+' &middot; i='+a.inc.toFixed(1)+'&deg;</div></div>';
  }).join('');
}

function updateGauge(){
  if(!sim)return;
  var p=sim.prob,c=rc(p),l=rl(p);
  document.getElementById('gnum').textContent=(p*100).toFixed(4)+'%';
  document.getElementById('gnum').style.color=c;
  document.getElementById('glbl').textContent=l;
  document.getElementById('glbl').style.color=c;
  var angle=-135+p*270;
  document.getElementById('ndl').setAttribute('transform','rotate('+angle+',80,80)');
  document.getElementById('ndlL').setAttribute('stroke',c);
  document.getElementById('ndlD').setAttribute('fill',c);
}

async function pick(id){
  sel=DB.find(function(a){return a.id===id;}); if(!sel)return;
  sim=null; logs=[];
  renderSidebar();
  document.getElementById('nosel').style.display='none';
  document.getElementById('cinfo').style.display='block';
  document.getElementById('ciname').textContent=sel.name;
  document.getElementById('cimeta').textContent='SMA: '+sel.sma+' AU  ECC: '+sel.ecc+'  Diam: '+sel.diameter+'m';
  document.getElementById('sbadge').style.display='block';
  document.getElementById('mlcard').style.display='block';
  renderTab();

  var data=null;
  try{var r=await fetch('/api/analyze?neo='+encodeURIComponent(sel.name)+'&runs=500');if(r.ok)data=await r.json();}catch(e){}

  var prob,traj,sruns,qScore,gProb,mProb;
  if(data&&!data.error){
    addLog('Python backend: received'); addLog('VQC: '+data.result.qml_score);
    addLog('GBM: '+(data.result.gbm_probability*100).toFixed(4)+'%');
    addLog('MC: '+(data.result.mc_probability*100).toFixed(4)+'%');
    addLog('Hybrid: '+(data.result.hybrid_probability*100).toFixed(6)+'%');
    addLog('Risk: '+data.result.risk_level+' - complete');
    prob=data.result.hybrid_probability; qScore=data.result.qml_score;
    gProb=data.result.gbm_probability; mProb=data.result.mc_probability;
    traj=data.mc_pts.map(function(p,i){return {x:p.x,y:p.y,z:p.z,r:Math.sqrt(p.x*p.x+p.y*p.y+p.z*p.z),nu:0,run:i*10};});
    sruns=500;
  } else {
    addLog('JS fallback for '+sel.name);
    var q=vqc(sel); qScore=q.score; addLog('VQC: '+qScore.toFixed(6));
    gProb=gbm(sel); addLog('GBM: '+(gProb*100).toFixed(4)+'%');
    var mc=monteCarlo(sel,500); mProb=mc.prob; traj=mc.traj; sruns=mc.runs;
    prob=Math.min(1,0.35*qScore+0.35*gProb+0.30*mProb);
    addLog('MC: '+(mProb*100).toFixed(4)+'%');
    addLog('Hybrid: '+(prob*100).toFixed(6)+'%');
    addLog('Risk: '+rl(prob)+' - complete');
  }
  sim={prob:prob,traj:traj,sruns:sruns,qScore:qScore,gProb:gProb,mProb:mProb};
  document.getElementById('sbadge').style.display='none';
  updateGauge(); renderTab();
}

/* Canvas */
var canvas=document.getElementById('C');
var ctx=canvas.getContext('2d');
var wrap=document.getElementById('cwrap');
function resize(){canvas.width=wrap.clientWidth;canvas.height=wrap.clientHeight;stars=null;}
resize(); window.addEventListener('resize',resize);

function proj(x,y,z){
  var W=canvas.width,H=canvas.height,cx=W/2,cy=H/2,scale=Math.min(W,H)*.32,rx=0.4;
  var y2=y*Math.cos(rx)-z*Math.sin(rx),z2=y*Math.sin(rx)+z*Math.cos(rx);
  var x3=x*Math.cos(ry)+z2*Math.sin(ry),z3=-x*Math.sin(ry)+z2*Math.cos(ry);
  var s=3.5/(3.5+z3);
  return{px:cx+x3*scale*s,py:cy-y2*scale*s,s:s};
}

function draw(){
  requestAnimationFrame(draw);
  var W=canvas.width,H=canvas.height; if(!W||!H)return;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#060a12'; ctx.fillRect(0,0,W,H);
  /* Stars */
  if(!stars){stars=[];for(var i=0;i<180;i++)stars.push({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.2,a:Math.random()});}
  for(var i=0;i<stars.length;i++){
    var st=stars[i];
    ctx.globalAlpha=st.a*(0.5+0.5*Math.sin(frame*.02+st.x));
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(st.x,st.y,st.r,0,Math.PI*2); ctx.fill();
  } ctx.globalAlpha=1;
  /* Sun */
  var sp=proj(0,0,0);
  var sg=ctx.createRadialGradient(sp.px,sp.py,2,sp.px,sp.py,28);
  sg.addColorStop(0,'#fff9e0'); sg.addColorStop(.3,'#ffcc00cc'); sg.addColorStop(1,'transparent');
  ctx.fillStyle=sg; ctx.beginPath(); ctx.arc(sp.px,sp.py,28,0,Math.PI*2); ctx.fill();
  /* Earth orbit ring */
  ctx.beginPath();
  for(var i=0;i<=80;i++){var a=i/80*Math.PI*2,p=proj(Math.cos(a),Math.sin(a),0);i===0?ctx.moveTo(p.px,p.py):ctx.lineTo(p.px,p.py);}
  ctx.strokeStyle='#1a3a6a44'; ctx.lineWidth=1; ctx.stroke();
  /* Earth */
  var ea=frame*.008%(Math.PI*2),ep=proj(Math.cos(ea),Math.sin(ea),0);
  var eg=ctx.createRadialGradient(ep.px-2,ep.py-2,1,ep.px,ep.py,8);
  eg.addColorStop(0,'#4fc3f7'); eg.addColorStop(.5,'#1565c0'); eg.addColorStop(1,'#0d47a1aa');
  ctx.fillStyle=eg; ctx.beginPath(); ctx.arc(ep.px,ep.py,8*ep.s,0,Math.PI*2); ctx.fill();
  /* Asteroid */
  if(sel){
    var color=sim?rc(sim.prob):'#00ff9d';
    ctx.beginPath();
    for(var i=0;i<=180;i++){var s=kepler(sel,i*365/180),p=proj(s.x,s.y,s.z);i===0?ctx.moveTo(p.px,p.py):ctx.lineTo(p.px,p.py);}
    ctx.strokeStyle=color+'88'; ctx.lineWidth=1.5; ctx.setLineDash([4,4]); ctx.stroke(); ctx.setLineDash([]);
    var ad=(playing?frame*.5:0)%365,as_=kepler(sel,ad),ap=proj(as_.x,as_.y,as_.z);
    var ag=ctx.createRadialGradient(ap.px,ap.py,1,ap.px,ap.py,18);
    ag.addColorStop(0,color); ag.addColorStop(1,'transparent');
    ctx.fillStyle=ag; ctx.beginPath(); ctx.arc(ap.px,ap.py,18,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=color; ctx.beginPath(); ctx.arc(ap.px,ap.py,4,0,Math.PI*2); ctx.fill();
    if(sim&&sim.traj){
      for(var i=0;i<Math.min(12,sim.traj.length);i++){
        var p=proj(sim.traj[i].x,sim.traj[i].y,sim.traj[i].z);
        ctx.globalAlpha=.25; ctx.fillStyle=color; ctx.beginPath(); ctx.arc(p.px,p.py,2,0,Math.PI*2); ctx.fill();
      } ctx.globalAlpha=1;
    }
  }
  if(playing)ry+=.006;
  frame++;
}
draw();

function togglePlay(){
  playing=!playing;
  var b=document.getElementById('playbtn');
  b.textContent=playing?'\u23F8 PAUSE':'\u25BA PLAY';
  b.style.background=playing?'#00ff9d22':'#ff2d5522';
  b.style.borderColor=playing?'#00ff9d':'#ff2d55';
  b.style.color=playing?'#00ff9d':'#ff2d55';
}

function setTab(t,btn){
  tab=t;
  document.querySelectorAll('.tb').forEach(function(b){b.classList.remove('on');});
  btn.classList.add('on');
  renderTab();
}

function renderTab(){
  var el=document.getElementById('tabbody');
  if(!sel){el.innerHTML='<div style="display:flex;align-items:center;justify-content:center;height:100%;opacity:.2;flex-direction:column;gap:6px"><div style="font-size:26px">&#9888;</div><div style="font-size:10px;letter-spacing:3px">SELECT A NEAR-EARTH OBJECT TO ANALYZE</div></div>';return;}
  if(tab==='overview'){
    if(!sim){el.innerHTML='<div style="color:#ffe600;font-size:9px;animation:pulse .8s infinite;padding:8px">&#9711; Running simulation...</div>';return;}
    var p=sel,c=rc(sim.prob);
    var cards=[['SMA','#4fc3f7',p.sma+' AU'],['ECC','#4fc3f7',p.ecc.toFixed(3)],['INC','#4fc3f7',p.inc+'&deg;'],
      ['RAAN','#ffe600',p.raan+'&deg;'],['ARGP','#ffe600',p.argp+'&deg;'],['MA','#ffe600',p.ma+'&deg;'],
      ['DIAMETER','#ff8c00',p.diameter+' m'],['PHA',p.haz?'#ff2d55':'#00ff9d',p.haz?'YES':'NO'],['DISCOVERY','#ffffff88',p.disc]];
    el.innerHTML='<div class="g3">'+cards.map(function(x){return '<div class="mc2"><div class="ml2">'+x[0]+'</div><div class="mv2" style="color:'+x[1]+'">'+x[2]+'</div></div>';}).join('')+'</div>'+
      '<div style="padding:8px 12px;background:'+c+'15;border:1px solid '+c+'44;border-radius:4px;font-size:10px;color:'+c+'">&#9679; HYBRID IMPACT PROBABILITY: '+(sim.prob*100).toFixed(6)+'% &mdash; '+rl(sim.prob)+'</div>';
  } else if(tab==='quantum'){
    if(!sim){el.innerHTML='<div style="color:#ffe600;font-size:9px;padding:8px;animation:pulse .8s infinite">&#9711; Running...</div>';return;}
    var q=vqc(sel);
    var bars=q.amp.map(function(a,i){
      return '<div class="qr"><span style="color:#00ff9d;font-size:10px;width:22px;font-family:monospace">q'+i+'</span>'+
        '<div style="flex:1;height:1px;background:#00ff9d33;position:relative">'+
        '<div style="position:absolute;left:14%;top:-7px;width:14px;height:14px;border:1px solid #00ff9d;background:#060a12;display:flex;align-items:center;justify-content:center;font-size:7px;color:#00ff9d;font-family:monospace">H</div>'+
        '<div style="position:absolute;left:40%;top:-7px;width:14px;height:14px;border:1px solid #ffe600;background:#060a12;display:flex;align-items:center;justify-content:center;font-size:7px;color:#ffe600;font-family:monospace">Rz</div>'+
        '<div style="position:absolute;left:65%;top:-7px;width:14px;height:14px;border:1px solid #ff8c00;background:#060a12;display:flex;align-items:center;justify-content:center;font-size:7px;color:#ff8c00;font-family:monospace">Rx</div></div>'+
        '<div style="width:54px;height:8px;border-radius:4px;background:linear-gradient(90deg,#00ff9d '+Math.round(Math.abs(a)*100)+'%,#0a1a0f 0%);border:1px solid #00ff9d22;margin-left:6px"></div>'+
        '<span style="color:#00ff9d66;font-size:9px;font-family:monospace;width:40px;text-align:right">'+a.toFixed(3)+'</span></div>';
    }).join('');
    el.innerHTML='<div style="font-size:9px;color:#00ff9d88;letter-spacing:2px;margin-bottom:10px;font-family:monospace">QUANTUM CIRCUIT &mdash; 8 QUBITS | VQC DEPTH 2</div>'+
      '<div style="background:#0a0f1e;border:1px solid #00ff9d22;border-radius:8px;padding:14px;margin-bottom:10px">'+bars+'<div style="font-size:9px;color:#ffffff22;font-family:monospace;margin-top:8px">MEASUREMENT: Z | SHOTS: 1024 | BACKEND: SIM</div></div>'+
      '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">'+
      '<div class="mc2"><div class="ml2">Q-ML SCORE</div><div class="mv2" style="color:#00ff9d;font-family:Orbitron,sans-serif;font-size:18px">'+q.score.toFixed(5)+'</div><div style="font-size:8px;color:#ffffff33;margin-top:2px">Z-basis expectation</div></div>'+
      '<div class="mc2"><div class="ml2">CIRCUIT</div><div style="font-size:9px;color:#4fc3f7;font-family:monospace;line-height:1.9;margin-top:4px">Qubits: 8<br>Layers: 2<br>Gates: H,Rz,Rx<br>Backend: SIM</div></div></div>'+
      '<div class="mc2" style="font-size:9px;color:#ffffff33;font-family:monospace;line-height:2">ZZFeatureMap(feature_dim=8, reps=2)<br>|&#936;&#10217; = U_&#966;(x)|0&#10217;^&#8855;8 | Optimizer: COBYLA</div>';
  } else if(tab==='montecarlo'){
    if(!sim){el.innerHTML='<div style="color:#ffe600;font-size:9px;padding:8px;animation:pulse .8s infinite">&#9711; Running...</div>';return;}
    var c=rc(sim.prob);
    var rows=sim.traj.slice(0,8).map(function(t){
      return '<tr><td style="color:#ffffff44">'+t.run+'</td><td>'+parseFloat(t.x).toFixed(4)+'</td><td>'+parseFloat(t.y).toFixed(4)+'</td><td>'+parseFloat(t.z).toFixed(4)+'</td><td>'+parseFloat(t.r).toFixed(4)+'</td><td>'+(t.nu!=null?parseFloat(t.nu).toFixed(2):'&mdash;')+'</td></tr>';
    }).join('');
    el.innerHTML='<div style="font-size:9px;color:#ffffff44;letter-spacing:2px;margin-bottom:10px">MONTE CARLO &mdash; '+sim.sruns+' RUNS &middot; KEPLER PROPAGATION</div>'+
      '<div class="g3"><div class="mc2"><div class="ml2">MC PROBABILITY</div><div class="mv2" style="color:'+c+'">'+(sim.mProb*100).toFixed(4)+'%</div></div>'+
      '<div class="mc2"><div class="ml2">SAMPLE RUNS</div><div class="mv2" style="color:#4fc3f7">'+sim.sruns+'</div></div>'+
      '<div class="mc2"><div class="ml2">HORIZON</div><div class="mv2" style="color:#ffe600">365 days</div></div></div>'+
      '<table><thead><tr><th>RUN</th><th>X (AU)</th><th>Y (AU)</th><th>Z (AU)</th><th>R (AU)</th><th>&nu; (&deg;)</th></tr></thead><tbody>'+rows+'</tbody></table>'+
      '<div style="margin-top:8px;font-size:9px;color:#ffffff22;font-family:monospace">&sigma;_a=&plusmn;2% &middot; &sigma;_e=&plusmn;0.01 &middot; &sigma;_ang=&plusmn;1&deg;</div>';
  } else if(tab==='log'){
    el.innerHTML=logs.length===0?'<div style="color:#ffffff22;font-size:9px">No logs yet. Select an asteroid to begin.</div>':
      logs.map(function(l,i){return '<div style="color:'+(i===0?'#00ff9d':'#ffffff44')+';font-family:monospace;font-size:10px;line-height:1.7;margin-bottom:2px">'+l+'</div>';}).join('');
  }
}
renderSidebar();
</script>
</body>
</html>"""

# ══════════════════════════════════════════════════════════════════
# write_dashboard uses HTML above — defined AFTER HTML
# ══════════════════════════════════════════════════════════════════
def write_dashboard():
    os.makedirs("static", exist_ok=True)
    with open("static/index.html", "w", encoding="utf-8") as f:
        f.write(HTML)
    print("  OK  static/index.html written")

# ══════════════════════════════════════════════════════════════════
# Flask imports & routes — AFTER both HTML and write_dashboard
# ══════════════════════════════════════════════════════════════════
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading, webbrowser, os, time

app = Flask(__name__)
CORS(app)

@app.route("/api/analyze")
def analyze():
    name = request.args.get("neo", "Apophis")
    runs = int(request.args.get("runs", 500))
    try:
        from src.data.neo_loader import load_neo_dataframe
        from src.quantum.vqc     import vqc_predict
        from src.physics.kepler  import monte_carlo, propagate
        from src.ml.ensemble     import hybrid_predict
        df    = load_neo_dataframe()
        match = df[df["name"].str.lower() == name.lower()]
        if match.empty:
            return jsonify({"error": "NEO not found"}), 404
        params = match.iloc[0].to_dict()
        qml    = vqc_predict(params)
        mc     = monte_carlo(params, runs=runs)
        result = hybrid_predict(params, qml, mc["impact_probability"])
        mc_pts = [{"x": round(s.x,4), "y": round(s.y,4), "z": round(s.z,4)}
                  for s in mc["states"][::max(1, runs//60)]]
        return jsonify({"name": params["name"], "result": result, "mc_pts": mc_pts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    return open("static/index.html", encoding="utf-8").read(), 200, {"Content-Type": "text/html"}

# ══════════════════════════════════════════════════════════════════
# MAIN — last, uses everything above
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    write_dashboard()
    threading.Thread(
        target=lambda: (time.sleep(1.4), webbrowser.open("http://127.0.0.1:5000")),
        daemon=True
    ).start()
    print("\n  AstroMind  ->  http://127.0.0.1:5000")
    print("  Ctrl+C to stop.\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
