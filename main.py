from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

@app.get("/quote")
async def quote(symbol: str = Query(...), interval: str = "1h", range: str = "1mo"):
    url = YAHOO.format(symbol=symbol)
    params = {"interval": interval, "range": range, "includePrePost": "false"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params, headers=HEADERS)
        return r.json()

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return HTML

@app.get("/status")
def status():
    return {"status": "ok", "service": "Yahoo Finance Proxy + Dashboard"}

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>Trading Dashboard Pro</title>
<style>
:root{--bg:#0d1117;--bg2:#161b22;--bg3:#21262d;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--green:#3fb950;--red:#f85149;--blue:#58a6ff;--yellow:#d29922;--purple:#bc8cff;}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,sans-serif;min-height:100vh;}
header{background:var(--bg2);border-bottom:1px solid var(--border);padding:12px 16px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;}
.logo{font-size:18px;font-weight:700;color:var(--blue);}.logo span{color:var(--text);}
#clock{font-size:12px;color:var(--muted);}
.section{padding:10px 14px;}
label{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:5px;}
.sym-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:8px;}
@media(min-width:600px){.sym-grid{grid-template-columns:repeat(6,1fr);}}
.sym-btn{background:var(--bg3);border:1px solid var(--border);color:var(--text);font-size:12px;font-weight:600;padding:10px 4px;border-radius:8px;cursor:pointer;text-align:center;}
.sym-btn.active{background:var(--blue);border-color:var(--blue);color:#000;}
.custom-row{display:flex;gap:8px;margin-bottom:10px;}
input[type=text],input[type=number]{background:var(--bg3);border:1px solid var(--border);color:var(--text);font-size:14px;padding:10px 12px;border-radius:8px;outline:none;width:100%;}
input:focus{border-color:var(--blue);}
.btn{background:var(--blue);color:#000;font-size:13px;font-weight:700;padding:10px 16px;border-radius:8px;border:none;cursor:pointer;white-space:nowrap;}
.btn-green{background:var(--green);}
.tf-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;}
@media(min-width:600px){.tf-grid{grid-template-columns:repeat(9,1fr);}}
.tf-btn{background:var(--bg3);border:1px solid var(--border);color:var(--muted);font-size:13px;font-weight:600;padding:9px 4px;border-radius:8px;cursor:pointer;text-align:center;}
.tf-btn.active{background:var(--purple);border-color:var(--purple);color:#fff;}
#price-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px;margin:10px 14px;}
.price-row{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;}
#price-val{font-size:30px;font-weight:700;}
#price-chg{font-size:14px;font-weight:600;}
.metrics-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:10px;}
@media(min-width:600px){.metrics-grid{grid-template-columns:repeat(6,1fr);}}
.metric{background:var(--bg3);border-radius:8px;padding:8px;text-align:center;}
.metric-lbl{font-size:10px;color:var(--muted);margin-bottom:2px;}
.metric-val{font-size:13px;font-weight:700;}
#signal-badge{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;border-radius:20px;font-size:13px;font-weight:700;margin-top:8px;}
.sig-buy{background:rgba(63,185,80,.2);color:var(--green);border:1px solid var(--green);}
.sig-sell{background:rgba(248,81,73,.2);color:var(--red);border:1px solid var(--red);}
.sig-neutral{background:rgba(139,148,158,.15);color:var(--muted);border:1px solid var(--border);}
#chart-wrap{margin:0 14px 10px;background:var(--bg2);border:1px solid var(--border);border-radius:12px;overflow:hidden;position:relative;}
canvas{display:block;width:100%;}
#chart-loader{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--bg2);gap:8px;}
#loader-text{font-size:13px;color:var(--muted);}
#loader-bar{width:60%;height:3px;background:var(--bg3);border-radius:2px;overflow:hidden;}
#loader-fill{height:100%;background:var(--blue);border-radius:2px;transition:width .3s;}
.ind-panels{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 14px 10px;}
@media(min-width:600px){.ind-panels{grid-template-columns:repeat(4,1fr);}}
.ind-panel{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:12px;}
.ind-title{font-size:11px;color:var(--muted);font-weight:600;margin-bottom:6px;display:flex;justify-content:space-between;}
.ind-val{font-size:17px;font-weight:700;}
.ind-bar{height:5px;background:var(--bg3);border-radius:3px;margin-top:7px;overflow:hidden;}
.ind-fill{height:100%;border-radius:3px;transition:width .4s;}
.risk-card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px;margin:0 14px 10px;}
.risk-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.risk-out-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px;}
.risk-item{background:var(--bg3);border-radius:8px;padding:10px;text-align:center;}
.risk-lbl{font-size:10px;color:var(--muted);margin-bottom:2px;}
.risk-num{font-size:14px;font-weight:700;}
#analysis-box{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px;margin:0 14px 14px;font-size:13px;line-height:1.7;display:none;}
#analysis-box h3{font-size:14px;color:var(--blue);margin-bottom:10px;}
#status{text-align:center;font-size:11px;padding:3px;margin-bottom:6px;}
.ok{color:#3fb950;}.err{color:#f85149;}.loading{color:#8b949e;}
#sym-label{font-size:13px;color:var(--muted);font-weight:600;}
.section-title{font-size:13px;font-weight:700;margin-bottom:8px;}
</style>
</head>
<body>
<header>
  <div class="logo">📈 Trading<span>Pro</span></div>
  <div id="clock">--:--:--</div>
</header>
<div class="section">
  <label>Instruments</label>
  <div class="sym-grid" id="sym-grid">
    <button class="sym-btn active" data-sym="GC=F" data-name="GOLD">GOLD</button>
    <button class="sym-btn" data-sym="CL=F" data-name="OIL">OIL</button>
    <button class="sym-btn" data-sym="ES=F" data-name="US500">US500</button>
    <button class="sym-btn" data-sym="NQ=F" data-name="US100">US100</button>
    <button class="sym-btn" data-sym="EURUSD=X" data-name="EURUSD">EUR/USD</button>
    <button class="sym-btn" data-sym="GBPUSD=X" data-name="GBPUSD">GBP/USD</button>
    <button class="sym-btn" data-sym="USDJPY=X" data-name="USDJPY">USD/JPY</button>
    <button class="sym-btn" data-sym="BTC-USD" data-name="BITCOIN">BTC</button>
    <button class="sym-btn" data-sym="ETH-USD" data-name="ETH">ETH</button>
    <button class="sym-btn" data-sym="^GDAXI" data-name="GER40">GER40</button>
    <button class="sym-btn" data-sym="SI=F" data-name="SILVER">SILVER</button>
    <button class="sym-btn" data-sym="RACE" data-name="Ferrari">RACE</button>
  </div>
  <div class="custom-row">
    <input type="text" id="custom-sym" placeholder="Symbole libre (ex: TSLA, AAPL...)">
    <button class="btn" onclick="loadCustom()">Go</button>
  </div>
</div>
<div class="section" style="padding-top:0">
  <label>Timeframe</label>
  <div class="tf-grid" id="tf-grid">
    <button class="tf-btn" data-int="5m" data-range="1d">M5</button>
    <button class="tf-btn" data-int="15m" data-range="5d">M15</button>
    <button class="tf-btn" data-int="30m" data-range="5d">M30</button>
    <button class="tf-btn active" data-int="1h" data-range="1mo">H1</button>
    <button class="tf-btn" data-int="4h" data-range="3mo">H4</button>
    <button class="tf-btn" data-int="1d" data-range="6mo">D1</button>
    <button class="tf-btn" data-int="3d" data-range="1y">D3</button>
    <button class="tf-btn" data-int="1wk" data-range="2y">W1</button>
    <button class="tf-btn" data-int="1mo" data-range="5y">MN</button>
  </div>
</div>
<div id="price-card">
  <div class="price-row"><span id="sym-label">GOLD</span><span id="price-val">--</span><span id="price-chg">--</span></div>
  <div id="signal-badge" class="sig-neutral">⬤ NEUTRAL</div>
  <div class="metrics-grid">
    <div class="metric"><div class="metric-lbl">ATR(14)</div><div class="metric-val" id="m-atr">--</div></div>
    <div class="metric"><div class="metric-lbl">BB Width</div><div class="metric-val" id="m-bbw">--</div></div>
    <div class="metric"><div class="metric-lbl">Vol Rel.</div><div class="metric-val" id="m-vol">--</div></div>
    <div class="metric"><div class="metric-lbl">EMA Fast</div><div class="metric-val" id="m-emaf">--</div></div>
    <div class="metric"><div class="metric-lbl">EMA Slow</div><div class="metric-val" id="m-emas">--</div></div>
    <div class="metric"><div class="metric-lbl">MACD Hist</div><div class="metric-val" id="m-macdh">--</div></div>
  </div>
</div>
<div id="chart-wrap">
  <canvas id="chart-canvas" height="260"></canvas>
  <div id="chart-loader">
    <div id="loader-text">Connexion…</div>
    <div id="loader-bar"><div id="loader-fill" style="width:0%"></div></div>
  </div>
</div>
<div class="ind-panels">
  <div class="ind-panel"><div class="ind-title"><span>RSI(14)</span><span id="rsi-zone">--</span></div><div class="ind-val" id="rsi-val">--</div><div class="ind-bar"><div class="ind-fill" id="rsi-fill" style="width:50%;background:var(--blue)"></div></div></div>
  <div class="ind-panel"><div class="ind-title"><span>MACD</span><span id="macd-cross">--</span></div><div class="ind-val" id="macd-val">--</div><div class="ind-bar"><div class="ind-fill" id="macd-fill" style="width:50%;background:var(--green)"></div></div></div>
  <div class="ind-panel"><div class="ind-title"><span>EMA Cross</span></div><div class="ind-val" id="ema-cross-val" style="font-size:13px">--</div></div>
  <div class="ind-panel"><div class="ind-title"><span>Bollinger</span></div><div class="ind-val" id="bb-val" style="font-size:13px">--</div></div>
</div>
<div class="risk-card">
  <div class="section-title">⚖️ Calculateur de Risque</div>
  <div class="risk-grid">
    <div><label>Capital (€)</label><input type="number" id="r-capital" value="10000"></div>
    <div><label>Risque %</label><input type="number" id="r-risk" value="1" step="0.1"></div>
    <div><label>Entrée</label><input type="number" id="r-entry" step="any"></div>
    <div><label>Stop Loss</label><input type="number" id="r-sl" step="any"></div>
    <div><label>Take Profit</label><input type="number" id="r-tp" step="any"></div>
    <div style="display:flex;align-items:flex-end;"><button class="btn btn-green" style="width:100%" onclick="calcRisk()">Calculer</button></div>
  </div>
  <div class="risk-out-grid">
    <div class="risk-item"><div class="risk-lbl">Risque €</div><div class="risk-num" id="ro-risk">--</div></div>
    <div class="risk-item"><div class="risk-lbl">R:R Ratio</div><div class="risk-num" id="ro-rr">--</div></div>
    <div class="risk-item"><div class="risk-lbl">Position</div><div class="risk-num" id="ro-size">--</div></div>
  </div>
</div>
<div class="section" style="padding-top:0">
  <button class="btn" style="width:100%;padding:14px" onclick="generateAnalysis()">🧠 Générer l'Analyse Technique</button>
</div>
<div id="analysis-box"></div>

<!-- XTB SECTION -->
<div style="background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px;margin:0 14px 10px;">
  <div style="font-size:13px;font-weight:700;margin-bottom:10px;">🏦 Saisie XTB (Click &amp; Trade)</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
    <div><label>Instrument</label>
      <select id="x-inst" style="background:var(--bg3);border:1px solid var(--border);color:var(--text);font-size:14px;padding:10px 12px;border-radius:8px;width:100%;outline:none;">
        <option value="FOREX">Forex (EUR/USD, GBP...)</option>
        <option value="JPY">Forex JPY (USD/JPY...)</option>
        <option value="GOLD">Gold (XAU/USD)</option>
        <option value="SILVER">Silver (XAG/USD)</option>
        <option value="OIL">Pétrole (OIL)</option>
        <option value="INDEX">Indices (US500, NAS...)</option>
        <option value="BTC">Bitcoin</option>
        <option value="ETH">Ethereum</option>
      </select>
    </div>
    <div style="display:flex;align-items:flex-end;">
      <button class="btn" style="width:100%;background:var(--purple);" onclick="fillXTBFromDashboard()">⬆ Importer du graphique</button>
    </div>
  </div>

  <!-- Prix XTB réel -->
  <div style="background:rgba(88,166,255,.08);border:1px solid rgba(88,166,255,.3);border-radius:8px;padding:10px;margin-bottom:10px;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:flex-end;">
      <div>
        <label style="color:var(--blue);">💹 Prix réel XTB (optionnel)</label>
        <input type="number" id="x-xtb-real" step="any" placeholder="Ex: 4398.5 (prix XTB actuel)" oninput="calcXTB()" style="border-color:rgba(88,166,255,.4);">
      </div>
      <div style="font-size:11px;color:var(--muted);padding-bottom:4px;">
        Saisis le prix actuel affiché sur XTB pour corriger l'écart avec Yahoo Finance. Entry/SL/TP seront recalculés proportionnellement.
      </div>
    </div>
    <div id="x-ecart-info" style="font-size:11px;color:var(--muted);margin-top:6px;display:none;">
      Écart Yahoo↔XTB : <span id="x-ecart-val" style="font-weight:700;"></span>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:10px;">
    <div><label>Entrée (prix)</label><input type="number" id="x-entry" step="any" oninput="calcXTB()"></div>
    <div><label>Stop Loss (prix)</label><input type="number" id="x-sl" step="any" oninput="calcXTB()"></div>
    <div><label>Take Profit (prix)</label><input type="number" id="x-tp" step="any" oninput="calcXTB()"></div>
  </div>

  <!-- Résultats -->
  <div style="background:var(--bg3);border-radius:10px;padding:12px;">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap;">
      <span style="font-size:12px;color:var(--muted);">Direction :</span>
      <span id="x-dir" style="font-size:15px;font-weight:700;">--</span>
      <span style="font-size:12px;color:var(--muted);margin-left:10px;">R:R :</span>
      <span id="x-rr" style="font-size:15px;font-weight:700;">--</span>
    </div>
    <!-- Saisie XTB -->
    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:12px;">
      <div style="font-size:11px;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px;">📋 À saisir dans XTB (Click &amp; Trade)</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
        <div style="background:var(--bg3);border-radius:8px;padding:10px;">
          <div style="font-size:10px;color:var(--muted);margin-bottom:4px;">PRIX D'ENTRÉE</div>
          <div id="x-xtb-entry" style="font-size:14px;font-weight:700;color:var(--yellow);">--</div>
        </div>
        <div style="background:var(--bg3);border-radius:8px;padding:10px;">
          <div style="font-size:10px;color:var(--muted);margin-bottom:4px;">S/L (pips)</div>
          <div id="x-xtb-sl" style="font-size:14px;font-weight:700;color:var(--red);">--</div>
        </div>
        <div style="background:var(--bg3);border-radius:8px;padding:10px;">
          <div style="font-size:10px;color:var(--muted);margin-bottom:4px;">T/P (pips)</div>
          <div id="x-xtb-tp" style="font-size:14px;font-weight:700;color:var(--green);">--</div>
        </div>
      </div>
      <div style="font-size:11px;color:var(--muted);margin-top:8px;text-align:center;">
        SL négatif si LONG · SL positif si SHORT · TP toujours positif dans XTB
      </div>
    </div>

    <!-- Prix absolus corrigés XTB -->
    <div style="background:var(--bg2);border:1px solid rgba(63,185,80,.3);border-radius:8px;padding:12px;margin-top:8px;">
      <div style="font-size:11px;color:var(--green);margin-bottom:8px;text-transform:uppercase;letter-spacing:.5px;font-weight:600;">📌 Prix absolus à saisir dans XTB</div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
        <div style="background:var(--bg3);border-radius:8px;padding:10px;">
          <div style="font-size:10px;color:var(--muted);margin-bottom:4px;">ENTRÉE</div>
          <div id="x-abs-entry" style="font-size:15px;font-weight:700;color:var(--yellow);">--</div>
        </div>
        <div style="background:var(--bg3);border-radius:8px;padding:10px;">
          <div style="font-size:10px;color:var(--muted);margin-bottom:4px;">STOP LOSS</div>
          <div id="x-abs-sl" style="font-size:15px;font-weight:700;color:var(--red);">--</div>
        </div>
        <div style="background:var(--bg3);border-radius:8px;padding:10px;">
          <div style="font-size:10px;color:var(--muted);margin-bottom:4px;">TAKE PROFIT</div>
          <div id="x-abs-tp" style="font-size:15px;font-weight:700;color:var(--green);">--</div>
        </div>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;">
      <div style="text-align:center;background:var(--bg2);border-radius:8px;padding:8px;">
        <div style="font-size:10px;color:var(--muted);">SL distance</div>
        <div id="x-sl-pips" style="font-size:14px;font-weight:700;color:var(--red);">--</div>
      </div>
      <div style="text-align:center;background:var(--bg2);border-radius:8px;padding:8px;">
        <div style="font-size:10px;color:var(--muted);">TP distance</div>
        <div id="x-tp-pips" style="font-size:14px;font-weight:700;color:var(--green);">--</div>
      </div>
    </div>
  </div>
</div>

<div id="status" class="loading">Initialisation…</div>
<script>
var S={sym:'GC=F',name:'GOLD',interval:'1h',range:'1mo',tf:'H1',candles:[],indicators:{},price:null,chg:null,chgPct:null};
setInterval(function(){document.getElementById('clock').textContent=new Date().toLocaleTimeString('fr-FR');},1000);
document.getElementById('sym-grid').addEventListener('click',function(e){
  var b=e.target.closest('.sym-btn');if(!b)return;
  document.querySelectorAll('.sym-btn').forEach(function(x){x.classList.remove('active');});b.classList.add('active');
  S.sym=b.dataset.sym;S.name=b.dataset.name;document.getElementById('custom-sym').value='';loadData();
});
document.getElementById('tf-grid').addEventListener('click',function(e){
  var b=e.target.closest('.tf-btn');if(!b)return;
  document.querySelectorAll('.tf-btn').forEach(function(x){x.classList.remove('active');});b.classList.add('active');
  S.interval=b.dataset.int;S.range=b.dataset.range;S.tf=b.textContent.trim();loadData();
});
function loadCustom(){var v=document.getElementById('custom-sym').value.trim().toUpperCase();if(!v)return;document.querySelectorAll('.sym-btn').forEach(function(x){x.classList.remove('active');});S.sym=v;S.name=v;loadData();}
document.getElementById('custom-sym').addEventListener('keydown',function(e){if(e.key==='Enter')loadCustom();});
function setProgress(p,t){document.getElementById('loader-fill').style.width=p+'%';document.getElementById('loader-text').textContent=t;}
function showLoader(v){document.getElementById('chart-loader').style.display=v?'flex':'none';}
function loadData(){
  showLoader(true);setProgress(10,'Connexion…');setStatus('Chargement…','loading');
  var url='/quote?symbol='+encodeURIComponent(S.sym)+'&interval='+S.interval+'&range='+S.range;
  fetch(url).then(function(r){return r.json();}).then(function(j){
    var res=j&&j.chart&&j.chart.result&&j.chart.result[0];
    if(!res)throw new Error('Pas de données');
    setProgress(80,'Calcul…');
    var meta=res.meta,q=res.indicators.quote[0],ts=res.timestamp;
    S.candles=ts.map(function(t,i){return{t:t*1000,o:q.open[i],h:q.high[i],l:q.low[i],c:q.close[i],v:q.volume?q.volume[i]:0};}).filter(function(c){return c.o&&c.h&&c.l&&c.c;});
    S.price=meta.regularMarketPrice||S.candles[S.candles.length-1].c;
    var prev=meta.chartPreviousClose||meta.previousClose||S.candles[0].c;
    S.chg=S.price-prev;S.chgPct=(S.chg/prev)*100;
    compute();updatePriceCard();drawChart();updatePanels();autoFillRisk();
    setStatus('✓ '+S.candles.length+' bougies · '+new Date().toLocaleTimeString('fr-FR'),'ok');
    showLoader(false);
  }).catch(function(e){setStatus('Erreur: '+e.message,'err');showLoader(false);});
}
function ema(arr,p){var k=2/(p+1),e=arr[0],out=[];arr.forEach(function(v){e=v*k+e*(1-k);out.push(e);});return out;}
function compute(){
  var c=S.candles.map(function(x){return x.c;}),h=S.candles.map(function(x){return x.h;}),
      l=S.candles.map(function(x){return x.l;}),v=S.candles.map(function(x){return x.v||0;}),n=c.length;
  var isPos=['W1','MN'].indexOf(S.tf)>=0,isSwing=['D1','D3'].indexOf(S.tf)>=0;
  var fp=isPos?50:isSwing?20:9,sp=isPos?200:isSwing?50:21;
  var emaf=ema(c,fp),emas=ema(c,sp),gains=[],losses=[];
  for(var i=1;i<n;i++){var d=c[i]-c[i-1];gains.push(Math.max(d,0));losses.push(Math.max(-d,0));}
  var ag=gains.slice(-14).reduce(function(a,b){return a+b;},0)/14,al=losses.slice(-14).reduce(function(a,b){return a+b;},0)/14;
  var rsi=al===0?100:100-100/(1+ag/al);
  var e12=ema(c,12),e26=ema(c,26),ml=e12.map(function(v,i){return v-e26[i];});
  var sig9=ema(ml.slice(-30),9),macdHist=ml[n-1]-sig9[sig9.length-1];
  var p20=c.slice(-20),mean=p20.reduce(function(a,b){return a+b;},0)/20;
  var std=Math.sqrt(p20.reduce(function(a,b){return a+(b-mean)*(b-mean);},0)/20);
  var bbUp=mean+2*std,bbLo=mean-2*std,bbW=(bbUp-bbLo)/mean*100,atrs=[];
  for(var j=1;j<n;j++)atrs.push(Math.max(h[j]-l[j],Math.abs(h[j]-c[j-1]),Math.abs(l[j]-c[j-1])));
  var atr=atrs.slice(-14).reduce(function(a,b){return a+b;},0)/14;
  var vAvg=v.slice(-20).reduce(function(a,b){return a+b;},0)/20,vRel=v[n-1]/(vAvg||1);
  var bbUpArr=c.map(function(_,i){
    if(i<19)return null;var sl=c.slice(i-19,i+1),m=sl.reduce(function(a,b){return a+b;},0)/20;
    var s=Math.sqrt(sl.reduce(function(a,b){return a+(b-m)*(b-m);},0)/20);return{up:m+2*s,lo:m-2*s};
  });
  S.indicators={emaf:emaf,emas:emas,fp:fp,sp:sp,emafLast:emaf[n-1],emasLast:emas[n-1],rsi:rsi,macdHist:macdHist,bbUp:bbUp,bbLo:bbLo,bbMid:mean,bbW:bbW,atr:atr,vRel:vRel,c:c,h:h,l:l,emafArr:emaf,emasArr:emas,bbUpArr:bbUpArr};
  var cross=emaf[n-1]>emas[n-1];
  S.signal=(cross&&rsi<70&&macdHist>0)?'BUY':(!cross&&rsi>30&&macdHist<0)?'SELL':'NEUTRAL';
}
function fmt(v,d){d=d||2;if(v==null||isNaN(v))return'--';return v>=1000?v.toLocaleString('fr-FR',{maximumFractionDigits:d}):v.toFixed(d);}
function updatePriceCard(){
  var ind=S.indicators,dp=S.price>100?2:4;
  document.getElementById('sym-label').textContent=S.name;
  var pEl=document.getElementById('price-val');pEl.textContent=fmt(S.price,dp);pEl.style.color=S.chg>=0?'var(--green)':'var(--red)';
  var sign=S.chg>=0?'+':'';
  document.getElementById('price-chg').textContent=sign+fmt(S.chg,dp)+' ('+sign+(S.chgPct||0).toFixed(2)+'%)';
  document.getElementById('price-chg').style.color=S.chg>=0?'var(--green)':'var(--red)';
  document.getElementById('m-atr').textContent=fmt(ind.atr,dp);document.getElementById('m-bbw').textContent=(ind.bbW||0).toFixed(1)+'%';
  document.getElementById('m-vol').textContent=(ind.vRel||0).toFixed(1)+'x';document.getElementById('m-emaf').textContent=fmt(ind.emafLast,dp);
  document.getElementById('m-emas').textContent=fmt(ind.emasLast,dp);document.getElementById('m-macdh').textContent=(ind.macdHist||0).toFixed(4);
  var badge=document.getElementById('signal-badge'),icons={BUY:'▲ BUY',SELL:'▼ SELL',NEUTRAL:'⬤ NEUTRAL'};
  badge.textContent=icons[S.signal];badge.className='sig-'+S.signal.toLowerCase();
}
function drawChart(){
  var canvas=document.getElementById('chart-canvas'),dpr=window.devicePixelRatio||1,W=canvas.offsetWidth||600,H=260;
  canvas.width=W*dpr;canvas.height=H*dpr;var ctx=canvas.getContext('2d');ctx.scale(dpr,dpr);
  var ind=S.indicators,n=S.candles.length,visN=Math.min(n,80),vis=S.candles.slice(n-visN);
  var pad={l:6,r:58,t:14,b:28},cW=W-pad.l-pad.r,cH=H-pad.t-pad.b;
  var emafV=ind.emafArr.slice(n-visN),emasV=ind.emasArr.slice(n-visN),bbV=ind.bbUpArr.slice(n-visN);
  var allVals=vis.map(function(c){return c.h;}).concat(vis.map(function(c){return c.l;})).concat(emafV.filter(Boolean)).concat(emasV.filter(Boolean)).concat(bbV.filter(Boolean).reduce(function(a,b){return a.concat([b.up,b.lo]);},[]) );
  var minV=Math.min.apply(null,allVals)*0.9996,maxV=Math.max.apply(null,allVals)*1.0004,rng=maxV-minV||1;
  var yp=function(v){return pad.t+cH*(1-(v-minV)/rng);},bW=Math.max(1,cW/visN-1),xp=function(i){return pad.l+(i+0.5)*(cW/visN);};
  ctx.fillStyle='#161b22';ctx.fillRect(0,0,W,H);
  ctx.strokeStyle='#21262d';ctx.lineWidth=1;
  for(var g=0;g<=4;g++){var gy=pad.t+cH*g/4;ctx.beginPath();ctx.moveTo(pad.l,gy);ctx.lineTo(W-pad.r,gy);ctx.stroke();ctx.fillStyle='#8b949e';ctx.font='9px -apple-system';ctx.textAlign='right';ctx.fillText(fmt(maxV-rng*g/4,maxV>100?2:4),W-2,gy+3);}
  var started=false;ctx.beginPath();
  bbV.forEach(function(b,i){if(!b)return;var x=xp(i);if(!started){ctx.moveTo(x,yp(b.up));started=true;}else ctx.lineTo(x,yp(b.up));});
  ctx.strokeStyle='rgba(188,140,255,.35)';ctx.lineWidth=1;ctx.stroke();
  ctx.beginPath();started=false;
  bbV.forEach(function(b,i){if(!b)return;var x=xp(i);if(!started){ctx.moveTo(x,yp(b.lo));started=true;}else ctx.lineTo(x,yp(b.lo));});ctx.stroke();
  [[emafV,'#58a6ff'],[emasV,'#f85149']].forEach(function(pair){
    var arr=pair[0],col=pair[1];ctx.beginPath();started=false;
    arr.forEach(function(v,i){if(!v)return;var x=xp(i),y=yp(v);if(!started){ctx.moveTo(x,y);started=true;}else ctx.lineTo(x,y);});
    ctx.strokeStyle=col;ctx.lineWidth=1.5;ctx.stroke();
  });
  vis.forEach(function(c,i){
    var x=xp(i),bull=c.c>=c.o;ctx.strokeStyle=bull?'#3fb950':'#f85149';ctx.fillStyle=bull?'#3fb950':'#f85149';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(x,yp(c.h));ctx.lineTo(x,yp(c.l));ctx.stroke();
    var y1=yp(Math.max(c.o,c.c)),bh=Math.max(1,yp(Math.min(c.o,c.c))-y1);ctx.fillRect(x-bW/2,y1,bW,bh);
  });
  var entry=parseFloat(document.getElementById('r-entry').value),sl=parseFloat(document.getElementById('r-sl').value),tp=parseFloat(document.getElementById('r-tp').value);
  function drawLine(v,col,lbl){if(!v||isNaN(v)||v<minV||v>maxV)return;var y=yp(v);ctx.setLineDash([4,3]);ctx.strokeStyle=col;ctx.lineWidth=1.2;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle=col;ctx.font='9px -apple-system';ctx.textAlign='left';ctx.fillText(lbl,pad.l+2,y-2);}
  if(entry){drawLine(entry,'#d29922','Entry');drawLine(sl,'#f85149','SL');drawLine(tp,'#3fb950','TP');}
  ctx.fillStyle='#8b949e';ctx.font='9px -apple-system';ctx.textAlign='center';
  var step=Math.max(1,Math.floor(visN/5));
  for(var k=0;k<visN;k+=step){var d=new Date(vis[k].t);var lbl=(S.interval.indexOf('m')>=0||S.interval==='1h'||S.interval==='4h')?d.toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}):d.toLocaleDateString('fr-FR',{day:'2-digit',month:'2-digit'});ctx.fillText(lbl,xp(k),H-6);}
}
function updatePanels(){
  var ind=S.indicators,rsi=ind.rsi;
  document.getElementById('rsi-val').textContent=(rsi||0).toFixed(1);document.getElementById('rsi-val').style.color=rsi>70?'var(--red)':rsi<30?'var(--green)':'var(--blue)';
  document.getElementById('rsi-fill').style.width=(rsi||50)+'%';document.getElementById('rsi-fill').style.background=rsi>70?'var(--red)':rsi<30?'var(--green)':'var(--blue)';
  document.getElementById('rsi-zone').textContent=rsi>70?'Suracheté':rsi<30?'Survendu':'Neutre';
  var h=ind.macdHist;document.getElementById('macd-val').textContent=(h||0).toFixed(5);document.getElementById('macd-val').style.color=h>=0?'var(--green)':'var(--red)';
  var pct=Math.min(100,Math.abs(h||0)/(ind.atr||1)*300);document.getElementById('macd-fill').style.width=pct+'%';document.getElementById('macd-fill').style.background=h>=0?'var(--green)':'var(--red)';
  document.getElementById('macd-cross').textContent=h>=0?'Haussier':'Baissier';
  var cross=ind.emafLast>ind.emasLast,emaEl=document.getElementById('ema-cross-val');
  emaEl.textContent=cross?'▲ EMA'+ind.fp+' > EMA'+ind.sp:'▼ EMA'+ind.fp+' < EMA'+ind.sp;emaEl.style.color=cross?'var(--green)':'var(--red)';
  var p=S.price,bbEl=document.getElementById('bb-val');
  if(p>ind.bbUp*0.998){bbEl.textContent='⬆ Bande sup.';bbEl.style.color='var(--red)';}
  else if(p<ind.bbLo*1.002){bbEl.textContent='⬇ Bande inf.';bbEl.style.color='var(--green)';}
  else{bbEl.textContent='↔ Zone médiane';bbEl.style.color='var(--blue)';}
}
function autoFillRisk(){
  var ind=S.indicators,p=S.price;if(!p)return;var dp=p>100?2:5;
  document.getElementById('r-entry').value=p.toFixed(dp);
  var atr=ind.atr||p*0.01,mult=(['MN','W1'].indexOf(S.tf)>=0)?3:(['D1','D3'].indexOf(S.tf)>=0)?2:S.tf==='H4'?1.5:1;
  var slD=atr*mult,tpD=slD*2,buy=S.signal!=='SELL';
  document.getElementById('r-sl').value=(buy?p-slD:p+slD).toFixed(dp);document.getElementById('r-tp').value=(buy?p+tpD:p-tpD).toFixed(dp);
}
function calcRisk(){
  var cap=parseFloat(document.getElementById('r-capital').value),riskPct=parseFloat(document.getElementById('r-risk').value);
  var entry=parseFloat(document.getElementById('r-entry').value),sl=parseFloat(document.getElementById('r-sl').value),tp=parseFloat(document.getElementById('r-tp').value);
  if(!cap||!riskPct||!entry||!sl)return;
  var riskE=cap*riskPct/100,slD=Math.abs(entry-sl),tpD=tp?Math.abs(tp-entry):null;
  document.getElementById('ro-risk').textContent=riskE.toFixed(2)+'€';document.getElementById('ro-rr').textContent=tpD?(tpD/slD).toFixed(2):'--';document.getElementById('ro-size').textContent=(riskE/slD).toFixed(3);drawChart();
}
function generateAnalysis(){
  var ind=S.indicators,p=S.price;if(!p){alert('Charge un instrument.');return;}
  var rsi=(ind.rsi||0).toFixed(1),h=ind.macdHist,cross=ind.emafLast>ind.emasLast;
  var bias=S.signal==='BUY'?'🟢 Haussier':S.signal==='SELL'?'🔴 Baissier':'🟡 Neutre';
  var entry=document.getElementById('r-entry').value,sl=document.getElementById('r-sl').value,tp=document.getElementById('r-tp').value;
  var tradeTxt=entry&&sl&&tp?'<br><br><b>📋 Setup</b><br>Entrée: '+entry+' · SL: '+sl+' · TP: '+tp+'<br>R:R = '+(Math.abs(tp-entry)/Math.abs(sl-entry)).toFixed(2):'';
  var box=document.getElementById('analysis-box');
  box.innerHTML='<h3>📊 '+S.name+' · '+S.tf+'</h3><b>Bias:</b> '+bias+'<br><br><b>EMA:</b> EMA'+ind.fp+(cross?' > ':' < ')+'EMA'+ind.sp+' → '+(cross?'haussier':'baissier')+'.<br><br><b>RSI:</b> '+rsi+' — '+(rsi>70?'suracheté':rsi<30?'survendu':'neutre')+'.<br><br><b>MACD:</b> '+(h>=0?'positif → momentum acheteur':'négatif → pression vendeuse')+'.<br><br><b>ATR:</b> '+fmt(ind.atr,S.price>100?2:4)+' — calibre ton SL sur cette valeur.'+tradeTxt+'<br><br><span style="color:var(--muted);font-size:11px">⚠️ Indicatif. Confirme avec price action.</span>';
  box.style.display='block';box.scrollIntoView({behavior:'smooth'});
}
function setStatus(txt,cls){var el=document.getElementById('status');el.textContent=txt;el.className=cls;}
window.addEventListener('resize',function(){if(S.candles.length)drawChart();});

