#!/usr/bin/env python3
import os

STATIC = '/opt/automacoes/cliquedf/noc/static'

# ── OLTS.HTML ──────────────────────────────────────────────
olts = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HubNOC — Monitor OLTs</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
:root{--bg:#0a0f1a;--surf:#0f1623;--surf2:#151e2e;--surf3:#1a2438;--border:#1e2d45;--border2:#243450;--text:#e2eaf4;--text2:#8ba3be;--text3:#4a6580;--blue:#00aaff;--green:#00e5a0;--red:#ff4466;--amber:#ffb830;--purple:#a78bfa;--radius:10px;--radius2:7px;--font:'Inter',system-ui,sans-serif;--sw:220px;--th:52px;}
body.light{--bg:#f0f4fa;--surf:#fff;--surf2:#e8edf5;--surf3:#dde3ef;--border:#cdd5e0;--border2:#bdc7d8;--text:#0f1623;--text2:#3a5070;--text3:#607a96;}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--font);font-size:13px;overflow:hidden;}
#shell{display:flex;height:100vh;}
#sb{width:var(--sw);background:var(--surf);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0;overflow:hidden;z-index:50;transition:width .25s cubic-bezier(.4,0,.2,1);}
#sb.col{width:52px;}
.sb-hd{padding:0 12px;height:var(--th);display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border);flex-shrink:0;}
.sb-logo{display:flex;align-items:center;gap:9px;flex:1;min-width:0;}
.sb-li{width:30px;height:30px;border-radius:8px;flex-shrink:0;background:linear-gradient(135deg,var(--blue),#0055aa);display:flex;align-items:center;justify-content:center;box-shadow:0 0 12px rgba(0,170,255,.3);}
.sb-li svg{width:15px;height:15px;color:#fff;}
.sb-lt{font-size:15px;font-weight:900;letter-spacing:-.3px;white-space:nowrap;overflow:hidden;}
.sb-lt span{color:var(--blue);}
.sb-tog{background:none;border:none;color:var(--text3);cursor:pointer;padding:5px;border-radius:5px;display:flex;flex-shrink:0;}
.sb-tog:hover{background:var(--surf2);color:var(--text);}
.sb-nav{flex:1;overflow-y:auto;padding:8px 6px;}
.sb-nav::-webkit-scrollbar{display:none;}
.sb-g{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);padding:10px 8px 4px;white-space:nowrap;overflow:hidden;}
#sb.col .sb-g{display:none;}
.ni{display:flex;align-items:center;gap:9px;padding:8px 9px;border-radius:var(--radius2);cursor:pointer;color:var(--text2);transition:all .15s;position:relative;white-space:nowrap;overflow:hidden;text-decoration:none;}
.ni:hover{background:var(--surf2);color:var(--text);}
.ni.on{background:rgba(0,170,255,.1);color:var(--blue);}
.ni.on::before{content:'';position:absolute;left:0;top:4px;bottom:4px;width:2px;background:var(--blue);border-radius:0 2px 2px 0;}
.ni svg{width:16px;height:16px;flex-shrink:0;}
.ni-l{font-size:13px;font-weight:500;}
#sb.col .ni-l{display:none;}
#sb.col .ni{justify-content:center;padding:9px;}
.sb-ft{padding:10px 6px;border-top:1px solid var(--border);}
.sb-u{display:flex;align-items:center;gap:9px;padding:8px;border-radius:var(--radius2);}
.sb-av{width:28px;height:28px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,var(--blue),var(--blue)88);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;}
.sb-ui{min-width:0;flex:1;}
.sb-un{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.sb-ug{font-size:10px;color:var(--text3);display:flex;align-items:center;gap:4px;margin-top:1px;}
.sb-ug::before{content:'';width:5px;height:5px;border-radius:50%;background:var(--green);flex-shrink:0;}
#sb.col .sb-ui{display:none;}
.btn-sair{width:100%;display:flex;align-items:center;gap:8px;padding:8px;border-radius:6px;background:rgba(255,68,102,.06);border:1px solid rgba(255,68,102,.15);color:var(--red);cursor:pointer;font-size:12px;font-weight:600;margin-bottom:6px;transition:.15s;}
.btn-sair:hover{background:rgba(255,68,102,.12);}
#sb.col .btn-sair span{display:none;}
#sb.col .btn-sair{justify-content:center;padding:9px;}
#main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0;}
#tb{height:var(--th);background:var(--surf);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;gap:12px;flex-shrink:0;position:relative;}
#tb::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--blue)40,transparent);}
.tb-title{font-size:14px;font-weight:700;flex:1;}
.tb-right{display:flex;align-items:center;gap:10px;margin-left:auto;}
.clock{font-family:monospace;font-size:13px;color:var(--blue);font-weight:700;}
.btn-tv{display:flex;align-items:center;gap:6px;background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.25);color:#a78bfa;padding:6px 14px;border-radius:var(--radius2);font-size:12px;font-weight:600;text-decoration:none;}
.btn-th{width:32px;height:32px;border-radius:50%;border:1px solid var(--border);background:var(--surf2);cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center;}
#content{flex:1;overflow-y:auto;display:flex;gap:0;}
.olt-lista{width:380px;flex-shrink:0;border-right:1px solid var(--border);overflow-y:auto;}
.olt-lista::-webkit-scrollbar{width:3px;}
.olt-lista::-webkit-scrollbar-thumb{background:var(--border2);}
.ol-hd{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;background:var(--surf);z-index:5;}
.ol-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--blue);}
.ol-cnt{font-size:11px;color:var(--text3);}
.olt-item{padding:14px 16px;border-bottom:1px solid var(--border);cursor:pointer;transition:.15s;position:relative;}
.olt-item:hover{background:var(--surf2);}
.olt-item.sel{background:rgba(0,170,255,.07);}
.olt-item.sel::before{content:'';position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--blue);}
.olt-item.down{border-left:3px solid var(--red);}
.olt-item.aviso{border-left:3px solid var(--amber);}
.oi-top{display:flex;align-items:center;gap:8px;margin-bottom:5px;}
.oi-nome{font-size:13px;font-weight:700;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.oi-online{font-size:14px;font-weight:800;color:var(--green);font-family:monospace;}
.oi-total{font-size:11px;color:var(--text3);font-family:monospace;}
.oi-bar{height:4px;background:var(--surf3);border-radius:2px;overflow:hidden;margin-bottom:5px;}
.oi-bar-fill{height:100%;border-radius:2px;background:var(--green);transition:width .4s ease;}
.oi-bar-fill.low{background:var(--red);}
.oi-bar-fill.mid{background:var(--amber);}
.oi-meta{font-size:11px;color:var(--text3);}
.dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.d-ok{background:var(--green);box-shadow:0 0 4px var(--green);}
.d-down{background:var(--red);box-shadow:0 0 6px var(--red);animation:blink 1.5s infinite;}
.d-av{background:var(--amber);}
.d-pause{background:var(--text3);}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.olt-detalhe{flex:1;overflow-y:auto;padding:20px 24px;}
.olt-detalhe::-webkit-scrollbar{width:4px;}
.olt-detalhe::-webkit-scrollbar-thumb{background:var(--border2);}
.det-empty{display:flex;align-items:center;justify-content:center;height:100%;color:var(--text3);font-size:14px;}
.det-header{margin-bottom:20px;}
.det-nome{font-size:22px;font-weight:900;margin-bottom:4px;}
.det-sub{font-size:13px;color:var(--text3);}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px;}
.kpi{background:var(--surf);border:1px solid var(--border);border-radius:var(--radius);padding:14px;position:relative;overflow:hidden;}
.kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.kpi.v::before{background:var(--green);}
.kpi.r::before{background:var(--red);}
.kpi.b::before{background:var(--blue);}
.kpi.a::before{background:var(--amber);}
.kv{font-size:30px;font-weight:900;line-height:1;font-family:monospace;}
.kpi.v .kv{color:var(--green);}
.kpi.r .kv{color:var(--red);}
.kpi.b .kv{color:var(--blue);}
.kpi.a .kv{color:var(--amber);}
.kl{font-size:11px;color:var(--text3);margin-top:3px;}
.info-card{background:var(--surf);border:1px solid var(--border);border-radius:var(--radius);padding:16px;margin-bottom:14px;}
.ic-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--blue);margin-bottom:12px;}
.info-row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border);font-size:12px;}
.info-row:last-child{border-bottom:none;}
.ik{color:var(--text3);}
.iv{font-weight:500;}
.badge{display:inline-block;padding:2px 8px;font-size:10px;font-weight:700;border-radius:20px;}
.b-ok{background:rgba(0,229,160,.1);color:var(--green);}
.b-down{background:rgba(255,68,102,.1);color:var(--red);}
.b-av{background:rgba(255,184,48,.1);color:var(--amber);}
.b-pause{background:rgba(74,101,128,.1);color:var(--text3);}
</style>
</head>
<body>
<div id="shell">
<div id="sb">
  <div class="sb-hd">
    <div class="sb-logo">
      <div class="sb-li"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14"/></svg></div>
      <div class="sb-lt">Hub<span>NOC</span></div>
    </div>
    <button class="sb-tog" onclick="toggleSB()"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
  <nav class="sb-nav">
    <div class="sb-g">VISÃO GERAL</div>
    <a class="ni" href="/dashboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg><span class="ni-l">Dashboard</span></a>
    <div class="sb-g">ATENDIMENTO</div>
    <a class="ni" href="/chamados"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 11 19.79 19.79 0 01.22 2.18 2 2 0 012.18 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 7.91a16 16 0 006.06 6.06l1.27-.53a2 2 0 012.11.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg><span class="ni-l">Chamados</span></a>
    <a class="ni" href="/incidentes"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg><span class="ni-l">Incidentes</span></a>
    <a class="ni" href="/alertas"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg><span class="ni-l">Alertas</span></a>
    <a class="ni" href="/cliente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg><span class="ni-l">Clientes</span></a>
    <div class="sb-g">MONITORAMENTO</div>
    <a class="ni" href="/sensores"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg><span class="ni-l">Sensores PRTG</span></a>
    <a class="ni on" href="/olts"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14"/><path d="M15.54 8.46a5 5 0 010 7.07M8.46 8.46a5 5 0 000 7.07"/></svg><span class="ni-l">Monitor OLTs</span></a>
    <a class="ni" href="/mapa"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg><span class="ni-l">Mapa de Rede</span></a>
    <div class="sb-g">SISTEMA</div>
    <a class="ni" href="/admin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg><span class="ni-l">Administração</span></a>
  </nav>
  <div class="sb-ft">
    <button class="btn-sair" onclick="sair()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg><span>Sair</span></button>
    <div class="sb-u">
      <div class="sb-av" id="sb-av">A</div>
      <div class="sb-ui"><div class="sb-un" id="sb-nome">—</div><div class="sb-ug">Online</div></div>
    </div>
  </div>
