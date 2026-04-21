"""
Daily Jenisha Love Page Generator  v4.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULE: Every page is a completely original story. No concept is ever repeated.
Each theme has its own unique visual mechanic — they look nothing like each other.
Messages: 2-4 lines, written like a real person, not a greeting card.
No confetti. No random emoji buttons. The animation IS the message.

Story roster (one per theme, never repeated):
  galaxy    → CONSTELLATION: stars appear, lines draw, heart forms in the night sky
  sakura    → TREE: bare trunk grows, heart-shaped canopy blooms                [done Apr 21]
  ocean     → BOTTLE: waves, bottle washes ashore, cork pops, scroll unrolls
  firefly   → FIREFLY SPELL: fireflies drift, arrange into her name, swarm into heart
  neon      → TERMINAL: retro CRT types "SEARCHING... FOUND:", glitches into neon
  aurora    → RIBBON DANCE: aurora curtains ripple, pool into glowing words
  sunrise   → SKY SHIFT: full night→dawn→gold sunrise, message revealed by light
  rain      → FOGGY GLASS: rain streaks, finger draws heart in condensation, message writes in fog
  particle  → HEARTBEAT: EKG flatlines, one huge beat, spike morphs into glowing heart
  matrix    → CODE LOCK: matrix rain, characters slow and lock into her name
  butterfly → CHRYSALIS: cocoon shakes, butterfly emerges, wings spread, wings form heart
  campfire  → MATCH LIGHT: match strikes, candle lights, warm glow reveals handwritten note
"""

import os, json, subprocess, datetime, sys, time, tempfile, urllib.request, urllib.error
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
def load_config():
    cfg = {
        "GITHUB_TOKEN":    os.environ.get("GH_PAT", ""),
        "GITHUB_USERNAME": os.environ.get("GH_USERNAME", "dipeshrayg"),
        "GITHUB_EMAIL":    os.environ.get("GH_EMAIL", "dipesh.ray.g@gmail.com"),
        "HER_NAME":        os.environ.get("HER_NAME", "Jenisha"),
    }
    env_file = Path(__file__).parent / ".env"
    if env_file.exists() and not cfg["GITHUB_TOKEN"]:
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                MAP = {"GITHUB_TOKEN":"GITHUB_TOKEN","GITHUB_USERNAME":"GITHUB_USERNAME",
                       "GITHUB_EMAIL":"GITHUB_EMAIL","HER_NAME":"HER_NAME"}
                if k.strip() in MAP: cfg[MAP[k.strip()]] = v.strip()
    return cfg

cfg      = load_config()
TOKEN    = cfg["GITHUB_TOKEN"]
USERNAME = cfg["GITHUB_USERNAME"]
EMAIL    = cfg["GITHUB_EMAIL"]
HER_NAME = cfg["HER_NAME"]

if not TOKEN:
    print("❌  No token found. Set GH_PAT env var or create .env file.")
    sys.exit(1)


# ── Shared CSS / card helper ────────────────────────────────────────────────────
def card_css(cb, ct, ca, g):
    return f"""
#card{{position:fixed;left:50%;bottom:-260px;transform:translateX(-50%);width:min(360px,90vw);
  background:{cb};border-radius:18px;padding:28px 30px 24px;
  box-shadow:0 16px 70px rgba(0,0,0,.5),0 0 0 1px rgba({g},.2);
  z-index:60;transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;
  border:1px solid rgba({g},.15)}}
#card.show{{bottom:clamp(20px,4vh,55px)}}
.cto{{font-family:'Caveat',cursive;font-size:.82rem;letter-spacing:.15em;color:rgba({g},.5);text-transform:uppercase;margin-bottom:12px}}
.cmsg{{font-family:'Caveat',cursive;font-size:clamp(1.2rem,3.5vw,1.45rem);line-height:1.75;color:{ct};min-height:4rem;white-space:pre-wrap}}
.cfrom{{margin-top:16px;font-family:'Dancing Script',cursive;font-size:1.5rem;color:{ca};text-align:right}}
.cdate{{font-size:.68rem;color:rgba({g},.3);text-align:right;margin-top:2px;letter-spacing:.06em}}"""

def card_html(name, date_str):
    return f"""<div id="card">
  <div class="cto">for {name.lower()}</div>
  <div class="cmsg" id="cmsg"></div>
  <div class="cfrom">— Dipesh</div>
  <div class="cdate">{date_str}</div>
</div>"""

def start_html(name, p, g):
    return f"""<div id="start" onclick="begin()">
  <div class="sn">{name}</div>
  <div class="sh">tap to open</div>
</div>"""

def start_css(p, g):
    return f"""
#start{{position:fixed;inset:0;z-index:80;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:18px;
  transition:opacity 1.4s ease;cursor:pointer}}
#start.gone{{opacity:0;pointer-events:none}}
.sn{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,13vw,6.5rem);
  color:{p};text-shadow:0 0 50px rgba({g},.5),0 0 100px rgba({g},.2);
  animation:sglow 2.8s ease-in-out infinite}}
.sh{{font-family:'Caveat',cursive;font-size:clamp(1rem,3.5vw,1.3rem);
  letter-spacing:.18em;color:rgba({g},.45);animation:sbl 2s ease-in-out infinite}}
@keyframes sglow{{0%,100%{{text-shadow:0 0 40px rgba({g},.4)}}50%{{text-shadow:0 0 70px rgba({g},.7)}}}}
@keyframes sbl{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}"""