// ── XTB CALCULATOR ─────────────────────────────────────────────────────────
function calcXTB(){
  var entry=parseFloat(document.getElementById('x-entry').value);
  var sl=parseFloat(document.getElementById('x-sl').value);
  var tp=parseFloat(document.getElementById('x-tp').value);
  var inst=document.getElementById('x-inst').value;
  if(!entry||!sl||!tp){return;}

  // Pip size per instrument
  var pipSizes={'FOREX':0.0001,'JPY':0.01,'GOLD':0.1,'SILVER':0.01,'OIL':0.01,'INDEX':1,'BTC':1,'ETH':0.1};
  var pip=pipSizes[inst]||0.0001;

  // Correction écart Yahoo ↔ XTB
  var xtbReal=parseFloat(document.getElementById('x-xtb-real').value);
  if(xtbReal&&entry){
    var ecart=xtbReal-entry;
    var ecartEl=document.getElementById('x-ecart-info');
    var ecartSign=ecart>=0?'+':'';
    document.getElementById('x-ecart-val').textContent=ecartSign+ecart.toFixed(2)+' (Yahoo: '+entry+' → XTB: '+xtbReal+')';
    document.getElementById('x-ecart-val').style.color=Math.abs(ecart)>2?'var(--yellow)':'var(--green)';
    ecartEl.style.display='block';
    // Recalcul proportionnel : décale entry, SL, TP du même écart
    entry=xtbReal;
    sl=parseFloat(document.getElementById('x-sl').value)+ecart;
    tp=parseFloat(document.getElementById('x-tp').value)+ecart;
  } else {
    document.getElementById('x-ecart-info').style.display='none';
  }

  var dir=sl<entry?'LONG':'SHORT';

  // Distance en pips (toujours positive)
  var slPips=Math.round(Math.abs(entry-sl)/pip);
  var tpPips=Math.round(Math.abs(tp-entry)/pip);
  var rr=tpPips/(slPips||1);

  // XTB Click & Trade : SL = négatif si LONG, positif si SHORT / TP = toujours positif
  var xtbSL=(dir==='LONG'?'-':'+')+slPips;
  var xtbTP='+'+tpPips;

  document.getElementById('x-dir').textContent=dir;
  document.getElementById('x-dir').style.color=dir==='LONG'?'var(--green)':'var(--red)';
  document.getElementById('x-sl-pips').textContent=slPips+' pips';
  document.getElementById('x-tp-pips').textContent=tpPips+' pips';
  document.getElementById('x-rr').textContent='1 : '+rr.toFixed(2);
  document.getElementById('x-rr').style.color=rr>=2?'var(--green)':rr>=1?'var(--yellow)':'var(--red)';

  // Saisie XTB (Click & Trade)
  document.getElementById('x-xtb-entry').textContent='Prix: '+entry;
  document.getElementById('x-xtb-sl').textContent='S/L: '+xtbSL;
  document.getElementById('x-xtb-tp').textContent='T/P: '+xtbTP;

  // Prix absolus corrigés
  var dp=entry>100?2:5;
  document.getElementById('x-abs-entry').textContent=entry.toFixed(dp);
  document.getElementById('x-abs-sl').textContent=sl.toFixed(dp);
  document.getElementById('x-abs-tp').textContent=tp.toFixed(dp);
}

function fillXTBFromDashboard(){
  var entry=document.getElementById('r-entry').value;
  var sl=document.getElementById('r-sl').value;
  var tp=document.getElementById('r-tp').value;
  if(entry)document.getElementById('x-entry').value=entry;
  if(sl)document.getElementById('x-sl').value=sl;
  if(tp)document.getElementById('x-tp').value=tp;
  // auto-detect instrument
  var inst='FOREX';
  var sym=S.sym;
  if(sym.indexOf('GC')>=0||sym.indexOf('GOLD')>=0||sym==='GC=F')inst='GOLD';
  else if(sym.indexOf('SI')>=0||sym.indexOf('SILVER')>=0)inst='SILVER';
  else if(sym.indexOf('CL')>=0||sym.indexOf('OIL')>=0)inst='OIL';
  else if(sym.indexOf('BTC')>=0)inst='BTC';
  else if(sym.indexOf('ETH')>=0)inst='ETH';
  else if(sym.indexOf('JPY')>=0)inst='JPY';
  else if(sym==='ES=F'||sym==='NQ=F'||sym.indexOf('GDAXI')>=0)inst='INDEX';
  document.getElementById('x-inst').value=inst;
  calcXTB();
}

loadData();
</script>
</body>
</html>"""