</div>
<div id="main">
  <div id="tb">
    <div class="tb-title">Monitor OLTs</div>
    <div class="tb-right">
      <div class="clock" id="clock">—</div>
      <a class="btn-tv" href="/tv" target="_blank"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="15" rx="2"/><polyline points="17 2 12 7 7 2"/></svg> TV NOC</a>
      <button class="btn-th" id="btn-th" onclick="toggleTheme()">☀️</button>
    </div>
  </div>
  <div id="content">
    <div class="olt-lista">
      <div class="ol-hd">
        <span class="ol-title">OLTs</span>
        <span class="ol-cnt" id="ol-cnt">—</span>
      </div>
      <div id="ol-lista">
        <div style="padding:24px;text-align:center;color:var(--text3);">Carregando...</div>
      </div>
    </div>
    <div class="olt-detalhe" id="olt-detalhe">
      <div class="det-empty">← Selecione uma OLT para ver detalhes</div>
    </div>
  </div>
</div>
</div>
<script>
var API='';
var token=localStorage.getItem('noc_token');
if(!token){window.location.href='/login';}
var _n=localStorage.getItem('noc_nome')||'—';
document.getElementById('sb-nome').textContent=_n;
document.getElementById('sb-av').textContent=_n.charAt(0).toUpperCase();
setInterval(function(){document.getElementById('clock').textContent=new Date().toLocaleTimeString('pt-BR');},1000);
document.getElementById('clock').textContent=new Date().toLocaleTimeString('pt-BR');
function toggleSB(){document.getElementById('sb').classList.toggle('col');}
function sair(){localStorage.clear();window.location.href='/login';}
function headers(){return{'Content-Type':'application/json','Authorization':'Bearer '+token};}
function esc(s){return(s||'').replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
(function(){var t=localStorage.getItem('noc_theme');if(t==='light'){document.body.classList.add('light');document.getElementById('btn-th').textContent='🌙';}})();
function toggleTheme(){document.body.classList.toggle('light');var l=document.body.classList.contains('light');document.getElementById('btn-th').textContent=l?'🌙':'☀️';localStorage.setItem('noc_theme',l?'light':'dark');}

var _olts=[];

function carregarOLTs(){
  fetch(API+'/api/olts/mapa',{headers:headers()})
  .then(function(r){return r.json();})
  .then(function(d){
    _olts=d||[];
    _olts.sort(function(a,b){
      var ord={DOWN:0,Aviso:1,Incomum:2,OK:3,Pausado:4};
      return (ord[a.prtg_status]||5)-(ord[b.prtg_status]||5);
    });
    document.getElementById('ol-cnt').textContent=_olts.length+' OLTs';
    var h='';
    _olts.forEach(function(o,i){
      var pct=o.total_clientes>0?Math.round((o.online/o.total_clientes)*100):0;
      var barCls=pct<70?'low':pct<90?'mid':'';
      var st=o.prtg_status||'OK';
      var dc=st==='DOWN'?'d-down':st==='Aviso'?'d-av':st==='Pausado'?'d-pause':'d-ok';
      var cls=st==='DOWN'?'down':st==='Aviso'?'aviso':'';
      h+='<div class="olt-item '+cls+'" id="oi-'+i+'" onclick="selecionarOLT('+i+')">'+
        '<div class="oi-top">'+
          '<span class="dot '+dc+'"></span>'+
          '<div class="oi-nome" title="'+esc(o.olt_nome)+'">'+esc(o.olt_nome)+'</div>'+
          '<span class="oi-online">'+o.online+'</span>'+
          '<span class="oi-total">/'+o.total_clientes+'</span>'+
        '</div>'+
        '<div class="oi-bar"><div class="oi-bar-fill '+barCls+'" style="width:'+pct+'%"></div></div>'+
        '<div class="oi-meta">'+esc(o.pop_nome||'—')+' · '+esc(o.modelo||'—')+' · <strong style="color:'+(st==='DOWN'?'var(--red)':st==='Aviso'?'var(--amber)':'var(--green)')+'">'+st+'</strong></div>'+
      '</div>';
    });
    document.getElementById('ol-lista').innerHTML=h;
  }).catch(function(){
    document.getElementById('ol-lista').innerHTML='<div style="padding:24px;text-align:center;color:var(--text3);">Erro ao carregar OLTs</div>';
  });
}

function selecionarOLT(i){
  document.querySelectorAll('.olt-item').forEach(function(el){el.classList.remove('sel');});
  var el=document.getElementById('oi-'+i);if(el)el.classList.add('sel');
  var o=_olts[i];if(!o)return;
  var st=o.prtg_status||'OK';
  var stBadge=st==='DOWN'?'b-down':st==='Aviso'?'b-av':st==='Pausado'?'b-pause':'b-ok';
  var pct=o.total_clientes>0?Math.round((o.online/o.total_clientes)*100):0;
  var barCls=pct<70?'low':pct<90?'mid':'';
  document.getElementById('olt-detalhe').innerHTML=
    '<div class="det-header">'+
      '<div class="det-nome">'+esc(o.olt_nome)+'</div>'+
      '<div class="det-sub">'+esc(o.pop_nome||'—')+' · '+esc(o.ip||'—')+'</div>'+
    '</div>'+
    '<div class="kpi-row">'+
      '<div class="kpi b"><div class="kv">'+o.total_clientes+'</div><div class="kl">TOTAL</div></div>'+
      '<div class="kpi v"><div class="kv">'+o.online+'</div><div class="kl">ONLINE</div></div>'+
      '<div class="kpi r"><div class="kv">'+(o.offline_problema||0)+'</div><div class="kl">PROBLEMA</div></div>'+
      '<div class="kpi a"><div class="kv">'+pct+'%</div><div class="kl">% ONLINE</div></div>'+
    '</div>'+
    '<div class="oi-bar" style="margin-bottom:16px;height:6px;"><div class="oi-bar-fill '+barCls+'" style="width:'+pct+'%"></div></div>'+
    '<div class="info-card">'+
      '<div class="ic-title">Informações</div>'+
      '<div class="info-row"><span class="ik">IP</span><span class="iv" style="font-family:monospace;">'+esc(o.ip||'—')+'</span></div>'+
      '<div class="info-row"><span class="ik">Modelo</span><span class="iv">'+esc(o.modelo||'—')+'</span></div>'+
      '<div class="info-row"><span class="ik">POP</span><span class="iv">'+esc(o.pop_nome||'—')+'</span></div>'+
      '<div class="info-row"><span class="ik">Uptime</span><span class="iv" style="font-family:monospace;">'+esc(o.uptime||'—')+'</span></div>'+
      '<div class="info-row"><span class="ik">Tráfego PRTG</span><span class="iv">'+esc(o.prtg_trafico||'—')+'</span></div>'+
      '<div class="info-row"><span class="ik">Status PRTG</span><span class="iv"><span class="badge '+stBadge+'">'+st+'</span></span></div>'+
      '<div class="info-row"><span class="ik">Suspensos</span><span class="iv" style="color:var(--amber);">'+esc(String(o.suspenso||0))+'</span></div>'+
    '</div>';
}

carregarOLTs();
setInterval(carregarOLTs,60000);
</script>
</body>
</html>"""

with open(os.path.join(STATIC, 'olts.html'), 'w') as f:
    f.write(olts)
print("olts.html OK")

# ── ADMIN.HTML ─────────────────────────────────────────────
admin = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HubNOC — Administração</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased;}
:root{--bg:#0a0f1a;--surf:#0f1623;--surf2:#151e2e;--surf3:#1a2438;--border:#1e2d45;--border2:#243450;--text:#e2eaf4;--text2:#8ba3be;--text3:#4a6580;--blue:#00aaff;--green:#00e5a0;--red:#ff4466;--amber:#ffb830;--radius:10px;--radius2:7px;--font:'Inter',system-ui,sans-serif;--sw:220px;--th:52px;}
body.light{--bg:#f0f4fa;--surf:#fff;--surf2:#e8edf5;--surf3:#dde3ef;--border:#cdd5e0;--border2:#bdc7d8;--text:#0f1623;--text2:#3a5070;--text3:#607a96;}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--font);font-size:13px;overflow:hidden;}
#shell{display:flex;height:100vh;}
#sb{width:var(--sw);background:var(--surf);border-right:1px solid var(--border);display:flex;flex-direction:column;flex-shrink:0;overflow:hidden;z-index:50;transition:width .25s cubic-bezier(.4,0,.2,1);}
#sb.col{width:52px;}
.sb-hd{padding:0 12px;height:var(--th);display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border);flex-shrink:0;}
.sb-logo{display:flex;align-items:center;gap:9px;flex:1;min-width:0;}
.sb-li{width:30px;height:30px;border-radius:8px;flex-shrink:0;background:linear-gradient(135deg,var(--blue),#0055aa);display:flex;align-items:center;justify-content:center;box-shadow:0 0 12px rgba(0,170,255,.3);}
.sb-li svg{width:15px;height:15px;color:#fff;}
.sb-lt{font-size:15px;font-weight:900;letter-spacing:-.3px;white-space:nowrap;overflow:hidden;}
.sb-lt span{color:var(--blue);}
.sb-tog{background:none;border:none;color:var(--text3);cursor:pointer;padding:5px;border-radius:5px;display:flex;flex-shrink:0;}
.sb-tog:hover{background:var(--surf2);color:var(--text);}
.sb-nav{flex:1;overflow-y:auto;padding:8px 6px;}
.sb-nav::-webkit-scrollbar{display:none;}
.sb-g{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);padding:10px 8px 4px;white-space:nowrap;overflow:hidden;}
#sb.col .sb-g{display:none;}
.ni{display:flex;align-items:center;gap:9px;padding:8px 9px;border-radius:var(--radius2);cursor:pointer;color:var(--text2);transition:all .15s;position:relative;white-space:nowrap;overflow:hidden;text-decoration:none;}
.ni:hover{background:var(--surf2);color:var(--text);}
.ni.on{background:rgba(0,170,255,.1);color:var(--blue);}
.ni.on::before{content:'';position:absolute;left:0;top:4px;bottom:4px;width:2px;background:var(--blue);border-radius:0 2px 2px 0;}
.ni svg{width:16px;height:16px;flex-shrink:0;}
.ni-l{font-size:13px;font-weight:500;}
#sb.col .ni-l{display:none;}
#sb.col .ni{justify-content:center;padding:9px;}
.sb-ft{padding:10px 6px;border-top:1px solid var(--border);}
.sb-u{display:flex;align-items:center;gap:9px;padding:8px;}
.sb-av{width:28px;height:28px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,var(--blue),var(--blue)88);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:#fff;}
.sb-ui{min-width:0;flex:1;}
.sb-un{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.sb-ug{font-size:10px;color:var(--text3);display:flex;align-items:center;gap:4px;margin-top:1px;}
.sb-ug::before{content:'';width:5px;height:5px;border-radius:50%;background:var(--green);flex-shrink:0;}
#sb.col .sb-ui{display:none;}
.btn-sair{width:100%;display:flex;align-items:center;gap:8px;padding:8px;border-radius:6px;background:rgba(255,68,102,.06);border:1px solid rgba(255,68,102,.15);color:var(--red);cursor:pointer;font-size:12px;font-weight:600;margin-bottom:6px;transition:.15s;}
.btn-sair:hover{background:rgba(255,68,102,.12);}
#sb.col .btn-sair span{display:none;}
#sb.col .btn-sair{justify-content:center;padding:9px;}
#main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0;}
#tb{height:var(--th);background:var(--surf);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 20px;gap:12px;flex-shrink:0;position:relative;}
#tb::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,var(--blue)40,transparent);}
.tb-title{font-size:14px;font-weight:700;flex:1;}
.tb-right{display:flex;align-items:center;gap:10px;margin-left:auto;}
.clock{font-family:monospace;font-size:13px;color:var(--blue);font-weight:700;}
.btn-tv{display:flex;align-items:center;gap:6px;background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.25);color:#a78bfa;padding:6px 14px;border-radius:var(--radius2);font-size:12px;font-weight:600;text-decoration:none;}
.btn-th{width:32px;height:32px;border-radius:50%;border:1px solid var(--border);background:var(--surf2);cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center;}
#content{flex:1;overflow-y:auto;padding:20px 24px;}
#content::-webkit-scrollbar{width:4px;}
#content::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px;}
.tabs{display:flex;gap:6px;margin-bottom:20px;}
.tab{padding:8px 18px;border-radius:var(--radius2);font-size:13px;font-weight:600;cursor:pointer;border:1px solid var(--border);background:var(--surf2);color:var(--text3);transition:.15s;}
.tab.on{background:rgba(0,170,255,.1);color:var(--blue);border-color:rgba(0,170,255,.3);}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;}
.kpi{background:var(--surf);border:1px solid var(--border);border-radius:var(--radius);padding:16px;position:relative;overflow:hidden;}
.kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.kpi.b::before{background:var(--blue);}
.kpi.r::before{background:var(--red);}
.kpi.a::before{background:var(--amber);}
.kpi.v::before{background:var(--green);}
.kv{font-size:32px;font-weight:900;line-height:1;}
.kpi.b .kv{color:var(--blue);}
.kpi.r .kv{color:var(--red);}
.kpi.a .kv{color:var(--amber);}
.kpi.v .kv{color:var(--green);}
.kl{font-size:11px;color:var(--text3);margin-top:4px;}
.card{background:var(--surf);border:1px solid var(--border);border-radius:var(--radius);}
.card-hd{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border);}
.card-title{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--blue);}
table{width:100%;border-collapse:collapse;}
thead th{text-align:left;padding:10px 14px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--text3);border-bottom:2px solid var(--border);}
tbody td{padding:12px 14px;border-bottom:1px solid var(--border);font-size:13px;vertical-align:middle;}
tbody tr:last-child td{border-bottom:none;}
.badge{display:inline-block;padding:3px 9px;font-size:10px;font-weight:700;border-radius:20px;}
.b-adm{background:rgba(255,68,102,.1);color:var(--red);}
.b-sup{background:rgba(255,184,48,.1);color:var(--amber);}
.b-ate{background:rgba(0,170,255,.1);color:var(--blue);}
.b-on{background:rgba(0,229,160,.1);color:var(--green);}
.b-off{background:rgba(74,101,128,.1);color:var(--text3);}
.ua{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff;flex-shrink:0;}
.btn-p{background:linear-gradient(135deg,var(--blue),#0077cc);border:none;color:#fff;padding:8px 16px;border-radius:var(--radius2);font-size:13px;font-weight:700;cursor:pointer;}
.btn-s{background:var(--surf2);border:1px solid var(--border);color:var(--text2);padding:8px 14px;border-radius:var(--radius2);font-size:13px;cursor:pointer;}
.btn-r{background:rgba(255,68,102,.08);border:1px solid rgba(255,68,102,.2);color:var(--red);padding:8px 14px;border-radius:var(--radius2);font-size:13px;cursor:pointer;font-weight:600;}
.ov{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:200;align-items:center;justify-content:center;backdrop-filter:blur(4px);}
.ov.show{display:flex;}
.modal{background:var(--surf);border:1px solid var(--border);border-radius:var(--radius);width:480px;max-width:95vw;}
.modal::before{content:'';display:block;height:2px;background:linear-gradient(90deg,var(--blue),transparent);border-radius:var(--radius) var(--radius) 0 0;}
.mhd{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid var(--border);font-weight:800;font-size:15px;}
.mbd{padding:20px;}
.mft{padding:12px 20px;border-top:1px solid var(--border);display:flex;gap:8px;justify-content:flex-end;}
.bx{background:none;border:none;color:var(--text3);font-size:20px;cursor:pointer;}
.fr{margin-bottom:14px;}
.fr label{display:block;font-size:10px;font-weight:700;letter-spacing:.08em;color:var(--text3);margin-bottom:6px;text-transform:uppercase;}
.fr input,.fr select{width:100%;background:var(--surf2);border:1px solid var(--border2);color:var(--text);padding:9px 12px;font-size:13px;font-family:var(--font);outline:none;border-radius:var(--radius2);}
.fr input:focus,.fr select:focus{border-color:var(--blue);}
.fr select option{background:var(--surf2);}
</style>
</head>
<body>
<div id="shell">
<div id="sb">
  <div class="sb-hd">
    <div class="sb-logo">
      <div class="sb-li"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14"/></svg></div>
      <div class="sb-lt">Hub<span>NOC</span></div>
    </div>
    <button class="sb-tog" onclick="toggleSB()"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>
  </div>
  <nav class="sb-nav">
    <div class="sb-g">VISÃO GERAL</div>
    <a class="ni" href="/dashboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg><span class="ni-l">Dashboard</span></a>
    <div class="sb-g">ATENDIMENTO</div>
    <a class="ni" href="/chamados"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 11 19.79 19.79 0 01.22 2.18 2 2 0 012.18 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.91 7.91a16 16 0 006.06 6.06l1.27-.53a2 2 0 012.11.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg><span class="ni-l">Chamados</span></a>
    <a class="ni" href="/incidentes"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg><span class="ni-l">Incidentes</span></a>
    <a class="ni" href="/alertas"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg><span class="ni-l">Alertas</span></a>
    <a class="ni" href="/cliente"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg><span class="ni-l">Clientes</span></a>
    <div class="sb-g">MONITORAMENTO</div>
    <a class="ni" href="/sensores"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg><span class="ni-l">Sensores PRTG</span></a>
    <a class="ni" href="/olts"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14"/><path d="M15.54 8.46a5 5 0 010 7.07M8.46 8.46a5 5 0 000 7.07"/></svg><span class="ni-l">Monitor OLTs</span></a>
    <a class="ni" href="/mapa"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg><span class="ni-l">Mapa de Rede</span></a>
    <div class="sb-g">SISTEMA</div>
    <a class="ni on" href="/admin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg><span class="ni-l">Administração</span></a>
  </nav>
  <div class="sb-ft">
    <button class="btn-sair" onclick="sair()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg><span>Sair</span></button>
    <div class="sb-u">
      <div class="sb-av" id="sb-av">A</div>
      <div class="sb-ui"><div class="sb-un" id="sb-nome">—</div><div class="sb-ug">Online</div></div>
    </div>
  </div>
</div>
<div id="main">
  <div id="tb">
    <div class="tb-title">Administração</div>
    <div class="tb-right">
      <div class="clock" id="clock">—</div>
      <a class="btn-tv" href="/tv" target="_blank"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="15" rx="2"/><polyline points="17 2 12 7 7 2"/></svg> TV NOC</a>
      <button class="btn-th" id="btn-th" onclick="toggleTheme()">☀️</button>
    </div>
  </div>
  <div id="content">
    <div class="tabs">
      <div class="tab on" onclick="abaUsuarios(this)">👥 Usuários</div>
    </div>
    <div class="kpi-row">
      <div class="kpi b"><div class="kv" id="adm-total">—</div><div class="kl">Total</div></div>
      <div class="kpi r"><div class="kv" id="adm-adm">—</div><div class="kl">Administradores</div></div>
      <div class="kpi a"><div class="kv" id="adm-sup">—</div><div class="kl">Supervisores</div></div>
      <div class="kpi v"><div class="kv" id="adm-ate">—</div><div class="kl">Atendentes</div></div>
    </div>
    <div class="card">
      <div class="card-hd">
        <span class="card-title">USUÁRIOS DO SISTEMA</span>
        <button class="btn-p" onclick="abrirNovoUsuario()">+ Novo Usuário</button>
      </div>
      <table>
        <thead><tr><th>Usuário</th><th>Nível</th><th>Status</th><th>Cadastrado em</th><th>Ações</th></tr></thead>
        <tbody id="tbody-usr"><tr><td colspan="5" style="padding:24px;text-align:center;color:var(--text3);">Carregando...</td></tr></tbody>
      </table>
    </div>
  </div>
</div>
</div>

<div class="ov" id="modal-usr">
  <div class="modal">
    <div class="mhd" id="musr-titulo">Novo Usuário <button class="bx" onclick="fecharUsr()">×</button></div>
    <div class="mbd">
      <div class="fr"><label>Nome completo</label><input type="text" id="u-nome" placeholder="Ex: João Silva"></div>
      <div class="fr"><label>Login</label><input type="text" id="u-login" placeholder="Ex: joao.silva"></div>
      <div class="fr"><label>Senha</label><input type="password" id="u-senha" placeholder="Mínimo 6 caracteres"></div>
      <div class="fr"><label>Nível de acesso</label>
        <select id="u-nivel">
          <option value="10">Atendente</option>
          <option value="50">Supervisor</option>
          <option value="99">Administrador</option>
        </select>
      </div>
    </div>
    <div class="mft"><button class="btn-s" onclick="fecharUsr()">Cancelar</button><button class="btn-p" onclick="salvarUsuario()">Salvar</button></div>
  </div>
</div>

<div class="ov" id="modal-senha">
  <div class="modal">
    <div class="mhd">Alterar Senha <button class="bx" onclick="fecharSenha()">×</button></div>
    <div class="mbd">
      <div class="fr"><label>Nova senha</label><input type="password" id="s-nova" placeholder="Mínimo 6 caracteres"></div>
      <div class="fr"><label>Confirmar senha</label><input type="password" id="s-conf" placeholder="Repita a senha"></div>
    </div>
    <div class="mft"><button class="btn-s" onclick="fecharSenha()">Cancelar</button><button class="btn-p" onclick="salvarSenha()">Alterar</button></div>
  </div>
</div>

<script>
var API='';
var token=localStorage.getItem('noc_token');
if(!token){window.location.href='/login';}
var _n=localStorage.getItem('noc_nome')||'—';
document.getElementById('sb-nome').textContent=_n;
document.getElementById('sb-av').textContent=_n.charAt(0).toUpperCase();
setInterval(function(){document.getElementById('clock').textContent=new Date().toLocaleTimeString('pt-BR');},1000);
document.getElementById('clock').textContent=new Date().toLocaleTimeString('pt-BR');
function toggleSB(){document.getElementById('sb').classList.toggle('col');}
function sair(){localStorage.clear();window.location.href='/login';}
function headers(){return{'Content-Type':'application/json','Authorization':'Bearer '+token};}
function esc(s){return(s||'').replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
(function(){var t=localStorage.getItem('noc_theme');if(t==='light'){document.body.classList.add('light');document.getElementById('btn-th').textContent='🌙';}})();
function toggleTheme(){document.body.classList.toggle('light');var l=document.body.classList.contains('light');document.getElementById('btn-th').textContent=l?'🌙':'☀️';localStorage.setItem('noc_theme',l?'light':'dark');}
function abaUsuarios(el){document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('on');});el.classList.add('on');carregarUsuarios();}
var _editId=null, _senhaId=null;
function carregarUsuarios(){
  fetch(API+'/api/admin/usuarios',{headers:headers()}).then(function(r){return r.json();}).then(function(l){
    var adm=0,sup=0,ate=0;
    l.forEach(function(u){if(u.nivel>=99)adm++;else if(u.nivel>=50)sup++;else ate++;});
    document.getElementById('adm-total').textContent=l.length;
    document.getElementById('adm-adm').textContent=adm;
    document.getElementById('adm-sup').textContent=sup;
    document.getElementById('adm-ate').textContent=ate;
    var h='';
    l.forEach(function(u){
      var nc=u.nivel>=99?'b-adm':u.nivel>=50?'b-sup':'b-ate';
      var nl=u.nivel>=99?'Administrador':u.nivel>=50?'Supervisor':'Atendente';
      var sc=u.ativo?'b-on':'b-off';
      var sl=u.ativo?'● Ativo':'Inativo';
      var cor=u.nivel>=99?'#ff4466':u.nivel>=50?'#ffb830':'#00aaff';
      h+='<tr>'+
        '<td><div style="display:flex;align-items:center;gap:10px;">'+
          '<div class="ua" style="background:linear-gradient(135deg,'+cor+','+cor+'88);">'+esc(u.nome.charAt(0).toUpperCase())+'</div>'+
          '<div><div style="font-weight:600;">'+esc(u.nome)+'</div><div style="font-size:11px;color:var(--text3);">'+esc(u.login)+'</div></div>'+
        '</div></td>'+
        '<td><span class="badge '+nc+'">'+nl+'</span></td>'+
        '<td><span class="badge '+sc+'">'+sl+'</span></td>'+
        '<td style="font-family:monospace;font-size:11px;color:var(--text3);">'+(u.criado_em||'—').substring(0,10)+'</td>'+
        '<td><div style="display:flex;gap:6px;">'+
          '<button onclick="editarUsr('+u.id+')" class="btn-s" style="padding:5px 10px;font-size:11px;">✏ Editar</button>'+
          '<button onclick="alterarSenha('+u.id+')" class="btn-s" style="padding:5px 10px;font-size:11px;">🔑 Senha</button>'+
          '<button onclick="bloquearUsr('+u.id+','+u.ativo+')" class="btn-r" style="padding:5px 10px;font-size:11px;">'+(u.ativo?'🚫 Bloquear':'✓ Ativar')+'</button>'+
        '</div></td>'+
      '</tr>';
    });
    document.getElementById('tbody-usr').innerHTML=h||'<tr><td colspan="5" style="padding:24px;text-align:center;color:var(--text3);">Nenhum usuário</td></tr>';
  }).catch(function(){});
}
function abrirNovoUsuario(){_editId=null;document.getElementById('musr-titulo').innerHTML='Novo Usuário <button class="bx" onclick="fecharUsr()">×</button>';document.getElementById('u-nome').value='';document.getElementById('u-login').value='';document.getElementById('u-senha').value='';document.getElementById('u-nivel').value='10';document.getElementById('modal-usr').classList.add('show');}
function fecharUsr(){document.getElementById('modal-usr').classList.remove('show');}
function editarUsr(id){_editId=id;document.getElementById('musr-titulo').innerHTML='Editar Usuário <button class="bx" onclick="fecharUsr()">×</button>';document.getElementById('u-senha').placeholder='Deixe em branco para não alterar';document.getElementById('modal-usr').classList.add('show');}
function salvarUsuario(){
  var nome=document.getElementById('u-nome').value.trim();
  var login=document.getElementById('u-login').value.trim();
  var senha=document.getElementById('u-senha').value;
  var nivel=parseInt(document.getElementById('u-nivel').value);
  if(!nome||!login){alert('Preencha nome e login');return;}
  if(!_editId&&!senha){alert('Informe a senha');return;}
  var b={nome:nome,login:login,nivel:nivel};
  if(senha)b.senha=senha;
  var method=_editId?'PUT':'POST';
  var url=API+'/api/admin/usuarios'+(_editId?'/'+_editId:'');
  fetch(url,{method:method,headers:headers(),body:JSON.stringify(b)}).then(function(r){return r.json();}).then(function(){fecharUsr();carregarUsuarios();}).catch(function(){alert('Erro');});
}
function alterarSenha(id){_senhaId=id;document.getElementById('s-nova').value='';document.getElementById('s-conf').value='';document.getElementById('modal-senha').classList.add('show');}
function fecharSenha(){document.getElementById('modal-senha').classList.remove('show');}
function salvarSenha(){var nova=document.getElementById('s-nova').value;var conf=document.getElementById('s-conf').value;if(nova.length<6){alert('Senha mínimo 6 caracteres');return;}if(nova!==conf){alert('Senhas não conferem');return;}fetch(API+'/api/admin/usuarios/'+_senhaId+'/senha',{method:'PUT',headers:headers(),body:JSON.stringify({senha:nova})}).then(function(r){return r.json();}).then(function(){fecharSenha();alert('Senha alterada!');}).catch(function(){alert('Erro');});}
function bloquearUsr(id,ativo){if(!confirm(ativo?'Bloquear usuário?':'Ativar usuário?'))return;fetch(API+'/api/admin/usuarios/'+id,{method:'PUT',headers:headers(),body:JSON.stringify({ativo:!ativo})}).then(function(r){return r.json();}).then(function(){carregarUsuarios();}).catch(function(){alert('Erro');});}
carregarUsuarios();
</script>
</body>
</html>"""

with open(os.path.join(STATIC, 'admin.html'), 'w') as f:
    f.write(admin)
print("admin.html OK")

import subprocess
subprocess.run(['systemctl','restart','hubnoc_cliquedf'])
print("Serviço reiniciado!")
print("\nDone! Acesse /olts e /admin para verificar.")