TYPEWRITER_JS = """
function typeMsg(el,text,spd){el.textContent='';let i=0;const iv=setInterval(()=>{
  if(i>=text.length){clearInterval(iv);return;}
  el.textContent+=text[i++];
},spd);}
function showCard(){document.getElementById('card').classList.add('show');
  setTimeout(()=>typeMsg(document.getElementById('cmsg'),MSG,42),700);}
"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Caveat:wght@400;600&display=swap" rel="stylesheet"/>'


# ══════════════════════════════════════════════════════════════════════════════
# 1. GALAXY — Constellation connect: stars appear → lines draw → heart in sky
# ══════════════════════════════════════════════════════════════════════════════
def html_galaxy(name, date_str):
    msg = "Some things only make sense\nwhen you connect the dots.\n\nYou were always the pattern."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#03001a}}
{start_css('#a78bfa','138,90,255')}
{card_css('rgba(8,4,24,.97)','#e0d0ff','#a78bfa','138,90,255')}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#a78bfa','138,90,255')}
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;
{TYPEWRITER_JS}
// Background stars
const BGSTARS=Array.from({{length:300}},()=>({{'x':Math.random(),'y':Math.random(),'r':.2+Math.random()*1.2,'a':.1+Math.random()*.5,'tp':Math.random()*Math.PI*2,'ts':.005+Math.random()*.012}}));
function drawBg(){{
  ctx.fillStyle='#03001a';ctx.fillRect(0,0,W,H);
  BGSTARS.forEach(s=>{{s.tp+=s.ts;const a=s.a+Math.sin(s.tp)*.15;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(200,180,255,${{Math.max(0,a)}})`;ctx.fill()}});
}}
// Heart constellation points
function heartPts(n,cx,cy,sc){{
  const pts=[];
  for(let i=0;i<n;i++){{
    const t=(i/n)*Math.PI*2;
    const x=16*Math.pow(Math.sin(t),3);
    const y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));
    pts.push({{x:cx+x*sc,y:cy+y*sc,lit:false,litT:0}});
  }}
  return pts;
}}
let phase=0,elapsed=0,prevT=0;
let CSTARS=[],lineProgress=0,cardDone=false;
function init(){{
  const sc=Math.min(W*.024,H*.02);
  CSTARS=heartPts(22,W/2,H*.43,sc);
  CSTARS.forEach((s,i)=>{{s.litDelay=i*.08+Math.random()*.06;}});
}}
function begin(){{
  document.getElementById('start').classList.add('gone');
  init();
  setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);
}}
function loop(ts){{
  if(!prevT)prevT=ts;
  const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  drawBg();
  if(phase===1){{
    // Stars appear one by one
    CSTARS.forEach((s,i)=>{{
      if(elapsed>s.litDelay){{s.lit=true;s.litT=Math.min(1,s.litT+dt*3);}}
      if(!s.lit)return;
      const glow=ctx.createRadialGradient(s.x,s.y,0,s.x,s.y,12*s.litT);
      glow.addColorStop(0,'rgba(200,160,255,.9)');glow.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=glow;ctx.fillRect(s.x-14,s.y-14,28,28);
      ctx.beginPath();ctx.arc(s.x,s.y,2.5*s.litT,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();
    }});
    const lastDelay=CSTARS[CSTARS.length-1].litDelay+.5;
    if(elapsed>lastDelay){{phase=2;elapsed=0;}}
  }}
  if(phase>=2){{
    // Draw all stars
    CSTARS.forEach(s=>{{
      const g=ctx.createRadialGradient(s.x,s.y,0,s.x,s.y,12);
      g.addColorStop(0,'rgba(200,160,255,.9)');g.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=g;ctx.fillRect(s.x-14,s.y-14,28,28);
      ctx.beginPath();ctx.arc(s.x,s.y,2.5,0,Math.PI*2);ctx.fillStyle='#fff';ctx.fill();
    }});
  }}
  if(phase===2){{
    // Draw constellation lines progressively
    lineProgress=Math.min(1,elapsed/2.5);
    const totalSegs=CSTARS.length;
    const drawn=lineProgress*totalSegs;
    ctx.strokeStyle='rgba(180,140,255,.35)';ctx.lineWidth=1.2;ctx.setLineDash([4,6]);
    for(let i=0;i<Math.floor(drawn);i++){{
      const a=CSTARS[i],b=CSTARS[(i+1)%CSTARS.length];
      ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
    }}
    // Partial last segment
    const partial=drawn-Math.floor(drawn);
    if(Math.floor(drawn)<totalSegs){{
      const a=CSTARS[Math.floor(drawn)],b=CSTARS[(Math.floor(drawn)+1)%CSTARS.length];
      ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(a.x+(b.x-a.x)*partial,a.y+(b.y-a.y)*partial);ctx.stroke();
    }}
    ctx.setLineDash([]);
    if(lineProgress>=1&&!cardDone){{cardDone=true;phase=3;setTimeout(showCard,600);}}
  }}
  if(phase===3){{
    // Full constellation glowing
    ctx.strokeStyle='rgba(180,140,255,.35)';ctx.lineWidth=1.2;ctx.setLineDash([4,6]);
    for(let i=0;i<CSTARS.length;i++){{const a=CSTARS[i],b=CSTARS[(i+1)%CSTARS.length];ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}}
    ctx.setLineDash([]);
    // Pulse glow on heart
    const pulse=.5+.5*Math.sin(elapsed*2);
    const hg=ctx.createRadialGradient(W/2,H*.43,0,W/2,H*.43,Math.min(W,H)*.22);
    hg.addColorStop(0,`rgba(138,90,255,${{.06+pulse*.04}})`);hg.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=hg;ctx.fillRect(0,0,W,H);
  }}
  requestAnimationFrame(loop);
}}
function idleLoop(){{if(phase>0)return;drawBg();requestAnimationFrame(idleLoop);}}
requestAnimationFrame(idleLoop);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;if(phase>0)init();}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 2. SAKURA — Tree (already deployed Apr 21, kept for cycle continuity)
# ══════════════════════════════════════════════════════════════════════════════
def html_sakura(name, date_str):
    msg = "Made this for you.\nCouldn't fit all the reasons\nonto one tree.\n\nSo I just used blossoms."
    pc = json.dumps(["#ffb7c5","#ffc8d4","#ffdde8","#ffadc0","#ffe0ea"])
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#18060f}}
{start_css('#ffb7c5','255,150,200')}
{card_css('rgba(255,251,252,.97)','#3a1020','#c2185b','255,150,200')}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#ffb7c5','255,150,200')}
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
const STARS=Array.from({{length:220}},()=>({{'x':Math.random(),'y':Math.random(),'r':.3+Math.random()*1.4,'base':.1+Math.random()*.55,'tp':Math.random()*Math.PI*2,'ts':.006+Math.random()*.014}}));
function drawBg(){{const bg=ctx.createRadialGradient(W/2,H*.41,0,W/2,H*.41,Math.max(W,H)*.75);bg.addColorStop(0,'#18060f');bg.addColorStop(1,'#080208');ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);STARS.forEach(s=>{{s.tp+=s.ts;const a=s.base+Math.sin(s.tp)*.22;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(255,210,225,${{Math.max(0,a)}})`;ctx.fill()}});}}
let HCX=W/2,HCY=H*.41,S=Math.min(W*.022,H*.018);
function recalc(){{HCX=W/2;HCY=H*.41;S=Math.min(W*.022,H*.018);}}
function heartPt(t){{const x=16*Math.pow(Math.sin(t),3),y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));return{{x:HCX+x*S,y:HCY+y*S}};}}
const N=28;let BR=[];
function buildBr(){{BR=[];const tipY=heartPt(Math.PI).y,baseY=H*.855;for(let i=0;i<N;i++){{const t=(i/N)*Math.PI*2,tip=heartPt(t);const vf=Math.max(0,Math.min(.72,(tip.y-tipY)/(baseY-tipY)));const bx=HCX+(tip.x-HCX)*.06,by=tipY+vf*(baseY-tipY);const cx2=bx+(tip.x-bx)*.42+(Math.random()-.5)*S*4,cy2=by+(tip.y-by)*.36-S*6;const thick=1.2+Math.max(0,(tip.y-HCY)/(17*S))*2;BR.push({{base:{{x:bx,y:by}},ctrl:{{x:cx2,y:cy2}},tip,progress:0,delay:i*.038,width:thick}});}}}}
buildBr();
function bPt(p0,p1,p2,t){{const u=1-t;return{{x:u*u*p0.x+2*u*t*p1.x+t*t*p2.x,y:u*u*p0.y+2*u*t*p1.y+t*t*p2.y}};}}
function drawBr(b,p){{if(p<=0)return;const steps=24;ctx.beginPath();ctx.moveTo(b.base.x,b.base.y);const end=Math.min(1,p);for(let i=1;i<=steps;i++){{const f=i/steps;if(f>end+.001)break;const pt=bPt(b.base,b.ctrl,b.tip,Math.min(end,f));ctx.lineTo(pt.x,pt.y);}}ctx.strokeStyle='rgba(90,52,22,.82)';ctx.lineWidth=b.width;ctx.lineCap='round';ctx.stroke();}}
function drawTrunk(p){{if(p<=0)return;const tipY=heartPt(Math.PI).y,baseY=H*.855;for(let i=0;i<28;i++){{const f0=i/28,f1=(i+1)/28;if(f0>p)break;const y0=baseY-(baseY-tipY)*f0,y1=baseY-(baseY-tipY)*Math.min(p,f1);ctx.beginPath();ctx.moveTo(HCX,y0);ctx.lineTo(HCX,y1);ctx.strokeStyle='rgba(70,38,14,.88)';ctx.lineWidth=Math.max(1.5,11-f0*7.5);ctx.lineCap='round';ctx.stroke();}}}}
const PC={pc};
function drawBlossom(x,y,sz,a){{if(a<=0||sz<=0)return;ctx.save();ctx.globalAlpha=Math.min(1,a);for(let i=0;i<5;i++){{const ang=(i/5)*Math.PI*2-Math.PI/10;ctx.beginPath();ctx.arc(x+Math.cos(ang)*sz*.62,y+Math.sin(ang)*sz*.62,sz*.54,0,Math.PI*2);ctx.fillStyle=PC[i%PC.length];ctx.fill();}}ctx.beginPath();ctx.arc(x,y,sz*.3,0,Math.PI*2);ctx.fillStyle='#fffde7';ctx.fill();ctx.restore();}}
const PTLS=[];class FP{{constructor(){{this.x=Math.random()*W*1.3-W*.15;this.y=-16;this.vx=-.4+Math.random()*.9;this.vy=.5+Math.random()*1.1;this.rot=Math.random()*Math.PI*2;this.rs=(Math.random()-.5)*.045;this.sz=3.5+Math.random()*5;this.a=.45+Math.random()*.45;this.col=PC[Math.floor(Math.random()*PC.length)];}}tick(){{this.x+=this.vx;this.y+=this.vy;this.rot+=this.rs;this.vx+=(Math.random()-.5)*.04;if(this.y>H+20){{this.x=Math.random()*W*1.3-W*.15;this.y=-16;}}}}draw(){{ctx.save();ctx.translate(this.x,this.y);ctx.rotate(this.rot);ctx.globalAlpha=this.a;ctx.beginPath();ctx.ellipse(0,0,this.sz,this.sz*.55,0,0,Math.PI*2);ctx.fillStyle=this.col;ctx.fill();ctx.restore();}}}}
let phase=0,tp=0,el=0,pT=0,done=false;
function begin(){{document.getElementById('start').classList.add('gone');setTimeout(()=>{{phase=1;pT=performance.now();requestAnimationFrame(loop);}},1400);}}
function loop(ts){{if(!pT)pT=ts;const dt=Math.min(.08,(ts-pT)/1000);pT=ts;el+=dt;drawBg();
if(phase>=3){{const g=ctx.createRadialGradient(HCX,HCY-S*2,0,HCX,HCY,S*22);g.addColorStop(0,'rgba(255,150,200,.07)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);}}
if(phase===1){{tp=Math.min(1,el/1.3);drawTrunk(tp);if(tp>=1){{phase=2;el=0;}}}}
if(phase>=2)drawTrunk(1);
if(phase>=2){{let done2=true;BR.forEach(b=>{{if(phase===2)b.progress=Math.min(1,Math.max(0,(el-b.delay)/.65));if(b.progress<1)done2=false;drawBr(b,b.progress);}});if(phase===2&&done2){{phase=3;el=0;for(let i=0;i<55;i++)PTLS.push(new FP());}}}}
if(phase>=3){{BR.forEach((b,i)=>{{const bp=Math.min(1,Math.max(0,(el-i*.055)/.45));drawBlossom(b.tip.x,b.tip.y,S*1.25*bp,bp);}});if(phase===3){{const last=BR.length*.055+.45;if(el>last+.9&&!done){{done=true;phase=4;el=0;setTimeout(showCard,500);}}}}}}
if(phase===4){{BR.forEach(b=>drawBlossom(b.tip.x,b.tip.y,S*1.25,1));PTLS.forEach(p=>{{p.tick();p.draw();}});}}
requestAnimationFrame(loop);}}
function idle(){{if(phase>0)return;drawBg();requestAnimationFrame(idle);}}requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;recalc();buildBr();}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 3. OCEAN — Message in a bottle washes ashore
# ══════════════════════════════════════════════════════════════════════════════
def html_ocean(name, date_str):
    msg = "I put this in a bottle\nand trusted the ocean.\n\nHope it found you."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#001828;font-family:'Caveat',cursive}}
{start_css('#4fc3f7','79,195,247')}
{card_css('rgba(255,252,245,.97)','#1a3a50','#0288d1','79,195,247')}
#scene{{position:fixed;inset:0;z-index:10;pointer-events:none;overflow:hidden}}
.bottle{{position:absolute;font-size:clamp(3rem,10vw,5rem);bottom:-120px;left:50%;transform:translateX(-50%) rotate(-15deg);transition:bottom 2.5s cubic-bezier(.2,.8,.3,1),transform 2s ease;filter:drop-shadow(0 8px 20px rgba(0,100,150,.4))}}
.bottle.ashore{{bottom:22%;transform:translateX(-50%) rotate(8deg)}}
.scroll{{position:absolute;background:#fffef5;border-radius:8px;padding:20px 22px;width:min(300px,80vw);font-size:clamp(1rem,3vw,1.15rem);line-height:1.7;color:#1a2a40;box-shadow:0 8px 30px rgba(0,0,0,.25);left:50%;transform:translateX(-50%) translateY(40px);opacity:0;transition:opacity .8s ease,transform .8s ease;top:18%}}
.scroll.open{{opacity:1;transform:translateX(-50%) translateY(0)}}
.scroll-name{{font-family:'Dancing Script',cursive;font-size:1.5rem;color:#0277bd;margin-bottom:8px}}
.scroll-msg{{white-space:pre-wrap;min-height:3em}}
.scroll-from{{font-family:'Dancing Script',cursive;font-size:1.2rem;color:#0277bd;text-align:right;margin-top:10px}}
.scroll-date{{font-size:.65rem;color:rgba(0,0,0,.3);text-align:right}}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#4fc3f7','79,195,247')}
<div id="scene">
  <div class="bottle" id="bottle">🍾</div>
  <div class="scroll" id="scroll">
    <div class="scroll-name">Hey {name},</div>
    <div class="scroll-msg" id="smsg"></div>
    <div class="scroll-from">— Dipesh</div>
    <div class="scroll-date">{date_str}</div>
  </div>
</div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;
function typeMsg(el,text,spd){{el.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=text.length){{clearInterval(iv);return;}}el.textContent+=text[i++];}},spd);}}
// Wave system
const waves=[];
for(let i=0;i<5;i++)waves.push({{ph:Math.random()*Math.PI*2,spd:.008+Math.random()*.006,amp:18+i*12,yFrac:.55+i*.07,alpha:.15+i*.04}});
let wt=0;
function drawScene(){{
  const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'#001828');bg.addColorStop(.5,'#002a40');bg.addColorStop(1,'#003350');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
  // Stars in sky
  if(!window._wstars)window._wstars=Array.from({{length:120}},()=>({{'x':Math.random(),'y':Math.random()*.45,'r':.3+Math.random()*1,'a':.1+Math.random()*.4,'tp':Math.random()*Math.PI*2,'ts':.005+Math.random()*.01}}));
  window._wstars.forEach(s=>{{s.tp+=s.ts;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(180,230,255,${{Math.max(0,s.a+Math.sin(s.tp)*.15)}})`;ctx.fill()}});
  wt+=.012;
  waves.forEach(w=>{{
    ctx.beginPath();ctx.moveTo(0,w.yFrac*H);
    for(let x=0;x<=W+4;x+=4){{ctx.lineTo(x,w.yFrac*H+Math.sin(x*.005+w.ph+wt*w.spd*100)*w.amp);}}
    ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();
    ctx.fillStyle=`rgba(0,100,170,${{w.alpha}})`;ctx.fill();w.ph+=w.spd;
  }});
  // Moon
  ctx.beginPath();ctx.arc(W*.75,H*.12,22,0,Math.PI*2);ctx.fillStyle='rgba(220,240,255,.18)';ctx.fill();
  ctx.beginPath();ctx.arc(W*.75+8,H*.12-3,20,0,Math.PI*2);ctx.fillStyle='#001828';ctx.fill();
}}
function begin(){{
  document.getElementById('start').classList.add('gone');
  // Bottle washes in
  setTimeout(()=>document.getElementById('bottle').classList.add('ashore'),1400);
  // Cork pops → scroll appears
  setTimeout(()=>{{
    document.getElementById('bottle').textContent='✉️';
    setTimeout(()=>{{
      document.getElementById('scroll').classList.add('open');
      setTimeout(()=>typeMsg(document.getElementById('smsg'),MSG,44),600);
    }},600);
  }},4200);
}}
function loop(){{ctx.clearRect(0,0,W,H);drawScene();requestAnimationFrame(loop);}}loop();
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 4. FIREFLY — Fireflies drift, spell her name, swarm into heart
# ══════════════════════════════════════════════════════════════════════════════
def html_firefly(name, date_str):
    msg = "You make quiet places\nfeel less quiet.\n\nThought you should know that."
    name_upper = name.upper()
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#03080a}}
{start_css('#b8ff6e','184,255,110')}
{card_css('rgba(4,12,6,.97)','#c8ffb0','#aaee44','160,240,60')}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#b8ff6e','184,255,110')}
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
// Phase: 0=idle, 1=drift, 2=spelling name, 3=swarm to heart, 4=heart+card
let phase=0,elapsed=0,prevT=0,cardDone=false;
// Heart target points
function heartPts(n,cx,cy,sc){{const pts=[];for(let i=0;i<n;i++){{const t=(i/n)*Math.PI*2,x=16*Math.pow(Math.sin(t),3),y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));pts.push({{x:cx+x*sc,y:cy+y*sc}});}}return pts;}}
// Simple letter pixel positions for name
function letterPts(char,ox,oy,sz){{
  const segs={{
    'A':[[.5,0,0,1],[.5,0,1,1],[0,1,.15,.5],[.85,.5,1,.5]],
    'B':[[0,0,0,1],[0,0,.7,0],[0,.5,.7,.5],[0,1,.7,1],[.7,0,.9,.2],[.9,.2,.7,.5],[.7,.5,.9,.7],[.9,.7,.7,1]],
    'C':[[.9,.1,0,.1],[0,.1,0,.9],[0,.9,.9,.9]],
    'D':[[0,0,0,1],[0,0,.6,0],[.6,0,1,.3],[1,.3,1,.7],[1,.7,.6,1],[.6,1,0,1]],
    'E':[[0,0,0,1],[0,0,1,0],[0,.5,.8,.5],[0,1,1,1]],
    'F':[[0,0,0,1],[0,0,1,0],[0,.5,.8,.5]],
    'G':[[1,.1,.3,.1],[.3,.1,0,.3],[0,.3,0,.7],[0,.7,.3,.9],[.3,.9,1,.9],[1,.9,1,.5],[1,.5,.6,.5]],
    'H':[[0,0,0,1],[1,0,1,1],[0,.5,1,.5]],
    'I':[[.3,0,.7,0],[.5,0,.5,1],[.3,1,.7,1]],
    'J':[[.2,0,.8,0],[.6,0,.6,.8],[.6,.8,.3,.9],[.3,.9,.1,.7]],
    'K':[[0,0,0,1],[0,.5,1,0],[0,.5,1,1]],
    'L':[[0,0,0,1],[0,1,1,1]],
    'M':[[0,0,0,1],[0,0,.5,.6],[.5,.6,1,0],[1,0,1,1]],
    'N':[[0,0,0,1],[0,0,1,1],[1,0,1,1]],
    'O':[[0,.1,.2,0],[.2,0,.8,0],[.8,0,1,.1],[1,.1,1,.9],[1,.9,.8,1],[.8,1,.2,1],[.2,1,0,.9],[0,.9,0,.1]],
    'P':[[0,0,0,1],[0,0,.7,0],[.7,0,1,.2],[1,.2,1,.4],[1,.4,.7,.5],[.7,.5,0,.5]],
    'Q':[[0,.1,.2,0],[.2,0,.8,0],[.8,0,1,.1],[1,.1,1,.9],[1,.9,.8,1],[.8,1,.2,1],[.2,1,0,.9],[0,.9,0,.1],[.6,.7,1,1]],
    'R':[[0,0,0,1],[0,0,.7,0],[.7,0,1,.2],[1,.2,1,.4],[1,.4,.7,.5],[.7,.5,0,.5],[.4,.5,1,1]],
    'S':[[1,.1,.3,.1],[.3,.1,0,.3],[0,.3,0,.5],[0,.5,.7,.5],[.7,.5,1,.7],[1,.7,1,.9],[1,.9,.3,.9],[.3,.9,0,.8]],
    'T':[[0,0,1,0],[.5,0,.5,1]],
    'U':[[0,0,0,.8],[0,.8,.2,1],[.2,1,.8,1],[.8,1,1,.8],[1,.8,1,0]],
    'V':[[0,0,.5,1],[1,0,.5,1]],
    'W':[[0,0,.25,1],[.25,1,.5,.5],[.5,.5,.75,1],[.75,1,1,0]],
    'X':[[0,0,1,1],[1,0,0,1]],
    'Y':[[0,0,.5,.5],[1,0,.5,.5],[.5,.5,.5,1]],
    'Z':[[0,0,1,0],[1,0,0,1],[0,1,1,1]],
  }};
  const segsArr=segs[char]||segs['A'];
  const pts=[];
  segsArr.forEach(([x1,y1,x2,y2])=>{{
    const steps=Math.ceil(Math.sqrt((x2-x1)**2+(y2-y1)**2)*8);
    for(let i=0;i<=steps;i++){{const t=i/steps;pts.push({{x:ox+(x1+(x2-x1)*t)*sz,y:oy+(y1+(y2-y1)*t)*sz}});}}
  }});
  return pts;
}}
// Build name targets
function buildNameTargets(){{
  const chars='{name_upper}'.split('');
  const charW=Math.min(W*.09,50),padding=charW*.3;
  const totalW=chars.length*(charW+padding)-padding;
  const startX=(W-totalW)/2;
  const startY=H*.35;
  let pts=[];
  chars.forEach((c,i)=>{{pts=[...pts,...letterPts(c,startX+i*(charW+padding),startY,charW)]}});
  return pts;
}}
const NFF=Math.min(120,Math.max(60,'{name_upper}'.length*15));
let fireflies=[];
let nameTargets=[];
let htargets=[];
function init(){{
  nameTargets=buildNameTargets();
  const sc=Math.min(W*.022,H*.018);
  htargets=heartPts(NFF,W/2,H*.42,sc);
  fireflies=Array.from({{length:NFF}},(_,i)=>{{return{{
    x:Math.random()*W,y:Math.random()*H,
    vx:(Math.random()-.5)*.8,vy:(Math.random()-.5)*.8,
    tx:0,ty:0,phase_t:Math.random()*Math.PI*2,
    glow:.5+Math.random()*.5,size:1.5+Math.random()*1.5,
  }}}});
}}
function begin(){{document.getElementById('start').classList.add('gone');init();setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);}}
function drawBg(){{
  ctx.fillStyle='#03080a';ctx.fillRect(0,0,W,H);
  // Faint trees silhouette
  ctx.fillStyle='rgba(0,15,5,.8)';
  for(let i=0;i<8;i++){{const tx=W*(i/7),tw=20+Math.random()*15,th=H*.35+Math.random()*H*.15;ctx.fillRect(tx-tw/2,H-th,tw,th);}}
}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  drawBg();
  if(phase===1){{
    // Random drift for 1.5s then start spelling
    fireflies.forEach(f=>{{
      f.phase_t+=.04;f.x+=f.vx;f.y+=f.vy;
      f.vx+=(Math.random()-.5)*.08;f.vy+=(Math.random()-.5)*.08;
      f.vx*=.96;f.vy*=.96;
      if(f.x<0)f.x=W;if(f.x>W)f.x=0;if(f.y<0)f.y=H;if(f.y>H)f.y=0;
      const a=f.glow*(.5+.5*Math.sin(f.phase_t*3));
      const g=ctx.createRadialGradient(f.x,f.y,0,f.x,f.y,f.size*4);
      g.addColorStop(0,`rgba(180,255,100,${{a}})`);g.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=g;ctx.fillRect(f.x-f.size*4,f.y-f.size*4,f.size*8,f.size*8);
      ctx.beginPath();ctx.arc(f.x,f.y,f.size,0,Math.PI*2);ctx.fillStyle=`rgba(220,255,150,${{a}})`;ctx.fill();
    }});
    if(elapsed>1.5){{phase=2;elapsed=0;fireflies.forEach((f,i)=>{{const tgt=nameTargets[i%nameTargets.length];f.tx=tgt.x;f.ty=tgt.y;}});}}
  }}
  if(phase===2){{
    const prog=Math.min(1,elapsed/2);
    fireflies.forEach((f,i)=>{{
      f.phase_t+=.04;
      f.x+=(f.tx-f.x)*prog*.08;f.y+=(f.ty-f.y)*prog*.08;
      const a=f.glow*(.6+.4*Math.sin(f.phase_t*3));
      const g=ctx.createRadialGradient(f.x,f.y,0,f.x,f.y,f.size*5);
      g.addColorStop(0,`rgba(180,255,100,${{a}})`);g.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=g;ctx.fillRect(f.x-f.size*5,f.y-f.size*5,f.size*10,f.size*10);
      ctx.beginPath();ctx.arc(f.x,f.y,f.size,0,Math.PI*2);ctx.fillStyle=`rgba(220,255,150,${{a}})`;ctx.fill();
    }});
    if(prog>=1&&elapsed>2.5){{phase=3;elapsed=0;fireflies.forEach((f,i)=>{{f.tx=htargets[i%htargets.length].x;f.ty=htargets[i%htargets.length].y;}});}}
  }}
  if(phase===3){{
    const prog=Math.min(1,elapsed/2.2);
    fireflies.forEach(f=>{{
      f.phase_t+=.04;f.x+=(f.tx-f.x)*prog*.1;f.y+=(f.ty-f.y)*prog*.1;
      const a=f.glow*(.7+.3*Math.sin(f.phase_t*2));
      const g=ctx.createRadialGradient(f.x,f.y,0,f.x,f.y,f.size*5);
      g.addColorStop(0,`rgba(180,255,100,${{a}})`);g.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=g;ctx.fillRect(f.x-f.size*5,f.y-f.size*5,f.size*10,f.size*10);
      ctx.beginPath();ctx.arc(f.x,f.y,f.size,0,Math.PI*2);ctx.fillStyle=`rgba(220,255,150,${{a}})`;ctx.fill();
    }});
    if(prog>=1&&!cardDone){{cardDone=true;phase=4;setTimeout(showCard,500);}}
  }}
  if(phase===4){{
    fireflies.forEach(f=>{{
      f.phase_t+=.025;
      const a=f.glow*(.5+.5*Math.sin(f.phase_t*2));
      ctx.beginPath();ctx.arc(f.x,f.y,f.size,0,Math.PI*2);ctx.fillStyle=`rgba(200,255,120,${{a}})`;ctx.fill();
    }});
  }}
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;drawBg();requestAnimationFrame(idle);}}requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 5. NEON — Retro CRT terminal: SEARCHING... FOUND: → glitches to neon name
# ══════════════════════════════════════════════════════════════════════════════
def html_neon(name, date_str):
    msg = "You showed up in my life\nand now everything else\nis a lot less interesting."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#08000f}}
{start_css('#ff2d78','255,45,120')}
{card_css('rgba(12,0,20,.97)','#ffe0f0','#ff2d78','255,45,120')}
#terminal{{position:fixed;inset:0;z-index:10;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .6s ease;pointer-events:none}}
#terminal.show{{opacity:1}}
.crt{{width:min(480px,92vw);background:#000;border:2px solid rgba(0,255,80,.4);border-radius:8px;padding:28px 24px;font-family:'Courier New',monospace;font-size:clamp(.8rem,2.5vw,1rem);color:#00ff51;box-shadow:0 0 30px rgba(0,255,80,.2),inset 0 0 30px rgba(0,0,0,.5);position:relative;overflow:hidden}}
.crt::before{{content:'';position:absolute;inset:0;background:repeating-linear-height(transparent,transparent 2px,rgba(0,0,0,.08) 2px,rgba(0,0,0,.08) 4px);pointer-events:none}}
.crt-line{{margin-bottom:4px;opacity:0;animation:crtIn .1s ease forwards}}
@keyframes crtIn{{to{{opacity:1}}}}
.cursor{{display:inline-block;width:10px;height:1.1em;background:#00ff51;animation:blink .7s step-end infinite;vertical-align:text-bottom;margin-left:2px}}
@keyframes blink{{50%{{opacity:0}}}}
.found{{color:#ff2d78;text-shadow:0 0 10px rgba(255,45,120,.8)}}
#neon-reveal{{position:fixed;inset:0;z-index:20;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:24px;opacity:0;transition:opacity 1.2s ease;pointer-events:none}}
#neon-reveal.show{{opacity:1}}
.neon-name{{font-family:'Dancing Script',cursive;font-size:clamp(4rem,16vw,9rem);color:#ff2d78;text-shadow:0 0 20px #ff2d78,0 0 50px rgba(255,45,120,.6),0 0 100px rgba(255,45,120,.3);animation:neonFlicker 3s ease-in-out infinite}}
@keyframes neonFlicker{{0%,100%{{opacity:1}}92%{{opacity:1}}93%{{opacity:.6}}94%{{opacity:1}}97%{{opacity:.85}}98%{{opacity:1}}}}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#ff2d78','255,45,120')}
<div id="terminal"><div class="crt" id="crt"></div></div>
<div id="neon-reveal"><div class="neon-name">{name}</div></div>
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
function drawBg(){{ctx.fillStyle='#08000f';ctx.fillRect(0,0,W,H);const g=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*.5);g.addColorStop(0,'rgba(255,0,80,.04)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);}}
function loop(){{ctx.clearRect(0,0,W,H);drawBg();requestAnimationFrame(loop);}}loop();
const LINES=[
  '> BOOTING SYSTEM...',
  '> INITIALIZING SEARCH PROTOCOL',
  '> SCANNING DATABASE...',
  '> RESULTS: 7,900,000,000 people',
  '> APPLYING FILTERS...',
  '  [criteria: makes everything better]',
  '  [criteria: impossible not to think about]',
  '  [criteria: one of a kind]',
  '> SEARCHING...',
  '> NARROWING... ████████░░ 82%',
  '> NARROWING... █████████░ 94%',
  '> NARROWING... ██████████ 100%',
  '',
  '> MATCH FOUND: 1',
  `> NAME: <span class="found">{name.upper()}</span>`,
  '> CONFIDENCE: 100.00%',
  '> STATUS: Irreplaceable',
  '',
  '> OPENING TRANSMISSION...',
];
function begin(){{
  document.getElementById('start').classList.add('gone');
  const term=document.getElementById('terminal');
  const crt=document.getElementById('crt');
  setTimeout(()=>{{term.classList.add('show');}},1400);
  let delay=1600;
  LINES.forEach((line,i)=>{{
    setTimeout(()=>{{
      const div=document.createElement('div');div.className='crt-line';
      div.innerHTML=line+'<span class="cursor"></span>';
      crt.appendChild(div);
      // Remove cursor from previous line
      if(crt.children.length>1){{const prev=crt.children[crt.children.length-2];const cur=prev.querySelector('.cursor');if(cur)cur.remove();}}
      crt.scrollTop=crt.scrollHeight;
    }},delay);
    delay+=line.includes('SCANNING')||line.includes('NARROWING')||line.includes('RESULTS')?400:180;
  }});
  // Glitch transition to neon
  setTimeout(()=>{{
    let flicker=0;const fi=setInterval(()=>{{
      term.style.opacity=flicker%2===0?'0':'1';flicker++;
      if(flicker>8){{clearInterval(fi);term.style.opacity='0';document.getElementById('neon-reveal').classList.add('show');
        setTimeout(showCard,1000);}}
    }},80);
  }},delay+400);
}}
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 6. AURORA — Ribbons dance, pool, write glowing message in the sky
# ══════════════════════════════════════════════════════════════════════════════
def html_aurora(name, date_str):
    msg = "Some things are only visible\nif you look at exactly the right moment.\n\nGlad you looked."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#000c10}}
{start_css('#00ffcc','0,255,204')}
{card_css('rgba(0,12,16,.97)','#c0fff4','#00ffcc','0,200,160')}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#00ffcc','0,255,204')}
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
let phase=0,elapsed=0,prevT=0,cardDone=false;
const STARS=Array.from({{length:200}},()=>({{'x':Math.random(),'y':Math.random()*.6,'r':.2+Math.random()*1,'a':.1+Math.random()*.4,'tp':Math.random()*Math.PI*2,'ts':.005+Math.random()*.01}}));
// Aurora bands
const BANDS=[
  {{color:'rgba(0,255,180,',y:.18,amp:60,spd:.006,phase:0,width:120}},
  {{color:'rgba(100,100,255,',y:.26,amp:50,spd:.004,phase:1.2,width:90}},
  {{color:'rgba(0,200,255,',y:.32,amp:70,spd:.008,phase:2.4,width:100}},
  {{color:'rgba(150,0,255,',y:.22,amp:45,spd:.005,phase:.8,width:80}},
  {{color:'rgba(0,255,140,',y:.38,amp:55,spd:.007,phase:3.1,width:70}},
];
let t=0;
// Name text reveal phase
let nameAlpha=0;
function drawBg(){{
  ctx.fillStyle='#000c10';ctx.fillRect(0,0,W,H);
  STARS.forEach(s=>{{s.tp+=s.ts;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(180,255,240,${{Math.max(0,s.a+Math.sin(s.tp)*.15)}})`;ctx.fill()}});
}}
function drawAurora(intensity){{
  t+=.012;
  BANDS.forEach(b=>{{
    b.phase+=b.spd;
    for(let x=0;x<=W;x+=2){{
      const y1=(b.y*H)+Math.sin(x*.004+b.phase)*b.amp;
      const y2=y1+b.width*intensity;
      const grad=ctx.createLinearGradient(0,y1,0,y2);
      grad.addColorStop(0,b.color+'0)');
      grad.addColorStop(.3,b.color+(.12*intensity)+')');
      grad.addColorStop(.7,b.color+(.08*intensity)+')');
      grad.addColorStop(1,b.color+'0)');
      ctx.fillStyle=grad;ctx.fillRect(x,y1,2,y2-y1);
    }}
  }});
}}
function drawNameInAurora(alpha){{
  if(alpha<=0)return;
  ctx.save();
  ctx.globalAlpha=alpha;
  ctx.font=`bold clamp(2rem,10vw,5rem) 'Dancing Script',cursive`;
  ctx.textAlign='center';
  ctx.textBaseline='middle';
  const gradient=ctx.createLinearGradient(W/2-100,0,W/2+100,0);
  gradient.addColorStop(0,'#00ffcc');gradient.addColorStop(.5,'#7b2fff');gradient.addColorStop(1,'#00ffcc');
  ctx.fillStyle=gradient;
  ctx.shadowColor='#00ffcc';ctx.shadowBlur=30*alpha;
  ctx.fillText('{name}',W/2,H*.32);
  ctx.restore();
}}
function begin(){{document.getElementById('start').classList.add('gone');setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  drawBg();
  if(phase===1){{
    drawAurora(Math.min(1,elapsed/2));
    if(elapsed>3){{phase=2;elapsed=0;}}
  }}
  if(phase===2){{
    drawAurora(1);
    nameAlpha=Math.min(1,elapsed/.8);
    drawNameInAurora(nameAlpha);
    if(elapsed>1.5&&!cardDone){{cardDone=true;setTimeout(showCard,600);}}
  }}
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;drawBg();requestAnimationFrame(idle);}}requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 7. SUNRISE — Full sky transformation dark→dawn→gold, message lit by sunrise
# ══════════════════════════════════════════════════════════════════════════════
def html_sunrise(name, date_str):
    msg = "Every day you're in it\nstarts better than the last.\n\nThat's all this is about."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#05020a}}
{start_css('#ffb347','255,180,60')}
{card_css('rgba(255,250,240,.97)','#2a1000','#e65100','255,140,40')}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#ffb347','255,180,60')}
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
let phase=0,sunProgress=0,prevT=0,elapsed=0,cardDone=false;
// Sky color stops at different sun positions (0=night, 1=full sunrise)
function skyColor(t){{
  const night={{top:[5,2,10],bot:[10,5,20]}};
  const dawn={{top:[30,15,60],bot:[180,60,20]}};
  const gold={{top:[80,120,200],bot:[255,160,40]}};
  function lerp(a,b,t){{return Math.round(a+(b-a)*t);}}
  function lerpCol(a,b,t){{return[lerp(a[0],b[0],t),lerp(a[1],b[1],t),lerp(a[2],b[2],t)];}}
  const topC=t<.5?lerpCol(night.top,dawn.top,t*2):lerpCol(dawn.top,gold.top,(t-.5)*2);
  const botC=t<.5?lerpCol(night.bot,dawn.bot,t*2):lerpCol(dawn.bot,gold.bot,(t-.5)*2);
  return{{top:`rgb(${{topC.join(',')}})`,bot:`rgb(${{botC.join(',')}})`,botArr:botC}};
}}
const STARS=Array.from({{length:160}},()=>({{'x':Math.random(),'y':Math.random()*.7,'r':.3+Math.random(),'a':.6+Math.random()*.4,'tp':Math.random()*Math.PI*2}}));
function drawScene(t){{
  const c=skyColor(t);
  const bg=ctx.createLinearGradient(0,0,0,H);
  bg.addColorStop(0,c.top);bg.addColorStop(1,c.bot);
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
  // Stars fade as sun rises
  const starAlpha=Math.max(0,1-t*2.5);
  STARS.forEach(s=>{{s.tp+=.005;const a=starAlpha*(s.a+Math.sin(s.tp)*.15);if(a<=0)return;ctx.beginPath();ctx.arc(s.x*W,s.y*H*.8,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(255,240,220,${{a}})`;ctx.fill()}});
  // Sun
  const sunY=H*.85-t*H*.55;
  const sunR=Math.min(W,H)*.055;
  if(t>.05){{
    const sunGlow=ctx.createRadialGradient(W/2,sunY,0,W/2,sunY,sunR*8);
    sunGlow.addColorStop(0,`rgba(255,200,80,${{t*.3}})`);
    sunGlow.addColorStop(.4,`rgba(255,140,40,${{t*.15}})`);
    sunGlow.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=sunGlow;ctx.fillRect(0,0,W,H);
    ctx.beginPath();ctx.arc(W/2,sunY,sunR*t,0,Math.PI*2);
    const sg=ctx.createRadialGradient(W/2,sunY,0,W/2,sunY,sunR);
    sg.addColorStop(0,'#fff8c0');sg.addColorStop(.5,'#ffcc40');sg.addColorStop(1,'rgba(255,120,20,.8)');
    ctx.fillStyle=sg;ctx.fill();
  }}
  // Horizon glow
  const hg=ctx.createLinearGradient(0,H*.6,0,H);
  hg.addColorStop(0,'rgba(0,0,0,0)');
  hg.addColorStop(1,`rgba(${{c.botArr.join(',')}},0.4)`);
  ctx.fillStyle=hg;ctx.fillRect(0,H*.6,W,H*.4);
  // Ground silhouette
  ctx.fillStyle=`rgba(5,3,2,${{.9+t*.1}})`;
  ctx.fillRect(0,H*.85,W,H*.15);
  // Hills
  ctx.beginPath();ctx.moveTo(0,H*.85);
  for(let x=0;x<=W;x+=20)ctx.lineTo(x,H*.82+Math.sin(x*.008)*H*.04);
  ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();
  ctx.fillStyle=`rgba(3,2,1,${{.95}})`;ctx.fill();
}}
function begin(){{document.getElementById('start').classList.add('gone');setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  if(phase===1){{
    sunProgress=Math.min(1,elapsed/5);
    drawScene(sunProgress);
    if(sunProgress>.7&&!cardDone){{cardDone=true;setTimeout(showCard,400);}}
    if(sunProgress>=1)phase=2;
  }}
  if(phase===2)drawScene(1);
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;drawScene(0);requestAnimationFrame(idle);}}requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 8. RAIN — Foggy glass: rain streaks → finger draws heart → message in fog
# ══════════════════════════════════════════════════════════════════════════════
def html_rain(name, date_str):
    msg = "You're the kind of person\nI want to be around\nwhen it rains.\n\nAnd every other time."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#060810}}
{start_css('#7eb8e8','126,184,232')}
{card_css('rgba(8,10,20,.97)','#d0e4f8','#7eb8e8','100,160,220')}
</style></head><body>
<canvas id="bg"></canvas>
<canvas id="fg"></canvas>
{start_html(name,'#7eb8e8','126,184,232')}
{card_html(name, date_str)}
<script>
const bg=document.getElementById('bg'),bgx=bg.getContext('2d');
const fg=document.getElementById('fg'),fgx=fg.getContext('2d');
let W=bg.width=fg.width=window.innerWidth,H=bg.height=fg.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
let phase=0,elapsed=0,prevT=0,cardDone=false;
// Rain streaks
const DROPS=Array.from({{length:120}},()=>({{'x':Math.random()*W,'y':Math.random()*H,'len':20+Math.random()*60,'spd':8+Math.random()*10,'a':.1+Math.random()*.35}}));
function drawRain(){{
  bgx.fillStyle='rgba(6,8,16,.85)';bgx.fillRect(0,0,W,H);
  bgx.strokeStyle='rgba(140,180,220,.25)';bgx.lineWidth=1;
  DROPS.forEach(d=>{{
    bgx.beginPath();bgx.moveTo(d.x,d.y);bgx.lineTo(d.x-1,d.y+d.len);bgx.globalAlpha=d.a;bgx.stroke();
    d.y+=d.spd;if(d.y>H+80){{d.y=-80;d.x=Math.random()*W;}}
  }});
  bgx.globalAlpha=1;
  // Foggy glass overlay
  const fog=bgx.createLinearGradient(0,0,0,H);
  fog.addColorStop(0,'rgba(100,120,160,.15)');fog.addColorStop(1,'rgba(80,100,140,.08)');
  bgx.fillStyle=fog;bgx.fillRect(0,0,W,H);
}}
// Heart drawing on fog
let heartDrawn=[];let heartProgress=0;
function heartPts(n,cx,cy,sc){{const pts=[];for(let i=0;i<n;i++){{const t=(i/n)*Math.PI*2,x=16*Math.pow(Math.sin(t),3),y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));pts.push({{x:cx+x*sc,y:cy+y*sc}});}}return pts;}}
const HX=W/2,HY=H*.38,HS=Math.min(W*.028,H*.024);
const HPTS=heartPts(60,HX,HY,HS);
// Message in fog (drawn as text with foggy style)
let msgFogAlpha=0;
function drawFogHeart(prog){{
  fgx.clearRect(0,0,W,H);
  const drawn=Math.floor(HPTS.length*prog);
  if(drawn<2)return;
  // Clear the fog along the heart path (finger drawing effect)
  fgx.save();
  fgx.globalCompositeOperation='destination-out';
  fgx.strokeStyle='rgba(255,255,255,.6)';fgx.lineWidth=18;fgx.lineCap='round';fgx.lineJoin='round';
  fgx.beginPath();fgx.moveTo(HPTS[0].x,HPTS[0].y);
  for(let i=1;i<drawn;i++)fgx.lineTo(HPTS[i].x,HPTS[i].y);
  fgx.stroke();fgx.restore();
  // Draw the cleared path as a glowing wet trail
  fgx.save();fgx.strokeStyle='rgba(160,200,240,.5)';fgx.lineWidth=4;fgx.lineCap='round';fgx.lineJoin='round';
  fgx.beginPath();fgx.moveTo(HPTS[0].x,HPTS[0].y);
  for(let i=1;i<drawn;i++)fgx.lineTo(HPTS[i].x,HPTS[i].y);
  fgx.stroke();fgx.restore();
}}
function drawFogLayer(){{
  // Full fog overlay on fg canvas
  fgx.globalCompositeOperation='source-over';
  const fog=fgx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*.7);
  fog.addColorStop(0,'rgba(130,150,180,.55)');fog.addColorStop(1,'rgba(100,120,160,.3)');
  // Draw fog first, then the heart "clears" it via destination-out above
}}
function begin(){{
  document.getElementById('start').classList.add('gone');
  // Start fog layer on fg
  fgx.fillStyle='rgba(130,150,180,.5)';fgx.fillRect(0,0,W,H);
  setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);
}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  drawRain();
  if(phase===1){{
    heartProgress=Math.min(1,elapsed/2.5);
    drawFogHeart(heartProgress);
    if(heartProgress>=1&&!cardDone){{cardDone=true;setTimeout(showCard,700);}}
  }}
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;drawRain();fgx.clearRect(0,0,W,H);fgx.fillStyle='rgba(130,150,180,.5)';fgx.fillRect(0,0,W,H);requestAnimationFrame(idle);}}
requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=bg.width=fg.width=window.innerWidth;H=bg.height=fg.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 9. PARTICLE — EKG flatline → huge heartbeat → spike morphs into glowing heart
# ══════════════════════════════════════════════════════════════════════════════
def html_particle(name, date_str):
    msg = "Jenisha.\n\nThat's it.\nThat's the whole message."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#0f0005}}
{start_css('#ff1464','255,20,100')}
{card_css('rgba(18,0,5,.97)','#ffd0e0','#ff1464','255,20,100')}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#ff1464','255,20,100')}
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
let phase=0,elapsed=0,prevT=0,cardDone=false;
// EKG line
let ekg=[];const EKG_LEN=Math.floor(W*.8);const EKG_X=W*.1;const EKG_Y=H*.45;
let ekgT=0;let beatDone=false;let beatT=-1;
// Heart morph
let heartAlpha=0,heartScale=0,heartPulse=0;
function addEKGPoint(flat){{
  const v=flat?0:ekgBeat(ekgT);
  ekg.push(v);if(ekg.length>EKG_LEN)ekg.shift();ekgT+=.25;
}}
function ekgBeat(t){{
  // Realistic QRS complex
  const mod=t%80;
  if(mod<30)return 0;
  if(mod<33)return-(mod-30)*8;   // Q
  if(mod<36)return 24+(mod-33)*60; // R up
  if(mod<37)return 204-(mod-36)*180; // spike
  if(mod<39)return 24-(mod-37)*15; // S
  if(mod<42)return 0;
  if(mod<50)return Math.sin((mod-42)/8*Math.PI)*12; // T wave
  return 0;
}}
function drawEKG(alpha,color){{
  if(ekg.length<2||alpha<=0)return;
  ctx.save();ctx.globalAlpha=alpha;
  ctx.strokeStyle=color||'#ff1464';ctx.lineWidth=2;ctx.shadowColor='#ff1464';ctx.shadowBlur=6;
  ctx.beginPath();
  ekg.forEach((v,i)=>{{
    const x=EKG_X+i*(W*.8/EKG_LEN),y=EKG_Y-v;
    i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  }});
  ctx.stroke();ctx.shadowBlur=0;ctx.restore();
}}
function heartPts(n,cx,cy,sc){{const pts=[];for(let i=0;i<n;i++){{const t=(i/n)*Math.PI*2,x=16*Math.pow(Math.sin(t),3),y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));pts.push({{x:cx+x*sc,y:cy+y*sc}});}}return pts;}}
function drawHeart(alpha,scale,pulse){{
  if(alpha<=0)return;
  const cx=W/2,cy=H*.42,sc=Math.min(W*.024,H*.02)*scale*(1+Math.sin(pulse)*.04);
  ctx.save();ctx.globalAlpha=alpha;
  // Glow
  const g=ctx.createRadialGradient(cx,cy,0,cx,cy,sc*22);
  g.addColorStop(0,'rgba(255,20,100,.25)');g.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  // Heart stroke
  const pts=heartPts(80,cx,cy,sc);
  ctx.beginPath();pts.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));ctx.closePath();
  ctx.strokeStyle='#ff1464';ctx.lineWidth=3;ctx.shadowColor='#ff1464';ctx.shadowBlur=20;ctx.stroke();
  ctx.shadowBlur=0;ctx.restore();
}}
function begin(){{document.getElementById('start').classList.add('gone');setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  ctx.fillStyle='rgba(15,0,5,.92)';ctx.fillRect(0,0,W,H);
  if(phase===1){{
    // Flatline for 1.2s then single massive beat
    if(elapsed<1.2){{addEKGPoint(true);drawEKG(1);}}
    else if(!beatDone){{
      // Big beat
      const bp=Math.min(1,(elapsed-1.2)/.6);
      ekg=[];for(let i=0;i<EKG_LEN;i++){{const rel=i/EKG_LEN;const v=rel>.3&&rel<.7?Math.sin((rel-.3)/.4*Math.PI)*160*Math.sin(bp*Math.PI):0;ekg.push(v);}}
      drawEKG(1);
      if(bp>=1){{beatDone=true;elapsed=1.2;}}
    }}
    else{{
      // Fade EKG, grow heart
      const fp=Math.min(1,(elapsed-1.2)/1);
      drawEKG(1-fp);
      heartAlpha=fp;heartScale=fp;heartPulse+=.04;
      drawHeart(heartAlpha,heartScale,heartPulse);
      if(fp>=1&&!cardDone){{cardDone=true;phase=2;setTimeout(showCard,500);}}
    }}
  }}
  if(phase===2){{heartPulse+=.04;drawHeart(1,1,heartPulse);}}
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;ctx.fillStyle='#0f0005';ctx.fillRect(0,0,W,H);addEKGPoint(true);drawEKG(.3);requestAnimationFrame(idle);}}
requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 10. MATRIX — Code rain, chars slow + lock into her name, matrix clears
# ══════════════════════════════════════════════════════════════════════════════
def html_matrix(name, date_str):
    msg = "If I could write you a program\nit would just be an infinite loop\nthat prints your name."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#000800}}
{start_css('#00ff41','0,220,50')}
{card_css('rgba(0,8,0,.97)','#b0ffb8','#00ff41','0,200,40')}
#nname{{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);font-family:'Dancing Script',cursive;font-size:clamp(3.5rem,14vw,8rem);color:#00ff41;text-shadow:0 0 20px #00ff41,0 0 60px rgba(0,255,65,.4);opacity:0;z-index:20;transition:opacity 1s ease;white-space:nowrap}}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#00ff41','0,220,50')}
<div id="nname">{name}</div>
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
const CHARS='ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789';
const FS=16;const COLS=Math.floor(W/FS);
const drops=Array.from({{length:COLS}},()=>Math.floor(Math.random()*H/FS));
const dropSpeeds=Array.from({{length:COLS}},()=>.3+Math.random()*.7);
let phase=0,elapsed=0,prevT=0,cardDone=false,rainAlpha=1;
function drawMatrix(){{
  ctx.fillStyle=`rgba(0,8,0,${{0.05+(.95*(1-rainAlpha))}})`;ctx.fillRect(0,0,W,H);
  ctx.fillStyle=`rgba(0,255,65,${{rainAlpha}})`;ctx.font=FS+'px monospace';
  drops.forEach((y,i)=>{{
    const char=CHARS[Math.floor(Math.random()*CHARS.length)];
    ctx.fillStyle=y*FS<20?`rgba(180,255,180,${{rainAlpha}})`:`rgba(0,200,40,${{rainAlpha*.7}})`;
    ctx.fillText(char,i*FS,y*FS);
    drops[i]+=dropSpeeds[i];
    if(drops[i]*FS>H&&Math.random()>.975)drops[i]=0;
  }});
}}
function begin(){{
  document.getElementById('start').classList.add('gone');
  setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);
}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  if(phase===1){{drawMatrix();if(elapsed>2.5){{phase=2;elapsed=0;}}}}
  if(phase===2){{
    // Fade out matrix, show name
    rainAlpha=Math.max(0,1-elapsed/1.2);
    drawMatrix();
    if(elapsed>.4)document.getElementById('nname').style.opacity=Math.min(1,(elapsed-.4)/.8);
    if(elapsed>1.5&&!cardDone){{cardDone=true;setTimeout(showCard,600);}}
  }}
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;drawMatrix();requestAnimationFrame(idle);}}requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 11. BUTTERFLY — Chrysalis shakes, butterfly emerges, wings open, form heart
# ══════════════════════════════════════════════════════════════════════════════
def html_butterfly(name, date_str):
    msg = "Opening this probably surprised you.\nGood.\nYou deserve nice surprises."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#080818}}
{start_css('#f9a8d4','249,168,212')}
{card_css('rgba(8,8,24,.97)','#f0d8ff','#c084fc','220,150,255')}
#scene{{position:fixed;inset:0;z-index:10;display:flex;align-items:center;justify-content:center;pointer-events:none}}
.cocoon{{font-size:clamp(4rem,12vw,7rem);transition:transform .2s ease;display:inline-block}}
.cocoon.shake{{animation:shake .5s ease-in-out 3}}
@keyframes shake{{0%,100%{{transform:rotate(-5deg)}}50%{{transform:rotate(5deg)}}}}
.butterfly{{font-size:clamp(5rem,15vw,9rem);display:none;animation:spread 1s ease forwards}}
@keyframes spread{{from{{transform:scaleX(.1)}}to{{transform:scaleX(1)}}}}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#f9a8d4','249,168,212')}
<div id="scene"><span class="cocoon" id="cocoon">🫘</span></div>
{card_html(name, date_str)}
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;{TYPEWRITER_JS}
const STARS=Array.from({{length:200}},()=>({{'x':Math.random(),'y':Math.random(),'r':.3+Math.random()*1.3,'a':.1+Math.random()*.5,'tp':Math.random()*Math.PI*2,'ts':.006+Math.random()*.012}}));
let phase=0,elapsed=0,prevT=0,cardDone=false;
// Particle butterflies
let particles=[];
function spawnParticles(){{
  const cols=['#f9a8d4','#e879f9','#c084fc','#fbbf24','#a78bfa'];
  for(let i=0;i<40;i++){{
    particles.push({{
      x:W/2,y:H/2,vx:(Math.random()-.5)*6,vy:(Math.random()-.8)*6,
      a:1,decay:.008+Math.random()*.008,em:'🦋',sz:16+Math.random()*20,rot:Math.random()*Math.PI*2
    }});
  }}
}}
function drawBg(){{
  const bg=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*.8);
  bg.addColorStop(0,'#12081e');bg.addColorStop(1,'#060410');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
  STARS.forEach(s=>{{s.tp+=s.ts;const a=s.a+Math.sin(s.tp)*.2;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(220,180,255,${{Math.max(0,a)}})`;ctx.fill()}});
}}
function drawParticles(){{
  particles.forEach((p,i)=>{{
    p.x+=p.vx;p.y+=p.vy;p.vy+=.08;p.a-=p.decay;
    if(p.a<=0)return;
    ctx.save();ctx.globalAlpha=p.a;ctx.font=p.sz+'px serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.translate(p.x,p.y);ctx.rotate(p.rot+=.05);ctx.fillText(p.em,0,0);ctx.restore();
  }});
  particles=particles.filter(p=>p.a>0);
}}
function begin(){{
  document.getElementById('start').classList.add('gone');
  const cocoon=document.getElementById('cocoon');
  // Shake 3 times
  setTimeout(()=>cocoon.classList.add('shake'),1400);
  // More shaking
  setTimeout(()=>{{cocoon.classList.remove('shake');void cocoon.offsetWidth;cocoon.classList.add('shake');}},2300);
  // Emerge
  setTimeout(()=>{{
    cocoon.style.fontSize='clamp(5rem,15vw,9rem)';
    let frames=0;const shake=setInterval(()=>{{cocoon.style.transform=`rotate(${{frames%2?5:-5}}deg)`;frames++;if(frames>10){{clearInterval(shake);cocoon.style.transform='';cocoon.textContent='🦋';cocoon.style.display='inline-block';cocoon.style.animation='spread 1s ease forwards';spawnParticles();phase=1;prevT=performance.now();requestAnimationFrame(loop);}}}},60);
  }},3200);
}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  drawBg();drawParticles();
  if(phase===1&&elapsed>1.2&&!cardDone){{cardDone=true;setTimeout(showCard,400);}}
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;drawBg();requestAnimationFrame(idle);}}requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 12. CAMPFIRE — Match strikes, candle lights, warm glow reveals handwritten note
# ══════════════════════════════════════════════════════════════════════════════
def html_campfire(name, date_str):
    msg = "If I could pick one place to be right now\nit would be wherever you are.\n\nThat's all."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#050100}}
{start_css('#ff8c42','255,140,66')}
#scene{{position:fixed;inset:0;z-index:10;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8vh;pointer-events:none}}
.candle-wrap{{text-align:center;opacity:0;transform:translateY(30px);transition:opacity .8s ease,transform .8s ease}}
.candle-wrap.show{{opacity:1;transform:translateY(0)}}
.candle{{font-size:clamp(3rem,10vw,5rem)}}
.note{{background:rgba(255,252,240,.95);border-radius:10px;padding:20px 22px;width:min(300px,80vw);margin:0 auto 16px;box-shadow:0 8px 40px rgba(0,0,0,.3);opacity:0;transition:opacity 1.2s ease;text-align:left}}
.note.show{{opacity:1}}
.note-to{{font-family:'Caveat',cursive;font-size:.9rem;color:rgba(100,50,20,.6);margin-bottom:8px}}
.note-msg{{font-family:'Caveat',cursive;font-size:clamp(1.1rem,3.5vw,1.3rem);line-height:1.7;color:#2a1000;white-space:pre-wrap;min-height:3em}}
.note-from{{font-family:'Dancing Script',cursive;font-size:1.3rem;color:#c45000;text-align:right;margin-top:10px}}
.note-date{{font-size:.65rem;color:rgba(0,0,0,.3);text-align:right}}
</style></head><body>
<canvas id="c"></canvas>
{start_html(name,'#ff8c42','255,140,66')}
<div id="scene">
  <div class="candle-wrap" id="cwrap">
    <div class="note" id="note">
      <div class="note-to">hey {name.lower()},</div>
      <div class="note-msg" id="nmsg"></div>
      <div class="note-from">— Dipesh</div>
      <div class="note-date">{date_str}</div>
    </div>
    <div class="candle">🕯️</div>
  </div>
</div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;
function typeMsg(el,text,spd){{el.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=text.length){{clearInterval(iv);return;}}el.textContent+=text[i++];}},spd);}}
let flameProgress=0,phase=0,prevT=0,elapsed=0;
// Match strike particles
let sparks=[];
function spark(x,y){{for(let i=0;i<20;i++)sparks.push({{x,y,vx:(Math.random()-.5)*6,vy:-(Math.random()*6+2),a:1,r:1+Math.random()*2}});}}
function drawBg(warmth){{
  const bg=ctx.createRadialGradient(W/2,H*.7,0,W/2,H*.7,Math.max(W,H)*warmth*.7);
  bg.addColorStop(0,`rgba(80,30,5,${{warmth*.6}})`);bg.addColorStop(.5,`rgba(30,10,2,${{warmth*.3}})`);bg.addColorStop(1,'rgba(5,1,0,1)');
  ctx.fillStyle='#050100';ctx.fillRect(0,0,W,H);
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
  // Warm candlelight flicker on ceiling/walls
  if(warmth>.1){{
    const fl=ctx.createRadialGradient(W/2,H*.6,0,W/2,H*.6,Math.min(W,H)*.4*warmth);
    fl.addColorStop(0,`rgba(255,160,60,${{warmth*.12}})`);fl.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=fl;ctx.fillRect(0,0,W,H);
  }}
}}
function drawSparks(){{
  sparks.forEach(s=>{{s.x+=s.vx;s.y+=s.vy;s.vy+=.15;s.a-=.03;if(s.a<=0)return;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(255,200,80,${{s.a}})`;ctx.fill()}});
  sparks=sparks.filter(s=>s.a>0);
}}
// Match strike animation
let matchX=W*.3,matchY=H*.4;
let matchDone=false;
function begin(){{
  document.getElementById('start').classList.add('gone');
  // Match strike at 1.4s
  setTimeout(()=>{{
    phase=1;prevT=performance.now();requestAnimationFrame(loop);
    spark(W*.55,H*.5);
    setTimeout(()=>spark(W*.55,H*.5),100);
    setTimeout(()=>{{matchDone=true;phase=2;elapsed=0;}},800);
  }},1400);
}}
function loop(ts){{
  if(!prevT)prevT=ts;const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  if(phase===1){{drawBg(0);drawSparks();}}
  if(phase===2){{
    flameProgress=Math.min(1,elapsed/2.5);
    drawBg(flameProgress);drawSparks();
    if(elapsed>.8&&!document.getElementById('cwrap').classList.contains('show')){{
      document.getElementById('cwrap').classList.add('show');
    }}
    if(elapsed>1.8&&!document.getElementById('note').classList.contains('show')){{
      document.getElementById('note').classList.add('show');
      setTimeout(()=>typeMsg(document.getElementById('nmsg'),MSG,44),800);
    }}
  }}
  requestAnimationFrame(loop);
}}
function idle(){{if(phase>0)return;drawBg(0);requestAnimationFrame(idle);}}requestAnimationFrame(idle);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script></body></html>"""



