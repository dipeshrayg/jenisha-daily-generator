"""
Daily Jenisha Love Page Generator  v3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Every page tells a STORY. Animation IS the message.
Three story mechanics rotate by day:
  • TREE   — bare tree grows → forms heart shape → blossoms bloom → petals drift → card
  • LETTER — mood background → sealed envelope arrives → wax seal breaks → letter unfolds → typewriter
  • GATHER — particles scattered → slowly converge → form glowing heart → message emerges

Messages are SHORT (2-4 lines) and sound like a real person, not a greeting card.
No confetti buttons.
"""

import os, json, subprocess, datetime, sys, time, tempfile, urllib.request, urllib.error, hashlib
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


# ── Theme definitions ──────────────────────────────────────────────────────────
# Each theme has: colors, particles, a short REAL message (2-4 lines, not a poem)
ALL_THEMES = [
    {
        "name": "Galaxy & Universe", "slug": "galaxy", "mood": "Emotional, Deep",
        "mechanic": "gather",
        "bg_from": "#0a0618", "bg_to": "#030008",
        "primary": "#c44dff", "secondary": "#ff6b9d", "glow": "180,80,255",
        "star_col": "210,185,255",
        "particles": ["✦","·","*","○","◦"],
        "particle_col": "#c44dff",
        "heart_col": "#c44dff", "heart_glow": "180,80,255",
        "msg": "Made this for you today.\nJust wanted you to know\nyou're on my mind.",
        "card_bg": "rgba(12,6,24,.96)", "card_text": "#e8d4ff", "card_accent": "#c44dff",
    },
    {
        "name": "Cherry Blossom", "slug": "sakura", "mood": "Loving, Gentle",
        "mechanic": "tree",
        "bg_from": "#18060f", "bg_to": "#080208",
        "primary": "#ffb7c5", "secondary": "#ff80aa", "glow": "255,150,200",
        "star_col": "255,210,225",
        "petal_cols": ["#ffb7c5","#ffc8d4","#ffdde8","#ffadc0","#ffe0ea"],
        "trunk_col": "rgba(90,52,22,.82)", "blossom_center": "#fffde7",
        "msg": "Made this for you.\nCouldn't fit all the reasons\nonto one tree.\n\nSo I just used blossoms.",
        "card_bg": "rgba(255,251,252,.97)", "card_text": "#3a1020", "card_accent": "#c2185b",
    },
    {
        "name": "Ocean Waves", "slug": "ocean", "mood": "Romantic, Peaceful",
        "mechanic": "letter",
        "bg_from": "#001830", "bg_to": "#00090f",
        "primary": "#4fc3f7", "secondary": "#0288d1", "glow": "79,195,247",
        "star_col": "150,220,255",
        "env_col": "#e8f4fd", "env_accent": "#0288d1", "seal_col": "#0277bd",
        "wave_col_1": "rgba(0,100,160,.18)", "wave_col_2": "rgba(0,150,200,.1)",
        "msg": "Hey.\nOpening this to let you know\nyou make everything feel calmer.\n\nThat's a rare thing.",
        "card_bg": "rgba(5,20,35,.96)", "card_text": "#c8e8f8", "card_accent": "#4fc3f7",
    },
    {
        "name": "Firefly Forest", "slug": "firefly", "mood": "Dreamy, Magical",
        "mechanic": "gather",
        "bg_from": "#060e04", "bg_to": "#020602",
        "primary": "#c8ff70", "secondary": "#88dd30", "glow": "180,255,80",
        "star_col": "200,255,150",
        "particles": ["◦","·","○","◌","∘"],
        "particle_col": "#c8ff70",
        "heart_col": "#b8ff50", "heart_glow": "160,240,60",
        "msg": "You make quiet places\nfeel less quiet.\n\nThought you should know that.",
        "card_bg": "rgba(6,14,4,.96)", "card_text": "#d0ffb0", "card_accent": "#aaee44",
    },
    {
        "name": "Neon Glow", "slug": "neon", "mood": "Flirty, Fun",
        "mechanic": "letter",
        "bg_from": "#0a0015", "bg_to": "#05000a",
        "primary": "#ff2d78", "secondary": "#00ffcc", "glow": "255,45,120",
        "star_col": "255,100,180",
        "env_col": "#1a0020", "env_accent": "#ff2d78", "seal_col": "#ff2d78",
        "wave_col_1": "rgba(255,45,120,.06)", "wave_col_2": "rgba(0,255,200,.04)",
        "msg": "You showed up in my life\nand now everything else\nis a lot less interesting.",
        "card_bg": "rgba(15,0,25,.97)", "card_text": "#ffe0f0", "card_accent": "#ff2d78",
    },
    {
        "name": "Aurora Borealis", "slug": "aurora", "mood": "Breathtaking",
        "mechanic": "gather",
        "bg_from": "#000c10", "bg_to": "#000508",
        "primary": "#00ffcc", "secondary": "#7b2fff", "glow": "0,230,180",
        "star_col": "180,255,240",
        "particles": ["∘","◦","·","○","⬡"],
        "particle_col": "#00ffcc",
        "heart_col": "#00e8b8", "heart_glow": "0,200,160",
        "msg": "Some things are only visible\nif you look at exactly the right moment.\n\nI'm glad I looked up.",
        "card_bg": "rgba(0,12,16,.97)", "card_text": "#c0fff4", "card_accent": "#00ffcc",
    },
    {
        "name": "Sunrise", "slug": "sunrise", "mood": "Hopeful, Warm",
        "mechanic": "letter",
        "bg_from": "#120400", "bg_to": "#060100",
        "primary": "#ffb347", "secondary": "#ff6b35", "glow": "255,160,60",
        "star_col": "255,210,150",
        "env_col": "#fff8f0", "env_accent": "#e65100", "seal_col": "#d84315",
        "wave_col_1": "rgba(255,140,20,.1)", "wave_col_2": "rgba(255,80,20,.06)",
        "msg": "Every day you're in it\nstarts better than the last.\n\nThat's all this is about.",
        "card_bg": "rgba(18,4,0,.97)", "card_text": "#fff0d0", "card_accent": "#ffb347",
    },
    {
        "name": "Rain on Window", "slug": "rain", "mood": "Cozy, Emotional",
        "mechanic": "letter",
        "bg_from": "#060810", "bg_to": "#020408",
        "primary": "#7eb8e8", "secondary": "#4a90d9", "glow": "100,170,230",
        "star_col": "140,190,240",
        "env_col": "#f0f4f8", "env_accent": "#1565c0", "seal_col": "#0d47a1",
        "wave_col_1": "rgba(60,130,200,.12)", "wave_col_2": "rgba(30,90,180,.07)",
        "msg": "You're the kind of person\nI want to be around\nwhen it rains.\n\nAnd every other time.",
        "card_bg": "rgba(6,8,16,.97)", "card_text": "#d0e4f8", "card_accent": "#7eb8e8",
    },
    {
        "name": "Particle Heart", "slug": "particle", "mood": "Dramatic, Loving",
        "mechanic": "gather",
        "bg_from": "#120005", "bg_to": "#060003",
        "primary": "#ff1464", "secondary": "#ff6b9d", "glow": "255,20,100",
        "star_col": "255,150,180",
        "particles": ["♥","❤","·","◦","∘"],
        "particle_col": "#ff1464",
        "heart_col": "#ff1464", "heart_glow": "255,20,100",
        "msg": "Jenisha.\n\nThat's it.\nThat's the whole message.",
        "card_bg": "rgba(18,0,5,.97)", "card_text": "#ffd0e0", "card_accent": "#ff1464",
    },
    {
        "name": "Matrix Love", "slug": "matrix", "mood": "Bold, Unique",
        "mechanic": "letter",
        "bg_from": "#000800", "bg_to": "#000200",
        "primary": "#00ff41", "secondary": "#00cc33", "glow": "0,220,50",
        "star_col": "100,255,120",
        "env_col": "#001200", "env_accent": "#00ff41", "seal_col": "#00cc33",
        "wave_col_1": "rgba(0,200,40,.07)", "wave_col_2": "rgba(0,150,30,.04)",
        "msg": "If I could write you a program\nit would just be an infinite loop\nthat prints your name.",
        "card_bg": "rgba(0,8,0,.97)", "card_text": "#b0ffb8", "card_accent": "#00ff41",
    },
    {
        "name": "Butterfly Garden", "slug": "butterfly", "mood": "Playful, Cute",
        "mechanic": "tree",
        "bg_from": "#080818", "bg_to": "#030310",
        "primary": "#f9a8d4", "secondary": "#a78bfa", "glow": "240,140,200",
        "star_col": "220,180,255",
        "petal_cols": ["#f9a8d4","#e879f9","#c084fc","#fbbf24","#a78bfa"],
        "trunk_col": "rgba(80,50,100,.75)", "blossom_center": "#fef9c3",
        "msg": "Opening this probably surprised you.\nGood.\nYou deserve nice surprises.",
        "card_bg": "rgba(8,8,24,.97)", "card_text": "#f0d8ff", "card_accent": "#c084fc",
    },
    {
        "name": "Campfire & Stars", "slug": "campfire", "mood": "Cozy, Romantic",
        "mechanic": "letter",
        "bg_from": "#0f0400", "bg_to": "#050100",
        "primary": "#ff8c42", "secondary": "#ffcc70", "glow": "255,140,66",
        "star_col": "255,200,120",
        "env_col": "#fff8f0", "env_accent": "#e65100", "seal_col": "#bf360c",
        "wave_col_1": "rgba(255,100,20,.09)", "wave_col_2": "rgba(255,200,50,.05)",
        "msg": "If I could pick one place to be right now\nit would be wherever you are.\n\nThat's all.",
        "card_bg": "rgba(15,4,0,.97)", "card_text": "#fff0d8", "card_accent": "#ff8c42",
    },
]

MECHANICS = {t["slug"]: t["mechanic"] for t in ALL_THEMES}


# ── Story mechanic: TREE (heart-shaped blossom tree) ──────────────────────────
def html_tree(theme, name, date_str):
    p  = theme["primary"]
    bf = theme["bg_from"]
    bt = theme["bg_to"]
    g  = theme["glow"]
    sc = theme["star_col"]
    pc = json.dumps(theme["petal_cols"])
    tc = theme["trunk_col"]
    bc = theme["blossom_center"]
    ca = theme["card_accent"]
    cb = theme["card_bg"]
    ct = theme["card_text"]
    msg_esc = theme["msg"].replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Caveat:wght@400;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;overflow:hidden;background:{bf}}}
#start{{position:fixed;inset:0;z-index:80;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;background:{bf};transition:opacity 1.4s ease;cursor:pointer}}
#start.gone{{opacity:0;pointer-events:none}}
.sn{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,13vw,6.5rem);color:{p};text-shadow:0 0 50px rgba({g},.5),0 0 100px rgba({g},.2);animation:glow 2.8s ease-in-out infinite}}
.sh{{font-family:'Caveat',cursive;font-size:clamp(1rem,3.5vw,1.3rem);letter-spacing:.18em;color:rgba({g},.45);animation:bl 2s ease-in-out infinite}}
@keyframes glow{{0%,100%{{text-shadow:0 0 40px rgba({g},.4)}}50%{{text-shadow:0 0 70px rgba({g},.7),0 0 120px rgba({g},.3)}}}}
@keyframes bl{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
#card{{position:fixed;left:50%;bottom:-240px;transform:translateX(-50%);width:min(360px,90vw);background:{cb};border-radius:18px;padding:28px 30px 24px;box-shadow:0 12px 60px rgba(0,0,0,.4),0 0 0 1px rgba({g},.2);z-index:60;transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;border:1px solid rgba({g},.15)}}
#card.show{{bottom:clamp(20px,4vh,55px)}}
.cto{{font-family:'Caveat',cursive;font-size:.82rem;letter-spacing:.15em;color:rgba({g},.5);text-transform:uppercase;margin-bottom:12px}}
.cmsg{{font-family:'Caveat',cursive;font-size:clamp(1.2rem,3.5vw,1.45rem);line-height:1.75;color:{ct};min-height:4rem;white-space:pre-wrap}}
.cfrom{{margin-top:16px;font-family:'Dancing Script',cursive;font-size:1.5rem;color:{ca};text-align:right}}
.cdate{{font-size:.68rem;color:rgba({g},.3);text-align:right;margin-top:2px;letter-spacing:.06em}}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="start" onclick="begin()"><div class="sn">{name}</div><div class="sh">tap to open</div></div>
<div id="card"><div class="cto">for {name.lower()} 🌸</div><div class="cmsg" id="cmsg"></div><div class="cfrom">— Dipesh</div><div class="cdate">{date_str}</div></div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
let HCX=W/2,HCY=H*.41,S=Math.min(W*.022,H*.018);
function recalc(){{HCX=W/2;HCY=H*.41;S=Math.min(W*.022,H*.018);}}
function heartPt(t){{
  const x=16*Math.pow(Math.sin(t),3);
  const y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));
  return{{x:HCX+x*S,y:HCY+y*S}};
}}
const STARS=Array.from({{length:220}},()=>{{return{{x:Math.random(),y:Math.random(),r:.3+Math.random()*1.4,base:.1+Math.random()*.55,tp:Math.random()*Math.PI*2,ts:.006+Math.random()*.014}}}});
function drawStars(){{STARS.forEach(s=>{{s.tp+=s.ts;const a=s.base+Math.sin(s.tp)*.22;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba({sc},${{Math.max(0,a)}})`;ctx.fill()}});}}
const N=28;let BRANCHES=[];
function buildBranches(){{
  BRANCHES=[];
  const tipY=heartPt(Math.PI).y,baseY=H*.855;
  for(let i=0;i<N;i++){{
    const t=(i/N)*Math.PI*2,tip=heartPt(t);
    const vf=Math.max(0,Math.min(.72,(tip.y-tipY)/(baseY-tipY)));
    const bx=HCX+(tip.x-HCX)*.06,by=tipY+vf*(baseY-tipY);
    const ctrlX=bx+(tip.x-bx)*.42+(Math.random()-.5)*S*4;
    const ctrlY=by+(tip.y-by)*.36-S*6;
    const dy=tip.y-HCY,maxDy=17*S,thick=1.2+Math.max(0,dy/maxDy)*2;
    BRANCHES.push({{base:{{x:bx,y:by}},ctrl:{{x:ctrlX,y:ctrlY}},tip,progress:0,delay:i*.038,width:thick}});
  }}
}}
buildBranches();
function bPt(p0,p1,p2,t){{const u=1-t;return{{x:u*u*p0.x+2*u*t*p1.x+t*t*p2.x,y:u*u*p0.y+2*u*t*p1.y+t*t*p2.y}};}}
function drawBranch(b,prog){{
  if(prog<=0)return;
  const steps=24;ctx.beginPath();ctx.moveTo(b.base.x,b.base.y);
  const end=Math.min(1,prog);
  for(let i=1;i<=steps;i++){{const f=i/steps;if(f>end+.001)break;const p=bPt(b.base,b.ctrl,b.tip,Math.min(end,f));ctx.lineTo(p.x,p.y);}}
  ctx.strokeStyle='{tc}';ctx.lineWidth=b.width;ctx.lineCap='round';ctx.lineJoin='round';ctx.stroke();
}}
function drawTrunk(prog){{
  if(prog<=0)return;
  const tipY=heartPt(Math.PI).y,baseY=H*.855,steps=28;
  for(let i=0;i<steps;i++){{const f0=i/steps,f1=(i+1)/steps;if(f0>prog)break;const y0=baseY-(baseY-tipY)*f0,y1=baseY-(baseY-tipY)*Math.min(prog,f1);const w=11-f0*7.5;ctx.beginPath();ctx.moveTo(HCX,y0);ctx.lineTo(HCX,y1);ctx.strokeStyle='rgba(70,38,14,.88)';ctx.lineWidth=Math.max(1.5,w);ctx.lineCap='round';ctx.stroke();}}
}}
const PC={pc};
function drawBlossom(x,y,size,alpha){{
  if(alpha<=0||size<=0)return;
  ctx.save();ctx.globalAlpha=Math.min(1,alpha);
  for(let i=0;i<5;i++){{const a=(i/5)*Math.PI*2-Math.PI/10,px=x+Math.cos(a)*size*.62,py=y+Math.sin(a)*size*.62;ctx.beginPath();ctx.arc(px,py,size*.54,0,Math.PI*2);ctx.fillStyle=PC[i%PC.length];ctx.fill();}}
  ctx.beginPath();ctx.arc(x,y,size*.3,0,Math.PI*2);ctx.fillStyle='{bc}';ctx.fill();
  ctx.restore();
}}
const PETALS=[];
class FP{{
  constructor(init){{this.x=Math.random()*W*1.3-W*.15;this.y=init?Math.random()*H:-16;this.vx=-.4+Math.random()*.9;this.vy=.5+Math.random()*1.1;this.rot=Math.random()*Math.PI*2;this.rs=(Math.random()-.5)*.045;this.sz=3.5+Math.random()*5;this.a=.45+Math.random()*.45;this.col=PC[Math.floor(Math.random()*PC.length)];}}
  tick(){{this.x+=this.vx;this.y+=this.vy;this.rot+=this.rs;this.vx+=(Math.random()-.5)*.04;if(this.y>H+20){{this.x=Math.random()*W*1.3-W*.15;this.y=-16;this.vx=-.4+Math.random()*.9;this.vy=.5+Math.random()*1.1;}}}}
  draw(){{ctx.save();ctx.translate(this.x,this.y);ctx.rotate(this.rot);ctx.globalAlpha=this.a;ctx.beginPath();ctx.ellipse(0,0,this.sz,this.sz*.55,0,0,Math.PI*2);ctx.fillStyle=this.col;ctx.fill();ctx.restore();}}
}}
let phase=0,trunkProg=0,elapsed=0,prevT=0,cardDone=false;
const MSG=`{msg_esc}`;
function typeMsg(el,text,speed){{el.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=text.length){{clearInterval(iv);return;}}el.textContent+=text[i++];}},speed);}}
function showCard(){{document.getElementById('card').classList.add('show');setTimeout(()=>typeMsg(document.getElementById('cmsg'),MSG,42),700);}}
function begin(){{document.getElementById('start').classList.add('gone');setTimeout(()=>{{phase=1;prevT=performance.now();requestAnimationFrame(loop);}},1400);}}
function drawBg(){{
  const bg=ctx.createRadialGradient(HCX,HCY,0,HCX,HCY,Math.max(W,H)*.75);
  bg.addColorStop(0,'{bf}');bg.addColorStop(1,'{bt}');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
}}
function loop(ts){{
  if(!prevT)prevT=ts;
  const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  ctx.clearRect(0,0,W,H);drawBg();
  if(phase>=3){{const glow=ctx.createRadialGradient(HCX,HCY-S*2,0,HCX,HCY,S*22);glow.addColorStop(0,'rgba({g},.07)');glow.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=glow;ctx.fillRect(0,0,W,H);}}
  drawStars();
  if(phase===1){{trunkProg=Math.min(1,elapsed/1.3);drawTrunk(trunkProg);if(trunkProg>=1){{phase=2;elapsed=0;}}}}
  if(phase>=2)drawTrunk(1);
  if(phase>=2){{
    let allDone=true;
    BRANCHES.forEach(b=>{{
      if(phase===2)b.progress=Math.min(1,Math.max(0,(elapsed-b.delay)/.65));
      if(b.progress<1)allDone=false;
      drawBranch(b,b.progress);
    }});
    if(phase===2&&allDone){{phase=3;elapsed=0;for(let i=0;i<55;i++)PETALS.push(new FP(false));}}
  }}
  if(phase>=3){{
    BRANCHES.forEach((b,i)=>{{const bp=Math.min(1,Math.max(0,(elapsed-i*.055)/.45));drawBlossom(b.tip.x,b.tip.y,S*1.25*bp,bp);}});
    if(phase===3){{const last=BRANCHES.length*.055+.45;if(elapsed>last+.9&&!cardDone){{cardDone=true;phase=4;elapsed=0;setTimeout(showCard,500);}}}}
  }}
  if(phase===4){{
    BRANCHES.forEach(b=>drawBlossom(b.tip.x,b.tip.y,S*1.25,1));
    PETALS.forEach(p=>{{p.tick();p.draw();}});
  }}
  requestAnimationFrame(loop);
}}
function idleLoop(ts){{if(phase>0)return;ctx.clearRect(0,0,W,H);drawBg();drawStars();requestAnimationFrame(idleLoop);}}
requestAnimationFrame(idleLoop);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;recalc();buildBranches();}});
</script>
</body></html>"""


# ── Story mechanic: LETTER (envelope opens → letter reveals) ──────────────────
def html_letter(theme, name, date_str):
    p   = theme["primary"]
    bf  = theme["bg_from"]
    bt  = theme["bg_to"]
    g   = theme["glow"]
    sc  = theme["star_col"]
    ec  = theme["env_col"]
    ea  = theme["env_accent"]
    sl  = theme["seal_col"]
    w1  = theme["wave_col_1"]
    w2  = theme["wave_col_2"]
    ca  = theme["card_accent"]
    cb  = theme["card_bg"]
    ct  = theme["card_text"]
    msg_esc = theme["msg"].replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Caveat:wght@400;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;overflow:hidden;background:{bf};font-family:'Caveat',cursive}}
#start{{position:fixed;inset:0;z-index:80;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;background:{bf};transition:opacity 1.4s ease;cursor:pointer}}
#start.gone{{opacity:0;pointer-events:none}}
.sn{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,13vw,6.5rem);color:{p};text-shadow:0 0 50px rgba({g},.5);animation:glow 2.8s ease-in-out infinite}}
.sh{{font-size:clamp(1rem,3.5vw,1.3rem);letter-spacing:.18em;color:rgba({g},.45);animation:bl 2s ease-in-out infinite}}
@keyframes glow{{0%,100%{{text-shadow:0 0 40px rgba({g},.4)}}50%{{text-shadow:0 0 70px rgba({g},.7)}}}}
@keyframes bl{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
#scene{{position:fixed;inset:0;z-index:10;display:flex;align-items:center;justify-content:center;pointer-events:none}}
.envelope{{position:relative;width:min(320px,85vw);transform:translateY(120vh);transition:transform 1.2s cubic-bezier(.34,1.3,.64,1);filter:drop-shadow(0 20px 60px rgba(0,0,0,.5))}}
.envelope.arrive{{transform:translateY(0)}}
.env-body{{background:{ec};border-radius:8px;padding:0;aspect-ratio:1.6/1;overflow:hidden;position:relative}}
.env-flap{{position:absolute;top:0;left:0;right:0;height:50%;background:{ec};clip-path:polygon(0 0,100% 0,50% 100%);border-bottom:2px solid rgba(0,0,0,.08);transform-origin:top center;transition:transform 1s cubic-bezier(.4,0,.2,1) .3s}}
.envelope.open .env-flap{{transform:rotateX(180deg)}}
.seal{{position:absolute;top:30%;left:50%;transform:translate(-50%,-50%) scale(1);width:44px;height:44px;border-radius:50%;background:{sl};display:flex;align-items:center;justify-content:center;font-size:1.3rem;transition:transform .5s ease .1s,opacity .4s ease .1s;z-index:5}}
.envelope.open .seal{{transform:translate(-50%,-50%) scale(0);opacity:0}}
.env-letter{{position:absolute;bottom:0;left:5%;right:5%;background:#fffef8;border-radius:6px 6px 0 0;padding:18px 16px 10px;transform:translateY(85%);transition:transform 1s cubic-bezier(.34,1.2,.64,1) .6s;box-shadow:0 -4px 20px rgba(0,0,0,.12)}}
.envelope.open .env-letter{{transform:translateY(0%)}}
.letter-name{{font-family:'Dancing Script',cursive;font-size:1.3rem;color:{ea};margin-bottom:6px}}
.letter-msg{{font-size:clamp(.95rem,2.8vw,1.1rem);color:#2a2030;line-height:1.7;white-space:pre-wrap;min-height:3em}}
.letter-from{{font-family:'Dancing Script',cursive;font-size:1.1rem;color:{ea};text-align:right;margin-top:8px}}
.letter-date{{font-size:.65rem;color:rgba(0,0,0,.3);text-align:right;margin-top:2px}}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="start" onclick="begin()"><div class="sn">{name}</div><div class="sh">tap to open</div></div>
<div id="scene">
  <div class="envelope" id="env">
    <div class="env-body">
      <div class="env-flap"></div>
      <div class="seal">💌</div>
      <div class="env-letter">
        <div class="letter-name">Hey {name},</div>
        <div class="letter-msg" id="lmsg"></div>
        <div class="letter-from">— Dipesh</div>
        <div class="letter-date">{date_str}</div>
      </div>
    </div>
  </div>
</div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const STARS=Array.from({{length:200}},()=>{{return{{x:Math.random(),y:Math.random(),r:.3+Math.random()*1.4,base:.1+Math.random()*.55,tp:Math.random()*Math.PI*2,ts:.006+Math.random()*.014}}}});
function drawStars(){{STARS.forEach(s=>{{s.tp+=s.ts;const a=s.base+Math.sin(s.tp)*.22;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba({sc},${{Math.max(0,a)}})`;ctx.fill()}});}}
const waves=[];for(let i=0;i<6;i++)waves.push({{phase:Math.random()*Math.PI*2,speed:.003+Math.random()*.005,amp:20+Math.random()*30,y:.4+Math.random()*.5}});
let wt=0;
function drawBg(){{
  const bg=ctx.createLinearGradient(0,0,0,H);bg.addColorStop(0,'{bf}');bg.addColorStop(1,'{bt}');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
  wt+=.016;
  waves.forEach(w=>{{
    ctx.beginPath();ctx.moveTo(0,w.y*H);
    for(let x=0;x<=W;x+=4){{const y=w.y*H+Math.sin(x*.006+w.phase+wt*w.speed*100)*w.amp;ctx.lineTo(x,y);}}
    ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();
    ctx.fillStyle=w.y<.5?'{w1}':'{w2}';ctx.fill();w.phase+=w.speed;
  }});
}}
const MSG=`{msg_esc}`;
function typeMsg(el,text,speed){{el.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=text.length){{clearInterval(iv);return;}}el.textContent+=text[i++];}},speed);}}
function begin(){{
  document.getElementById('start').classList.add('gone');
  const env=document.getElementById('env');
  setTimeout(()=>env.classList.add('arrive'),1400);
  setTimeout(()=>env.classList.add('open'),2800);
  setTimeout(()=>typeMsg(document.getElementById('lmsg'),MSG,44),4000);
}}
function loop(){{ctx.clearRect(0,0,W,H);drawBg();drawStars();requestAnimationFrame(loop);}}
loop();
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script>
</body></html>"""


# ── Story mechanic: GATHER (particles converge into glowing heart) ─────────────
def html_gather(theme, name, date_str):
    p   = theme["primary"]
    s   = theme["secondary"]
    bf  = theme["bg_from"]
    bt  = theme["bg_to"]
    g   = theme["glow"]
    sc  = theme["star_col"]
    pc  = theme["particle_col"]
    hc  = theme["heart_col"]
    hg  = theme["heart_glow"]
    ca  = theme["card_accent"]
    cb  = theme["card_bg"]
    ct  = theme["card_text"]
    msg_esc = theme["msg"].replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name}</title>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Caveat:wght@400;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;overflow:hidden;background:{bf}}}
#start{{position:fixed;inset:0;z-index:80;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;background:{bf};transition:opacity 1.4s ease;cursor:pointer}}
#start.gone{{opacity:0;pointer-events:none}}
.sn{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,13vw,6.5rem);color:{p};text-shadow:0 0 50px rgba({g},.5);animation:glow 2.8s ease-in-out infinite}}
.sh{{font-family:'Caveat',cursive;font-size:clamp(1rem,3.5vw,1.3rem);letter-spacing:.18em;color:rgba({g},.45);animation:bl 2s ease-in-out infinite}}
@keyframes glow{{0%,100%{{text-shadow:0 0 40px rgba({g},.4)}}50%{{text-shadow:0 0 70px rgba({g},.7)}}}}
@keyframes bl{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
#card{{position:fixed;left:50%;bottom:-220px;transform:translateX(-50%);width:min(360px,90vw);background:{cb};border-radius:18px;padding:26px 28px 22px;box-shadow:0 12px 60px rgba(0,0,0,.5),0 0 0 1px rgba({g},.2);z-index:60;transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;border:1px solid rgba({g},.15)}}
#card.show{{bottom:clamp(20px,4vh,55px)}}
.cto{{font-family:'Caveat',cursive;font-size:.82rem;letter-spacing:.15em;color:rgba({g},.5);text-transform:uppercase;margin-bottom:12px}}
.cmsg{{font-family:'Caveat',cursive;font-size:clamp(1.2rem,3.5vw,1.45rem);line-height:1.75;color:{ct};min-height:4rem;white-space:pre-wrap}}
.cfrom{{margin-top:16px;font-family:'Dancing Script',cursive;font-size:1.5rem;color:{ca};text-align:right}}
.cdate{{font-size:.68rem;color:rgba({g},.3);text-align:right;margin-top:2px;letter-spacing:.06em}}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="start" onclick="begin()"><div class="sn">{name}</div><div class="sh">tap to open</div></div>
<div id="card"><div class="cto">for {name.lower()}</div><div class="cmsg" id="cmsg"></div><div class="cfrom">— Dipesh</div><div class="cdate">{date_str}</div></div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const CX=()=>W/2, CY=()=>H*.44, SC=()=>Math.min(W*.028,H*.022);
// Heart points
function heartPts(n){{
  const pts=[],scale=SC();
  const cx=CX(),cy=CY();
  for(let i=0;i<n;i++){{
    const t=(i/n)*Math.PI*2;
    const x=16*Math.pow(Math.sin(t),3);
    const y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));
    pts.push({{x:cx+x*scale,y:cy+y*scale}});
  }}
  return pts;
}}
const STARS=Array.from({{length:240}},()=>{{return{{x:Math.random(),y:Math.random(),r:.3+Math.random()*1.5,base:.1+Math.random()*.6,tp:Math.random()*Math.PI*2,ts:.006+Math.random()*.014}}}});
function drawStars(){{STARS.forEach(s=>{{s.tp+=s.ts;const a=s.base+Math.sin(s.tp)*.25;ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);ctx.fillStyle=`rgba({sc},${{Math.max(0,a)}})`;ctx.fill()}});}}
// Particles
const NPART=120;
let particles=[];
let heartTargets=[];
let gathering=false,gathered=false;
let gatherStart=0,gatherDur=3.5;
let heartPulse=0,heartAlpha=0;
let cardDone=false;

function initParticles(){{
  heartTargets=heartPts(NPART);
  particles=Array.from({{length:NPART}},(_,i)=>{{
    return{{
      x:Math.random()*W,y:Math.random()*H,
      tx:heartTargets[i].x,ty:heartTargets[i].y,
      vx:(Math.random()-.5)*1.5,vy:(Math.random()-.5)*1.5,
      size:1.5+Math.random()*2.5,alpha:.3+Math.random()*.5,
      gathering:false,t:0,
    }};
  }});
}}

function drawHeart(){{
  if(heartAlpha<=0)return;
  const scale=SC(),cx=CX(),cy=CY();
  ctx.save();
  ctx.globalAlpha=heartAlpha;
  // Glow
  const gr=ctx.createRadialGradient(cx,cy,0,cx,cy,scale*20);
  gr.addColorStop(0,`rgba({hg},.25)`);gr.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=gr;ctx.fillRect(0,0,W,H);
  // Stroke heart
  ctx.beginPath();
  const n=80;
  for(let i=0;i<=n;i++){{
    const t=(i/n)*Math.PI*2;
    const x=cx+16*Math.pow(Math.sin(t),3)*scale;
    const y=cy-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t))*scale;
    i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  }}
  ctx.closePath();
  const pulse=1+Math.sin(heartPulse)*.04;
  ctx.shadowColor='{hc}';ctx.shadowBlur=20*pulse;
  ctx.strokeStyle='{hc}';ctx.lineWidth=2.5*pulse;ctx.stroke();
  ctx.shadowBlur=0;
  ctx.restore();
}}

const MSG=`{msg_esc}`;
function typeMsg(el,text,speed){{el.textContent='';let i=0;const iv=setInterval(()=>{{if(i>=text.length){{clearInterval(iv);return;}}el.textContent+=text[i++];}},speed);}}
function showCard(){{document.getElementById('card').classList.add('show');setTimeout(()=>typeMsg(document.getElementById('cmsg'),MSG,42),700);}}

let phase=0,prevT=0,elapsed=0;
function begin(){{
  document.getElementById('start').classList.add('gone');
  initParticles();
  setTimeout(()=>{{phase=1;gathering=true;gatherStart=performance.now();prevT=performance.now();requestAnimationFrame(loop);}},1400);
}}

function drawBg(){{
  const bg=ctx.createRadialGradient(CX(),CY(),0,CX(),CY(),Math.max(W,H)*.8);
  bg.addColorStop(0,'{bf}');bg.addColorStop(1,'{bt}');
  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);
}}

function loop(ts){{
  if(!prevT)prevT=ts;
  const dt=Math.min(.08,(ts-prevT)/1000);prevT=ts;elapsed+=dt;
  ctx.clearRect(0,0,W,H);drawBg();drawStars();

  if(phase===1){{
    const gp=Math.min(1,(ts-gatherStart)/1000/gatherDur);
    heartAlpha=Math.max(0,gp-.4)/.6;
    heartPulse+=.04;
    drawHeart();
    // Move particles toward heart
    particles.forEach((p,i)=>{{
      const ease=Math.pow(gp,1.8);
      p.x+=(p.tx-p.x)*ease*.06+(1-ease)*p.vx;
      p.y+=(p.ty-p.y)*ease*.06+(1-ease)*p.vy;
      const a=p.alpha*(1-ease*.3);
      ctx.beginPath();ctx.arc(p.x,p.y,p.size*(1-ease*.5+.5),0,Math.PI*2);
      ctx.fillStyle=`rgba({g},${{Math.max(0,a)}})`;ctx.fill();
    }});
    if(gp>=1&&!cardDone){{phase=2;cardDone=true;setTimeout(showCard,800);}}
  }}

  if(phase===2){{
    heartAlpha=1;heartPulse+=.04;
    drawHeart();
    // Particles stay on heart outline, gently orbiting
    const scale=SC(),cx=CX(),cy=CY();
    particles.forEach((p,i)=>{{
      const t=(i/NPART)*Math.PI*2+elapsed*.05;
      p.x=cx+16*Math.pow(Math.sin(t),3)*scale+(Math.random()-.5)*2;
      p.y=cy-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t))*scale+(Math.random()-.5)*2;
      ctx.beginPath();ctx.arc(p.x,p.y,p.size*.8,0,Math.PI*2);
      ctx.fillStyle=`rgba({g},.6)`;ctx.fill();
    }});
  }}

  requestAnimationFrame(loop);
}}

function idleLoop(){{if(phase>0)return;ctx.clearRect(0,0,W,H);drawBg();drawStars();requestAnimationFrame(idleLoop);}}
requestAnimationFrame(idleLoop);
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}});
</script>
</body></html>"""


# ── HTML dispatcher ────────────────────────────────────────────────────────────
def get_html(theme, name, date_str):
    m = theme["mechanic"]
    if m == "tree":    return html_tree(theme, name, date_str)
    if m == "letter":  return html_letter(theme, name, date_str)
    return html_gather(theme, name, date_str)


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

    mech_label = {"tree": "🌸 Growing Tree", "letter": "💌 Envelope Letter", "gather": "✨ Particle Gather"}

    print(f"\n{'='*60}")
    print(f"  💗  Daily Love Page — {HER_NAME}")
    print(f"  📅  {date_str}")
    print(f"  🎨  Theme   : {theme['name']} ({theme['mood']})")
    print(f"  📖  Story   : {mech_label.get(theme['mechanic'], theme['mechanic'])}")
    print(f"  ➡️   Tomorrow: {next_theme['name']} ({next_theme['mood']})")
    print(f"{'='*60}\n")

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