# ══════════════════════════════════════════════════════════════════════════════
# 13. HEARTCATCH — Game: catch falling hearts with a basket
# ══════════════════════════════════════════════════════════════════════════════
def html_heartcatch(name, date_str):
    msg = "This started as a game\nbut I kept coming back anyway.\n\nThat should tell you something."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;overflow:hidden;background:#0d0015;font-family:'Caveat',cursive}}
#ui{{position:fixed;top:18px;left:50%;transform:translateX(-50%);display:flex;gap:24px;align-items:center;z-index:10}}
#score{{color:#ff70b0;font-size:1.5rem}}#lives{{font-size:1.5rem}}
#hint{{position:fixed;bottom:28px;left:50%;transform:translateX(-50%);font-size:1rem;color:rgba(255,180,220,.45);letter-spacing:.1em;animation:bl 2s infinite}}
@keyframes bl{{0%,100%{{opacity:.35}}50%{{opacity:.85}}}}
#mo{{position:fixed;inset:0;background:rgba(13,0,21,.93);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:20;opacity:0;pointer-events:none;transition:opacity 1.2s;padding:20px;text-align:center}}
#mo.show{{opacity:1;pointer-events:all}}
.mt{{font-family:'Dancing Script',cursive;font-size:clamp(2.2rem,9vw,3.5rem);color:#ff70b0;margin-bottom:20px}}
.mm{{font-family:'Caveat',cursive;font-size:clamp(1.1rem,3.5vw,1.5rem);color:#ffe0f0;line-height:1.85;white-space:pre-wrap}}
.mf{{font-family:'Dancing Script',cursive;font-size:1.8rem;color:#ff70b0;margin-top:18px}}
.md{{font-size:.7rem;color:rgba(255,180,220,.3);margin-top:3px;letter-spacing:.08em}}</style></head><body>
<canvas id="c"></canvas>
<div id="ui"><span id="score">♥ 0 / 15</span><span id="lives">❤️❤️❤️</span></div>
<div id="hint">move to catch the hearts</div>
<div id="mo"><div class="mt">{name}</div><div class="mm" id="mm"></div><div class="mf">— Dipesh</div><div class="md">{date_str}</div></div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const MSG=`{msg}`;
let caught=0,lives=3,over=false,bx=W/2,tx=W/2,spawnT=0,lastT=0;
const HEARTS=[],SPARKS=[];
const BGS=Array.from({{length:180}},()=>({{'x':Math.random()*W,'y':Math.random()*H,'r':.3+Math.random(),'a':.1+Math.random()*.5,'tp':Math.random()*Math.PI*2}}));
class Heart{{constructor(){{this.x=70+Math.random()*(W-140);this.y=-30;this.vy=1.3+Math.random()*2;this.vx=(Math.random()-.5)*.5;this.sz=15+Math.random()*12;this.rot=0;this.rs=(Math.random()-.5)*.03;this.col=`hsl(${{330+Math.random()*40}},90%,${{65+Math.random()*15}}%)`;this.alive=true;}}tick(){{this.x+=this.vx;this.y+=this.vy;this.rot+=this.rs;if(this.y>H+40&&this.alive){{this.alive=false;if(!over){{lives=Math.max(0,lives-1);document.getElementById('lives').textContent=['❤️','❤️','❤️'].map((_,i)=>i<lives?'❤️':'🤍').join('');if(lives<=0)setTimeout(win,600);}}}}}}
draw(){{if(!this.alive)return;ctx.save();ctx.translate(this.x,this.y);ctx.rotate(this.rot);const s=this.sz/16;ctx.scale(s,s);ctx.beginPath();ctx.moveTo(0,-4);ctx.bezierCurveTo(0,-11,12,-11,12,-4);ctx.bezierCurveTo(12,3,0,12,0,16);ctx.bezierCurveTo(0,12,-12,3,-12,-4);ctx.bezierCurveTo(-12,-11,0,-11,0,-4);ctx.fillStyle=this.col;ctx.shadowColor=this.col;ctx.shadowBlur=10;ctx.fill();ctx.restore();}}}}
class Spark{{constructor(x,y,c){{this.x=x;this.y=y;this.vx=(Math.random()-.5)*9;this.vy=-3-Math.random()*5;this.a=1;this.r=2+Math.random()*3;this.col=c;}}tick(){{this.x+=this.vx;this.y+=this.vy;this.vy+=.28;this.a-=.033;}}draw(){{if(this.a<=0)return;ctx.globalAlpha=Math.max(0,this.a);ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);ctx.fillStyle=this.col;ctx.fill();ctx.globalAlpha=1;}}}}
function win(){{over=true;document.getElementById('hint').style.opacity='0';const el=document.getElementById('mo');el.classList.add('show');const m=document.getElementById('mm');m.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}m.textContent+=MSG[i++];}},42);}}
function updUI(){{document.getElementById('score').textContent=`♥ ${{caught}} / 15`;}}
function loop(ts){{const dt=Math.min(.08,(ts-lastT)/1000);lastT=ts;
ctx.fillStyle='#0d0015';ctx.fillRect(0,0,W,H);
BGS.forEach(s=>{{s.tp+=.005;const a=s.a+Math.sin(s.tp)*.15;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(200,140,255,${{Math.max(0,a)}})`;ctx.fill();}});
if(!over){{spawnT+=dt;const diff=1+caught*.07;if(spawnT>1.3/diff){{spawnT=0;HEARTS.push(new Heart());}}}}
bx+=(tx-bx)*.13;
const bw=Math.min(W*.22,108),bh=16,by=H-58;
ctx.beginPath();ctx.moveTo(bx-bw/2,by);ctx.lineTo(bx+bw/2,by);ctx.lineTo(bx+bw*.38,by+bh);ctx.lineTo(bx-bw*.38,by+bh);ctx.closePath();
ctx.strokeStyle='#ff70b0';ctx.lineWidth=3;ctx.shadowColor='#ff70b0';ctx.shadowBlur=14;ctx.stroke();ctx.shadowBlur=0;
HEARTS.forEach(h=>{{if(!h.alive)return;h.tick();if(!over&&h.alive&&h.y+h.sz>by&&h.y<by+bh+4&&h.x>bx-bw/2&&h.x<bx+bw/2){{h.alive=false;caught++;for(let i=0;i<10;i++)SPARKS.push(new Spark(h.x,h.y,h.col));updUI();if(caught>=15)win();}}h.draw();}});
SPARKS.forEach(s=>{{s.tick();s.draw();}});requestAnimationFrame(loop);}}
window.addEventListener('mousemove',e=>tx=e.clientX);
window.addEventListener('touchmove',e=>{{e.preventDefault();tx=e.touches[0].clientX;}},{{passive:false}});
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
requestAnimationFrame(loop);
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 14. MEMORY — Card flip matching game
# ══════════════════════════════════════════════════════════════════════════════
def html_memory(name, date_str):
    msg = "I've been thinking about you\nmore than I should probably admit.\n\nPretty sure you already knew that."
    colors = json.dumps(["#ff6b6b","#ff9f43","#ffd32a","#0be881","#00d2d3","#54a0ff","#c56cf0","#ff9ff3"])
    emojis = json.dumps(["💗","🧡","💛","💚","💙","💜","🌸","✨"])
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;min-height:100%;background:#080810;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Caveat',cursive;padding:24px 12px;overflow-x:hidden}}
h1{{font-family:'Dancing Script',cursive;color:#a78bfa;font-size:clamp(1.6rem,6vw,2.4rem);margin-bottom:4px;text-align:center}}
#sub{{color:rgba(167,139,250,.4);font-size:.95rem;letter-spacing:.14em;margin-bottom:22px}}
#grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(6px,2vw,10px);width:min(420px,95vw)}}
.card{{aspect-ratio:1;position:relative;cursor:pointer;transform-style:preserve-3d;transition:transform .5s}}
.card.flipped,.card.matched{{transform:rotateY(180deg)}}
.card.matched{{cursor:default}}
.face{{position:absolute;inset:0;border-radius:12px;display:flex;align-items:center;justify-content:center;backface-visibility:hidden;-webkit-backface-visibility:hidden}}
.front{{background:#1a1a30;border:2px solid rgba(167,139,250,.18);font-size:1.4rem;color:rgba(167,139,250,.3)}}
.back{{transform:rotateY(180deg);font-size:clamp(1.4rem,5vw,2rem)}}
#moves{{color:rgba(200,180,255,.4);font-size:.95rem;margin-top:14px;letter-spacing:.1em}}
#wo{{position:fixed;inset:0;background:rgba(8,8,16,.96);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:20;opacity:0;pointer-events:none;transition:opacity 1.2s;padding:20px;text-align:center}}
#wo.show{{opacity:1;pointer-events:all}}
.wt{{font-family:'Dancing Script',cursive;font-size:clamp(2rem,9vw,3rem);color:#a78bfa;margin-bottom:18px}}
.wm{{font-family:'Caveat',cursive;font-size:clamp(1.1rem,3.5vw,1.45rem);color:#e0d0ff;line-height:1.85;white-space:pre-wrap}}
.wf{{font-family:'Dancing Script',cursive;font-size:1.7rem;color:#a78bfa;margin-top:18px}}
.wd{{font-size:.7rem;color:rgba(167,139,250,.3);margin-top:3px;letter-spacing:.08em}}</style></head><body>
<h1>find the pairs</h1><div id="sub">for {name.lower()}</div>
<div id="grid"></div><div id="moves">0 moves</div>
<div id="wo"><div class="wt">{name}</div><div class="wm" id="wm"></div><div class="wf">— Dipesh</div><div class="wd">{date_str}</div></div>
<script>
const C={colors};const E={emojis};const MSG=`{msg}`;
let flipped=[],matched=0,moves=0,locked=false;
const vals=[...Array(8).keys(),...Array(8).keys()].sort(()=>Math.random()-.5);
const grid=document.getElementById('grid');
vals.forEach(v=>{{const d=document.createElement('div');d.className='card';d.dataset.v=v;
d.innerHTML=`<div class="face front">?</div><div class="face back" style="background:${{C[v]}}">${{E[v]}}</div>`;
d.addEventListener('click',()=>flip(d));grid.appendChild(d);}});
function flip(c){{if(locked||c.classList.contains('flipped')||c.classList.contains('matched'))return;
c.classList.add('flipped');flipped.push(c);
if(flipped.length===2){{moves++;document.getElementById('moves').textContent=`${{moves}} move${{moves!==1?'s':''}}`;locked=true;
if(flipped[0].dataset.v===flipped[1].dataset.v){{flipped[0].classList.add('matched');flipped[1].classList.add('matched');flipped=[];locked=false;matched++;if(matched===8)setTimeout(win,700);}}
else{{setTimeout(()=>{{flipped.forEach(c=>c.classList.remove('flipped'));flipped=[];locked=false;}},1100);}};}}}}
function win(){{const el=document.getElementById('wo');el.classList.add('show');const m=document.getElementById('wm');m.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}m.textContent+=MSG[i++];}},44);}}
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 15. REASONS — Interactive animated checklist: 13 things
# ══════════════════════════════════════════════════════════════════════════════
def html_reasons(name, date_str):
    msg = "Stopped counting after thirteen.\nNot because I ran out.\n\nJust felt like a good place to stop."
    items = json.dumps([
        "the way you exist","you make ordinary things interesting",
        "you are better at things than you think","you're actually really funny",
        "you don't need this page but I made it anyway",
        "the way you laugh when something catches you off guard",
        "you remind me that things can be good",
        "you are annoyingly easy to think about",
        "you show up fully, even when you don't have to",
        "you are exactly the right amount of everything",
        "talking to you doesn't feel like work",
        "you didn't have to be this interesting",
        "I just like you. that's it.",
    ])
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;min-height:100%;background:#05000e;font-family:'Caveat',cursive;padding-bottom:50px;overflow-x:hidden}}
.hdr{{text-align:center;padding:44px 20px 8px}}.ht{{font-family:'Dancing Script',cursive;font-size:clamp(2rem,8vw,3rem);color:#c084fc;text-shadow:0 0 50px rgba(192,132,252,.25)}}
.hs{{font-size:.95rem;color:rgba(192,132,252,.38);letter-spacing:.16em;margin-top:6px}}
#list{{max-width:500px;margin:28px auto;padding:0 18px;display:flex;flex-direction:column;gap:14px}}
.item{{background:rgba(192,132,252,.05);border:1px solid rgba(192,132,252,.1);border-radius:14px;padding:16px 20px;display:flex;gap:14px;align-items:center;opacity:0;transform:translateX(-24px);transition:opacity .6s,transform .6s,background .3s,border-color .3s;cursor:pointer}}
.item.vis{{opacity:1;transform:translateX(0)}}.item.done{{background:rgba(192,132,252,.12);border-color:rgba(192,132,252,.3)}}
.num{{width:30px;height:30px;border-radius:50%;background:rgba(192,132,252,.12);border:1.5px solid rgba(192,132,252,.28);display:flex;align-items:center;justify-content:center;font-size:.88rem;color:#c084fc;flex-shrink:0;transition:background .3s,color .3s}}
.item.done .num{{background:#c084fc;color:#0d0018;border-color:#c084fc}}
.txt{{font-size:clamp(.95rem,3vw,1.15rem);color:#e9d5ff;line-height:1.5}}
#fin{{text-align:center;max-width:460px;margin:0 auto;padding:16px 18px 0;opacity:0;transition:opacity 1.2s}}
#fin.show{{opacity:1}}
.fmsg{{font-size:clamp(1rem,3.2vw,1.35rem);color:#e9d5ff;line-height:1.88;white-space:pre-wrap}}
.ffrom{{font-family:'Dancing Script',cursive;font-size:1.7rem;color:#c084fc;margin-top:16px}}
.fdate{{font-size:.7rem;color:rgba(192,132,252,.28);margin-top:3px;letter-spacing:.08em}}</style></head><body>
<div class="hdr"><div class="ht">13 things.</div><div class="hs">for {name.lower()} — tap each one</div></div>
<div id="list"></div>
<div id="fin"><div class="fmsg" id="fmsg"></div><div class="ffrom">— Dipesh</div><div class="fdate">{date_str}</div></div>
<script>
const ITEMS={items};const MSG=`{msg}`;let done=0;
const list=document.getElementById('list');
ITEMS.forEach((txt,i)=>{{const d=document.createElement('div');d.className='item';
d.innerHTML=`<div class="num">${{i+1}}</div><div class="txt">${{txt}}</div>`;
d.addEventListener('click',()=>{{if(!d.classList.contains('done')){{d.classList.add('done');done++;if(done===ITEMS.length)setTimeout(showFin,700);}}}});
list.appendChild(d);setTimeout(()=>d.classList.add('vis'),180+i*130);}});
function showFin(){{const el=document.getElementById('fin');el.classList.add('show');const m=document.getElementById('fmsg');m.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}m.textContent+=MSG[i++];}},46);el.scrollIntoView({{behavior:'smooth',block:'center'}});}}
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 16. QUIZ — Personality quiz (rigged — she's perfect every time)
# ══════════════════════════════════════════════════════════════════════════════
def html_quiz(name, date_str):
    msg = "I already knew the answer\nbefore I made this.\n\nJust wanted you to see it too."
    qs = json.dumps([
        {"q":"What's your default setting?","opts":["overthinking things","figuring it out anyway","pretending not to care"]},
        {"q":"Someone needs help. You:","opts":["show up before they finish asking","quietly handle it","check in later"]},
        {"q":"Your idea of a good time?","opts":["somewhere low-key and real","anything, if the company's right","being completely unbothered"]},
        {"q":"How do people remember you?","opts":["exactly as you are","better than you give yourself credit for","as someone who showed up"]},
    ])
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;min-height:100%;background:#030c1a;display:flex;align-items:center;justify-content:center;font-family:'Caveat',cursive;padding:24px}}
#app{{width:min(480px,100%);text-align:center}}
.logo{{font-family:'Dancing Script',cursive;font-size:clamp(1.8rem,7vw,2.5rem);color:#38bdf8;margin-bottom:4px}}
.sub{{font-size:.95rem;color:rgba(56,189,248,.38);letter-spacing:.14em;margin-bottom:28px}}
#prog{{height:4px;background:rgba(56,189,248,.12);border-radius:2px;margin-bottom:28px;overflow:hidden}}
#pbar{{height:100%;background:#38bdf8;width:0;transition:width .5s;border-radius:2px}}
#qt{{font-size:clamp(1.15rem,4vw,1.55rem);color:#e0f2fe;line-height:1.6;margin-bottom:24px;min-height:56px}}
#opts{{display:flex;flex-direction:column;gap:11px}}
.opt{{background:rgba(56,189,248,.06);border:1.5px solid rgba(56,189,248,.18);border-radius:14px;padding:15px 18px;font-family:'Caveat',cursive;font-size:clamp(1rem,3.2vw,1.2rem);color:#bae6fd;text-align:left;cursor:pointer;transition:all .2s;width:100%}}
.opt:hover{{background:rgba(56,189,248,.13);border-color:rgba(56,189,248,.45)}}
.opt.sel{{background:rgba(56,189,248,.22);border-color:#38bdf8;color:#fff}}
#result{{display:none}}
.rt{{font-family:'Dancing Script',cursive;font-size:clamp(2rem,8vw,2.8rem);color:#38bdf8;margin-bottom:6px}}
.rd{{font-size:clamp(1rem,3.2vw,1.3rem);color:#bae6fd;margin-bottom:26px;line-height:1.6}}
.div{{height:1px;background:rgba(56,189,248,.12);margin:22px 0}}
.rmsg{{font-size:clamp(1.05rem,3.4vw,1.4rem);color:#e0f2fe;line-height:1.88;white-space:pre-wrap}}
.rfrom{{font-family:'Dancing Script',cursive;font-size:1.7rem;color:#38bdf8;margin-top:16px}}
.rdate{{font-size:.7rem;color:rgba(56,189,248,.28);margin-top:3px;letter-spacing:.08em}}</style></head><body>
<div id="app">
  <div class="logo">find out</div><div class="sub">for {name.lower()}</div>
  <div id="prog"><div id="pbar"></div></div>
  <div id="qt"></div><div id="opts"></div>
  <div id="result"><div class="rt">you are</div><div class="rd">exactly who I wanted to find.</div><div class="div"></div><div class="rmsg" id="rmsg"></div><div class="rfrom">— Dipesh</div><div class="rdate">{date_str}</div></div>
</div><script>
const QS={qs};const MSG=`{msg}`;let qi=0,locked=false;
function render(){{document.getElementById('pbar').style.width=(qi/QS.length*100)+'%';if(qi>=QS.length){{showResult();return;}}locked=false;const q=QS[qi];document.getElementById('qt').textContent=q.q;const opts=document.getElementById('opts');opts.innerHTML='';q.opts.forEach((o,i)=>{{const b=document.createElement('button');b.className='opt';b.textContent=o;b.addEventListener('click',()=>{{if(locked)return;locked=true;b.classList.add('sel');setTimeout(()=>{{qi++;render();}},750);}});opts.appendChild(b);}});}}
function showResult(){{document.getElementById('prog').style.display='none';document.getElementById('qt').style.display='none';document.getElementById('opts').style.display='none';document.querySelector('.sub').style.display='none';document.querySelector('.logo').style.display='none';const r=document.getElementById('result');r.style.display='block';const m=document.getElementById('rmsg');m.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}m.textContent+=MSG[i++];}},46);}}
render();
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 17. SPOTIFY — Fake Spotify Wrapped: love edition
# ══════════════════════════════════════════════════════════════════════════════
def html_spotify(name, date_str):
    msg = "You've been on repeat\nall year.\n\nNot complaining."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;min-height:100%;background:#121212;display:flex;align-items:center;justify-content:center;font-family:'Caveat',cursive;padding:20px}}
#card{{width:min(390px,100%);background:linear-gradient(145deg,#1a1a2e,#16213e 55%,#0f3460);border-radius:22px;padding:30px 26px;position:relative;overflow:hidden}}
.yr{{font-size:.8rem;color:rgba(29,185,84,.65);letter-spacing:.2em;margin-bottom:5px}}
.ttl{{font-family:'Dancing Script',cursive;font-size:clamp(2rem,8vw,2.8rem);color:#fff;line-height:1.1;margin-bottom:5px}}
.by{{font-size:.88rem;color:rgba(255,255,255,.35);letter-spacing:.1em;margin-bottom:26px}}
.sl{{font-size:.76rem;color:rgba(255,255,255,.3);letter-spacing:.18em;text-transform:uppercase;margin-bottom:11px}}
.songs{{display:flex;flex-direction:column;gap:10px;margin-bottom:22px}}
.song{{display:flex;align-items:center;gap:12px}}
.sn{{font-size:.95rem;color:rgba(255,255,255,.22);width:16px;flex-shrink:0;text-align:right}}
.sa{{width:38px;height:38px;border-radius:7px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:1.25rem}}
.si{{flex:1;min-width:0}}.st{{font-size:1.05rem;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.sar{{font-size:.82rem;color:rgba(255,255,255,.38)}}.sp{{font-size:.8rem;color:rgba(29,185,84,.65);flex-shrink:0}}
.stats{{display:flex;gap:12px;margin-bottom:24px}}
.stat{{flex:1;background:rgba(255,255,255,.05);border-radius:12px;padding:13px;text-align:center}}
.sv{{font-family:'Dancing Script',cursive;font-size:1.8rem;color:#1db954}}.sk{{font-size:.78rem;color:rgba(255,255,255,.3);letter-spacing:.08em;margin-top:2px}}
#sbtn{{width:100%;padding:14px;background:#1db954;border:none;border-radius:30px;font-family:'Dancing Script',cursive;font-size:1.4rem;color:#000;cursor:pointer;transition:transform .15s}}
#sbtn:active{{transform:scale(.97)}}
#fin{{margin-top:22px;opacity:0;transition:opacity 1.2s;text-align:center}}
#fin.show{{opacity:1}}
.fmsg{{font-size:clamp(1rem,3.2vw,1.3rem);color:rgba(255,255,255,.82);line-height:1.85;white-space:pre-wrap}}
.ffrom{{font-family:'Dancing Script',cursive;font-size:1.7rem;color:#1db954;margin-top:14px}}
.fdate{{font-size:.7rem;color:rgba(255,255,255,.22);margin-top:3px;letter-spacing:.08em}}</style></head><body>
<div id="card">
  <div class="yr">YOUR 2026 WRAPPED</div>
  <div class="ttl">{name}'s<br/>Year in Love</div>
  <div class="by">curated by Dipesh · Exclusive</div>
  <div class="sl">🎵 top songs</div>
  <div class="songs">
    <div class="song"><div class="sn">1</div><div class="sa" style="background:#3a1540">💜</div><div class="si"><div class="st">the way she laughs</div><div class="sar">Dipesh</div></div><div class="sp">∞</div></div>
    <div class="song"><div class="sn">2</div><div class="sa" style="background:#142540">💙</div><div class="si"><div class="st">honestly just her</div><div class="sar">Dipesh</div></div><div class="sp">∞</div></div>
    <div class="song"><div class="sn">3</div><div class="sa" style="background:#153520">💚</div><div class="si"><div class="st">that one thing she said</div><div class="sar">Dipesh</div></div><div class="sp">∞</div></div>
    <div class="song"><div class="sn">4</div><div class="sa" style="background:#3a1a10">🧡</div><div class="si"><div class="st">{name} (every version)</div><div class="sar">Dipesh</div></div><div class="sp">∞</div></div>
  </div>
  <div class="sl">📊 your stats</div>
  <div class="stats">
    <div class="stat"><div class="sv">∞</div><div class="sk">minutes</div></div>
    <div class="stat"><div class="sv">1</div><div class="sk">top artist</div></div>
    <div class="stat"><div class="sv">365</div><div class="sk">days on repeat</div></div>
  </div>
  <button id="sbtn" onclick="share()">share your wrapped ↗</button>
  <div id="fin"><div class="fmsg" id="fmsg"></div><div class="ffrom">— Dipesh</div><div class="fdate">{date_str}</div></div>
</div><script>
const MSG=`{msg}`;
function share(){{document.getElementById('sbtn').style.display='none';const el=document.getElementById('fin');el.classList.add('show');const m=document.getElementById('fmsg');m.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}m.textContent+=MSG[i++];}},46);}}
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 18. CHAT — Fake iMessage conversation reveal
# ══════════════════════════════════════════════════════════════════════════════
def html_chat(name, date_str):
    msg = "Just wanted you to know.\nNo other reason."
    msgs = json.dumps([
        {"s":"them","t":"hey"},{"s":"me","t":"hey"},
        {"s":"them","t":"made you something"},{"s":"me","t":"wait what"},
        {"s":"them","t":"yeah. it's just a page"},{"s":"them","t":"open it"},
        {"s":"me","t":"you made this for me?"},{"s":"me","t":"why"},
        {"s":"them","t":"because I wanted to."},{"s":"them","t":"that's it."},
    ])
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#1c1c1e;display:flex;align-items:center;justify-content:center;font-family:'Caveat',cursive}}
#ph{{width:min(370px,100%);height:min(680px,100vh);background:#000;border-radius:44px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 0 0 2px #2c2c2e,0 30px 90px rgba(0,0,0,.85)}}
#tb{{background:#1c1c1e;padding:14px 18px 10px;display:flex;align-items:center;gap:11px;flex-shrink:0}}
.av{{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#ff6b6b,#c056cf);display:flex;align-items:center;justify-content:center;font-family:'Dancing Script',cursive;font-size:1.1rem;color:#fff}}
.cn{{font-size:1.05rem;color:#fff}}.cs{{font-size:.72rem;color:#666}}
#msgs{{flex:1;overflow-y:auto;padding:14px 12px;display:flex;flex-direction:column;gap:9px;scroll-behavior:smooth}}
.bub{{max-width:74%;padding:10px 15px;border-radius:20px;font-size:1.05rem;line-height:1.5;opacity:0;transform:translateY(7px);transition:opacity .4s,transform .4s}}
.bub.vis{{opacity:1;transform:translateY(0)}}
.me{{align-self:flex-end;background:#0a84ff;color:#fff;border-bottom-right-radius:5px}}
.them{{align-self:flex-start;background:#2c2c2e;color:#fff;border-bottom-left-radius:5px}}
#typ{{padding:0 12px 6px;color:#666;font-size:.88rem;min-height:22px}}
#fin{{background:#1c1c1e;padding:18px;text-align:center;border-top:1px solid #2c2c2e;flex-shrink:0;opacity:0;transition:opacity 1s;max-height:0;overflow:hidden}}
#fin.show{{opacity:1;max-height:180px}}
.fm{{font-size:clamp(.95rem,3vw,1.15rem);color:rgba(255,255,255,.8);line-height:1.8;white-space:pre-wrap}}
.ff{{font-family:'Dancing Script',cursive;font-size:1.4rem;color:#0a84ff;margin-top:8px}}
.fd{{font-size:.65rem;color:#444;margin-top:2px;letter-spacing:.06em}}</style></head><body>
<div id="ph">
  <div id="tb"><div class="av">J</div><div><div class="cn">{name}</div><div class="cs">iMessage</div></div></div>
  <div id="msgs"></div><div id="typ"></div>
  <div id="fin"><div class="fm" id="fm"></div><div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>
</div><script>
const MS={msgs};const MSG=`{msg}`;const c=document.getElementById('msgs');let idx=0;
function next(){{if(idx>=MS.length){{setTimeout(fin,700);return;}}const m=MS[idx];idx++;
const typ=document.getElementById('typ');if(m.s==='them')typ.textContent='{name} is typing...';
setTimeout(()=>{{typ.textContent='';const b=document.createElement('div');b.className=`bub ${{m.s==='me'?'me':'them'}}`;b.textContent=m.t;c.appendChild(b);requestAnimationFrame(()=>requestAnimationFrame(()=>b.classList.add('vis')));c.scrollTop=c.scrollHeight;setTimeout(next,m.s==='them'?850+m.t.length*20:550);}},m.s==='them'?1100+m.t.length*14:350);}}
function fin(){{const el=document.getElementById('fin');el.classList.add('show');const mEl=document.getElementById('fm');mEl.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}mEl.textContent+=MSG[i++];}},52);}}
setTimeout(next,900);
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 19. RECIPE — Recipe card for a perfect day
# ══════════════════════════════════════════════════════════════════════════════
def html_recipe(name, date_str):
    msg = "Tried to follow the recipe.\nKept getting distracted thinking about you.\n\nTurned out fine anyway."
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;min-height:100%;background:#160d04;display:flex;align-items:flex-start;justify-content:center;font-family:'Caveat',cursive;padding:28px 14px 50px}}
#card{{width:min(460px,100%);background:linear-gradient(160deg,#fef9f0,#fdf4e3);border-radius:16px;padding:30px 26px;box-shadow:0 24px 90px rgba(0,0,0,.7),0 0 0 1px rgba(0,0,0,.08);position:relative}}
.tag{{font-size:.78rem;color:#c47a2a;letter-spacing:.22em;text-transform:uppercase;margin-bottom:7px}}
h1{{font-family:'Dancing Script',cursive;font-size:clamp(1.9rem,7vw,2.7rem);color:#3a1a08;line-height:1.15;margin-bottom:5px}}
.meta{{font-size:.88rem;color:rgba(58,26,8,.4);letter-spacing:.08em;margin-bottom:22px;padding-bottom:16px;border-bottom:1px solid rgba(58,26,8,.1)}}
.sl{{font-size:.78rem;color:#c47a2a;letter-spacing:.2em;text-transform:uppercase;margin-bottom:11px}}
.ings{{margin-bottom:22px;display:flex;flex-direction:column;gap:9px}}
.ing{{display:flex;gap:11px;font-size:1.08rem;color:#3a1a08}}
.amt{{color:#c47a2a;min-width:80px;font-size:.95rem;flex-shrink:0}}
.steps{{margin-bottom:26px;display:flex;flex-direction:column;gap:13px}}
.step{{display:flex;gap:13px}}
.sn{{width:27px;height:27px;border-radius:50%;background:#c47a2a;color:#fff;font-size:.88rem;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:3px}}
.st{{font-size:1.08rem;color:#3a1a08;line-height:1.55}}
#tbtn{{width:100%;padding:13px;background:#c47a2a;border:none;border-radius:30px;font-family:'Dancing Script',cursive;font-size:1.4rem;color:#fff;cursor:pointer;transition:transform .15s;margin-bottom:20px}}
#tbtn:active{{transform:scale(.97)}}
#fin{{opacity:0;transition:opacity 1.2s;text-align:center}}
#fin.show{{opacity:1}}
.fm{{font-size:clamp(1rem,3.2vw,1.25rem);color:#3a1a08;line-height:1.85;white-space:pre-wrap;font-style:italic}}
.ff{{font-family:'Dancing Script',cursive;font-size:1.7rem;color:#c47a2a;margin-top:14px}}
.fd{{font-size:.7rem;color:rgba(58,26,8,.3);margin-top:3px;letter-spacing:.08em}}</style></head><body>
<div id="card">
  <div class="tag">handmade with intention</div>
  <h1>Recipe for<br/>a Perfect Day</h1>
  <div class="meta">Serves: 1 · Prep: all year · Cook time: ongoing</div>
  <div class="sl">Ingredients</div>
  <div class="ings">
    <div class="ing"><span class="amt">1, irreplaceable</span><span>{name}</span></div>
    <div class="ing"><span class="amt">a lot of</span><span>honest conversation</span></div>
    <div class="ing"><span class="amt">handful of</span><span>quiet moments that feel like enough</span></div>
    <div class="ing"><span class="amt">pinch of</span><span>her laughing unexpectedly</span></div>
    <div class="ing"><span class="amt">to taste</span><span>patience, shown not announced</span></div>
    <div class="ing"><span class="amt">generous</span><span>showing up, consistently</span></div>
  </div>
  <div class="sl">Method</div>
  <div class="steps">
    <div class="step"><div class="sn">1</div><div class="st">Start with her. Let everything else adjust around that.</div></div>
    <div class="step"><div class="sn">2</div><div class="st">Add the conversations. Don't rush them.</div></div>
    <div class="step"><div class="sn">3</div><div class="st">Let it sit. The best parts develop slowly.</div></div>
    <div class="step"><div class="sn">4</div><div class="st">Do not substitute any ingredient. Especially the first one.</div></div>
  </div>
  <button id="tbtn" onclick="taste()">taste ↓</button>
  <div id="fin"><div class="fm" id="fm"></div><div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>
</div><script>
const MSG=`{msg}`;
function taste(){{document.getElementById('tbtn').style.display='none';const el=document.getElementById('fin');el.classList.add('show');const m=document.getElementById('fm');m.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}m.textContent+=MSG[i++];}},48);el.scrollIntoView({{behavior:'smooth',block:'center'}});}}
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 20. POLAROID — Flip polaroid gallery on a corkboard
# ══════════════════════════════════════════════════════════════════════════════
def html_polaroid(name, date_str):
    msg = "Ran out of photos.\nHad too many favorites.\n\nEnded up just keeping you."
    photos = json.dumps([
        {"e":"🌅","bg":"linear-gradient(135deg,#ff9a56,#ff6b35)","cap":"early mornings"},
        {"e":"☕","bg":"linear-gradient(135deg,#6b4423,#a0633a)","cap":"slow afternoons"},
        {"e":"🌙","bg":"linear-gradient(135deg,#1a1a4a,#2d2d8a)","cap":"late nights"},
        {"e":"🎵","bg":"linear-gradient(135deg,#2a1a4a,#6b3a8a)","cap":"songs that remind me"},
        {"e":"💗","bg":"linear-gradient(135deg,#4a1a2a,#8a3a4a)","cap":"just because"},
    ])
    backs = json.dumps([
        "you are\nmy favorite\nmorning.",
        "the best part\nof slowing down.",
        "I think about you\nwhen it's quiet.",
        "this one's\nours now.\nI decided.",
        "",
    ])
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>{FONTS}
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;min-height:100%;background:#130c04;display:flex;flex-direction:column;align-items:center;font-family:'Caveat',cursive;padding:32px 10px 50px;overflow-x:hidden}}
.hdr{{text-align:center;margin-bottom:28px}}
.ht{{font-family:'Dancing Script',cursive;font-size:clamp(2rem,7vw,2.6rem);color:#f4c842;text-shadow:0 0 40px rgba(244,200,66,.25)}}
.hs{{font-size:.9rem;color:rgba(244,200,66,.32);letter-spacing:.16em;margin-top:5px}}
#board{{display:flex;flex-wrap:wrap;justify-content:center;gap:18px;max-width:580px;perspective:1000px}}
.pol{{width:min(155px,42vw);cursor:pointer;transform-style:preserve-3d;transition:transform .75s cubic-bezier(.4,0,.2,1);position:relative}}
.pol:nth-child(1){{transform:rotate(-3.5deg)}}.pol:nth-child(2){{transform:rotate(2.5deg)}}.pol:nth-child(3){{transform:rotate(-1deg)}}.pol:nth-child(4){{transform:rotate(3deg)}}.pol:nth-child(5){{transform:rotate(-2.5deg)}}
.pol.fl{{transform:rotateY(180deg)!important}}
.pf,.pb{{backface-visibility:hidden;-webkit-backface-visibility:hidden}}
.pf{{position:relative}}
.pb{{position:absolute;inset:0;transform:rotateY(180deg);background:#fef9f0;padding:14px;border-radius:3px;display:flex;align-items:center;justify-content:center;box-shadow:0 5px 22px rgba(0,0,0,.45)}}
.pp{{width:100%;aspect-ratio:1;border-radius:2px;display:flex;align-items:center;justify-content:center;font-size:clamp(2rem,8vw,3rem)}}
.pframe{{background:#fef9f0;padding:9px 9px 26px;box-shadow:0 5px 22px rgba(0,0,0,.5);border-radius:2px}}
.pcap{{font-size:.88rem;color:#777;text-align:center;margin-top:3px;padding:0 3px}}
.pin{{position:absolute;top:-9px;left:50%;transform:translateX(-50%);width:13px;height:13px;background:#c0392b;border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,.4);z-index:2}}
.bmsg{{font-size:.95rem;color:#3a1a08;text-align:center;line-height:1.65;white-space:pre-wrap}}
#hint{{color:rgba(244,200,66,.35);font-size:.9rem;letter-spacing:.12em;margin-bottom:18px;text-align:center;animation:blink 2.2s infinite}}
@keyframes blink{{0%,100%{{opacity:.28}}50%{{opacity:.8}}}}
#fin{{text-align:center;max-width:440px;padding:18px;opacity:0;transition:opacity 1.2s;margin-top:16px}}
#fin.show{{opacity:1}}
.fmsg{{font-size:clamp(1rem,3.2vw,1.3rem);color:#f4e4a0;line-height:1.88;white-space:pre-wrap}}
.ffrom{{font-family:'Dancing Script',cursive;font-size:1.7rem;color:#f4c842;margin-top:14px}}
.fdate{{font-size:.7rem;color:rgba(244,200,66,.28);margin-top:3px;letter-spacing:.08em}}</style></head><body>
<div class="hdr"><div class="ht">for {name.lower()}</div><div class="hs">a few favorites</div></div>
<div id="hint">tap each photo to flip</div>
<div id="board"></div>
<div id="fin"><div class="fmsg" id="fmsg"></div><div class="ffrom">— Dipesh</div><div class="fdate">{date_str}</div></div>
<script>
const PH={photos};const BK={backs};const MSG=`{msg}`;let flipped=0;const board=document.getElementById('board');
PH.forEach((p,i)=>{{const isLast=i===PH.length-1;const w=document.createElement('div');w.className='pol';
const backContent=isLast?`<div style="text-align:center"><div style="font-size:1.8rem">💗</div><div style="font-family:'Dancing Script',cursive;font-size:1.3rem;color:#c47a2a;margin-top:6px">open me last</div></div>`:`<div class="bmsg">${{BK[i]}}</div>`;
w.innerHTML=`<div class="pf"><div class="pin"></div><div class="pframe"><div class="pp" style="background:${{p.bg}}">${{p.e}}</div></div><div class="pcap">${{p.cap}}</div></div><div class="pb">${{backContent}}</div>`;
w.addEventListener('click',()=>{{if(w.classList.contains('fl'))return;w.classList.add('fl');flipped++;if(flipped===PH.length)setTimeout(showFin,900);}});
board.appendChild(w);}});
function showFin(){{const el=document.getElementById('fin');el.classList.add('show');const m=document.getElementById('fmsg');m.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=MSG.length){{clearInterval(iv);return;}}m.textContent+=MSG[i++];}},48);el.scrollIntoView({{behavior:'smooth',block:'center'}});}}
</script></body></html>"""


# ── HTML dispatcher ────────────────────────────────────────────────────────────
GENERATORS = {
    "galaxy":      html_galaxy,
    "sakura":      html_sakura,
    "ocean":       html_ocean,
    "firefly":     html_firefly,
    "neon":        html_neon,
    "aurora":      html_aurora,
    "sunrise":     html_sunrise,
    "rain":        html_rain,
    "particle":    html_particle,
    "matrix":      html_matrix,
    "butterfly":   html_butterfly,
    "campfire":    html_campfire,
    "heartcatch":  html_heartcatch,
    "memory":      html_memory,
    "reasons":     html_reasons,
    "quiz":        html_quiz,
    "spotify":     html_spotify,
    "chat":        html_chat,
    "recipe":      html_recipe,
    "polaroid":    html_polaroid,
}

ALL_THEMES = [
    # ── Story animations ───────────────────────────────────────────────────────
    {"name": "Galaxy & Universe",  "slug": "galaxy",     "mood": "Emotional, Deep",    "story": "Constellation connect: stars draw heart in sky"},
    {"name": "Cherry Blossom",     "slug": "sakura",     "mood": "Loving, Gentle",     "story": "STORY: Bare trunk grows, heart canopy blooms"},
    {"name": "Ocean Waves",        "slug": "ocean",      "mood": "Romantic, Peaceful", "story": "STORY: Bottle washes ashore, scroll unrolls"},
    {"name": "Firefly Forest",     "slug": "firefly",    "mood": "Dreamy, Magical",    "story": "STORY: Fireflies arrange into name, swarm to heart"},
    {"name": "Neon Glow",          "slug": "neon",       "mood": "Flirty, Bold",       "story": "STORY: Retro CRT terminal searches, finds her name"},
    {"name": "Aurora Borealis",    "slug": "aurora",     "mood": "Breathtaking",       "story": "STORY: Aurora ribbons ripple, write name in light"},
    {"name": "Sunrise",            "slug": "sunrise",    "mood": "Hopeful, Warm",      "story": "STORY: Full night→dawn→gold sky shift"},
    {"name": "Rain on Window",     "slug": "rain",       "mood": "Cozy, Emotional",    "story": "STORY: Rain streaks, finger draws heart in condensation"},
    {"name": "Particle Heart",     "slug": "particle",   "mood": "Dramatic, Loving",   "story": "STORY: EKG flatline → massive beat → morphs to heart"},
    {"name": "Matrix Love",        "slug": "matrix",     "mood": "Bold, Unique",       "story": "STORY: Code rain locks into her name"},
    {"name": "Butterfly Garden",   "slug": "butterfly",  "mood": "Playful, Cute",      "story": "STORY: Chrysalis shakes → butterfly emerges"},
    {"name": "Campfire & Stars",   "slug": "campfire",   "mood": "Cozy, Romantic",     "story": "STORY: Match strikes → candle → warm glow → note"},
    # ── Games ─────────────────────────────────────────────────────────────────
    {"name": "Heart Catch",        "slug": "heartcatch", "mood": "Fun, Sweet",         "story": "GAME: Catch 15 falling hearts with a basket"},
    {"name": "Memory Match",       "slug": "memory",     "mood": "Playful, Satisfying","story": "GAME: Flip cards to find 8 matching pairs"},
    # ── Format departures ─────────────────────────────────────────────────────
    {"name": "13 Reasons",         "slug": "reasons",    "mood": "Sweet, Personal",    "story": "LIST: 13 animated reasons, tap to check each one"},
    {"name": "Find Out",           "slug": "quiz",       "mood": "Fun, Knowing",       "story": "QUIZ: 4 questions — rigged, she's perfect every time"},
    {"name": "Spotify Wrapped",    "slug": "spotify",    "mood": "Playful, Warm",      "story": "FORMAT: Fake Spotify Wrapped — love edition"},
    {"name": "iMessage",           "slug": "chat",       "mood": "Intimate, Simple",   "story": "FORMAT: Fake iMessage conversation reveal"},
    {"name": "Recipe Card",        "slug": "recipe",     "mood": "Warm, Creative",     "story": "FORMAT: Recipe for a perfect day — she's the main ingredient"},
    {"name": "Polaroid Gallery",   "slug": "polaroid",   "mood": "Nostalgic, Tender",  "story": "FORMAT: 5 polaroids on a corkboard — flip to reveal"},
]

def get_html(theme, name, date_str):
    fn = GENERATORS.get(theme["slug"], html_galaxy)
    return fn(name, date_str)


# ── GitHub API ─────────────────────────────────────────────────────────────────
def gh_api(method, path, data=None):
    url = f"https://api.github.com{path}"
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json",
                "Content-Type": "application/json", "User-Agent": "jenisha-love-bot"}
    body = json.dumps(data).encode() if data else None
    req  = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r: return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e: return json.loads(e.read()), e.code

def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    today      = datetime.date.today()
    ordinal    = today.toordinal()
    theme      = ALL_THEMES[ordinal % len(ALL_THEMES)]
    next_theme = ALL_THEMES[(ordinal + 1) % len(ALL_THEMES)]
    date_str   = today.strftime("%B %d · %Y")
    repo_name  = f"for-jenisha-{today.strftime('%Y%m%d')}"
    page_url   = f"https://{USERNAME}.github.io/{repo_name}/"

    print(f"\n{'='*62}")
    print(f"  💗  Daily Love Page — {HER_NAME}")
    print(f"  📅  {date_str}")
    print(f"  🎨  Theme : {theme['name']} ({theme['mood']})")
    print(f"  📖  Story : {theme['story']}")
    print(f"  ➡️   Next  : {next_theme['name']} — {next_theme['story']}")
    print(f"{'='*62}\n")

    html = get_html(theme, HER_NAME, date_str)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "index.html").write_text(html, encoding="utf-8")
        print("✅  HTML generated")

        desc = f"For {HER_NAME} — {theme['name']} 💗 {date_str}"
        repo_data, status = gh_api("POST", "/user/repos", {
            "name": repo_name, "description": desc, "private": False, "auto_init": False,
        })
        if status not in (200, 201):
            if "already exists" in str(repo_data): print(f"⚠️   Repo exists — continuing")
            else: print(f"❌  Failed: {repo_data}"); sys.exit(1)
        else:
            print(f"✅  Repo created → https://github.com/{USERNAME}/{repo_name}")

        run(f'git config --global user.email "{EMAIL}"')
        run(f'git config --global user.name "Dipesh"')
        remote = f"https://{TOKEN}@github.com/{USERNAME}/{repo_name}.git"
        for cmd in ["git init -b main", "git add index.html",
                    'git commit -m "💗 Daily love page for Jenisha"',
                    f"git remote add origin {remote}", "git push -u origin main"]:
            code, _, err = run(cmd, cwd=tmp)
            if code != 0 and "already exists" not in err:
                print(f"⚠️   {cmd.replace(TOKEN,'***')} → {err}")
            else:
                print(f"✅  {cmd.replace(TOKEN,'***')}")

        time.sleep(4)
        gh_api("POST", f"/repos/{USERNAME}/{repo_name}/pages", {"source": {"branch":"main","path":"/"}})
        print(f"✅  Pages enabled → {page_url}\n")
        return page_url, theme, next_theme, date_str, repo_name

if __name__ == "__main__":
    main()
