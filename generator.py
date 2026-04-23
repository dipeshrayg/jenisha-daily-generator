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
# ==============================================================================
# STORY ANIMATIONS (slots 1-12) -- v6.0: 12 original concepts, each unique
# Every slot is a completely different TYPE of experience.
# ==============================================================================
def html_galaxy(name, date_str):
    """LIVE CODE EDITOR — JavaScript types itself; the code IS the love note."""
    msg = "I keep building things\njust to have a reason.\n\nThis one was for you."
    code = ('const YOU = "' + name + '";\n'
            'const ME = "Dipesh";\n'
            'const REASON = Infinity;\n\n'
            '// this runs first every morning\n'
            'function firstThought() {\n'
            '  return YOU; // reliable\n'
            '}\n\n'
            '// warning: no exit condition\n'
            "// I don't plan to add one\n"
            'setInterval(() => {\n'
            '  thinkAbout(YOU);\n'
            '}, 1000);\n\n'
            '// always returns true\n'
            'function isItAGoodDay() {\n'
            '  return YOU !== undefined;\n'
            '}\n\n'
            "/* I don't know exactly when\n"
            '   this started. But it\n'
            '   compiles clean. Keeping it. */\n\n'
            'console.log("made this for " + YOU);')
    cj = json.dumps(code)
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const CODE={cj};const NAME={nj};const DATE={dj};'
          'const KWS=["const ","let ","function ","return ","setInterval","console.log","Infinity"];'
          'let ci=0,inStr=false,strCh="",inCom=false,comMl=false;'
          'const out=document.getElementById("out"),cur=document.getElementById("cur");'
          'function apd(txt,cls){'
          '  const last=out.lastChild;'
          '  if(last&&last.nodeType===1&&last.className===(cls||"")&&cls!==undefined){last.textContent+=txt;return;}'
          '  const s=document.createElement("span");if(cls)s.className=cls;s.textContent=txt;out.appendChild(s);}'
          'function tp(){'
          '  if(ci>=CODE.length){out.appendChild(cur);setTimeout(showFin,2400);return;}'
          '  const c=CODE[ci],sl=CODE.slice(ci);'
          '  if(c==="\\n"){out.appendChild(document.createElement("br"));if(!comMl)inCom=false;ci++;out.appendChild(cur);out.scrollTop=out.scrollHeight;setTimeout(tp,130+Math.random()*70);return;}'
          '  if(inCom||comMl){'
          '    if(comMl&&sl.startsWith("*/")){apd("*/","com");inCom=false;comMl=false;ci+=2;}'
          '    else{apd(c,"com");ci++;}}'
          '  else if(inStr){apd(c,"str");if(c===strCh&&CODE[ci-1]!=="\\\\")inStr=false;ci++;}'
          '  else if(sl.startsWith("//")){apd("//","com");inCom=true;ci+=2;}'
          '  else if(sl.startsWith("/*")){apd("/*","com");comMl=true;ci+=2;}'
          '  else if(c===\'"\'){inStr=true;strCh=c;apd(c,"str");ci++;}'
          '  else{'
          '    let hit=false;'
          '    for(const kw of KWS){if(sl.startsWith(kw)){apd(kw,"kw");ci+=kw.length;hit=true;break;}}'
          '    if(!hit){apd(c,"");ci++;}}'
          '  out.appendChild(cur);out.scrollTop=out.scrollHeight;'
          '  setTimeout(tp,15+Math.random()*13+(c===","||c===";"?28:0));}'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},46);}'
          'tp();')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>for_{name.lower()}.js</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#0d1117;overflow:hidden;font-family:"Fira Code","Courier New",monospace}}'
            f'#ed{{position:fixed;inset:0;display:flex;flex-direction:column}}'
            f'#tb{{background:#161b22;padding:10px 16px;display:flex;align-items:center;gap:8px;flex-shrink:0;border-bottom:1px solid #21262d}}'
            f'.dot{{width:12px;height:12px;border-radius:50%}}.d1{{background:#ff5f56}}.d2{{background:#ffbd2e}}.d3{{background:#27c93f}}'
            f'.fn{{color:#484f58;font-size:.82rem;margin-left:8px}}'
            f'#area{{flex:1;padding:20px;overflow-y:auto;font-size:clamp(.75rem,2.2vw,.95rem);line-height:2;color:#e6edf3}}'
            f'.kw{{color:#c084fc}}.str{{color:#86efac}}.com{{color:#484f58;font-style:italic}}'
            f'#cur{{display:inline-block;width:2px;height:1em;background:#c084fc;vertical-align:middle;animation:blink 1s step-end infinite}}'
            f'@keyframes blink{{50%{{opacity:0}}}}'
            f'#fin{{position:fixed;inset:0;background:rgba(13,17,23,.97);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 1.2s;padding:24px;text-align:center}}'
            f'#fin.show{{opacity:1;pointer-events:all}}'
            f'.ft{{font-family:"Dancing Script",cursive;font-size:clamp(2rem,8vw,3rem);color:#c084fc;margin-bottom:18px}}'
            f'.fm{{font-family:"Courier New",monospace;font-size:clamp(.95rem,3vw,1.25rem);color:#86efac;line-height:1.9;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.7rem;color:#c084fc;margin-top:18px}}'
            f'.fd{{font-size:.7rem;color:rgba(192,132,252,.28);margin-top:3px;letter-spacing:.08em}}</style></head><body>'
            f'<div id="ed"><div id="tb"><div class="dot d1"></div><div class="dot d2"></div><div class="dot d3"></div>'
            f'<span class="fn">for_{name.lower()}.js</span></div>'
            f'<div id="area"><span id="out"></span><span id="cur"></span></div></div>'
            f'<div id="fin"><div class="ft">{name}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_sakura(name, date_str):
    """RUNAWAY BUTTON — 'Will you be mine?' NO button runs away; YES triggers hearts."""
    msg = "Wasn't going to give you\nthe option anyway.\n\nJust wanted you to know."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'let tries=0;'
          'const noBtn=document.getElementById("no"),yesBtn=document.getElementById("yes");'
          'const W=window.innerWidth,H=window.innerHeight;'
          'let nx=W/2+120,ny=H/2;'
          'function moveNo(cx,cy){'
          '  const dx=nx-cx,dy=ny-cy,dist=Math.sqrt(dx*dx+dy*dy);'
          '  if(dist>160)return;'
          '  const esc=180/Math.max(dist,1);'
          '  nx=Math.max(60,Math.min(W-60,nx+dx/dist*esc));'
          '  ny=Math.max(60,Math.min(H-60,ny+dy/dist*esc));'
          '  noBtn.style.left=nx+"px";noBtn.style.top=ny+"px";'
          '  tries++;'
          '  if(tries===4){noBtn.style.opacity="0";noBtn.style.pointerEvents="none";'
          '    document.getElementById("hint").textContent="(gave up running)";}'
          '}'
          'document.addEventListener("mousemove",e=>moveNo(e.clientX,e.clientY));'
          'document.addEventListener("touchmove",e=>{e.preventDefault();moveNo(e.touches[0].clientX,e.touches[0].clientY);},{passive:false});'
          'yesBtn.addEventListener("click",sayYes);'
          'function sayYes(){'
          '  document.getElementById("question").style.display="none";'
          '  document.getElementById("btns").style.display="none";'
          '  document.getElementById("hint").style.display="none";'
          '  const cv=document.getElementById("c");cv.style.display="block";'
          '  const ctx=cv.getContext("2d");'
          '  cv.width=window.innerWidth;cv.height=window.innerHeight;'
          '  const parts=[];'
          '  for(let i=0;i<80;i++){parts.push({x:W/2,y:H/2,vx:(Math.random()-.5)*16,vy:-3-Math.random()*12,a:1,col:`hsl(${330+Math.random()*40},90%,${65+Math.random()*15}%)`});}'
          '  function draw(){'
          '    ctx.clearRect(0,0,cv.width,cv.height);'
          '    parts.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=.35;p.a-=.018;'
          '      if(p.a<=0)return;'
          '      ctx.save();ctx.globalAlpha=p.a;ctx.translate(p.x,p.y);ctx.scale(.9,.9);'
          '      ctx.beginPath();ctx.moveTo(0,-4);ctx.bezierCurveTo(0,-11,12,-11,12,-4);ctx.bezierCurveTo(12,3,0,12,0,16);ctx.bezierCurveTo(0,12,-12,3,-12,-4);ctx.bezierCurveTo(-12,-11,0,-11,0,-4);'
          '      ctx.fillStyle=p.col;ctx.fill();ctx.restore();});'
          '    if(parts.some(p=>p.a>0))requestAnimationFrame(draw);'
          '    else showFin();}'
          '  draw();}'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},46);}'
          'noBtn.style.left=nx+"px";noBtn.style.top=ny+"px";')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#fdf6ff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:"Caveat",cursive;overflow:hidden}}'
            f'#question{{font-family:"Dancing Script",cursive;font-size:clamp(2.2rem,9vw,3.5rem);color:#1a0030;text-align:center;margin-bottom:40px}}'
            f'#btns{{display:flex;gap:32px;align-items:center}}'
            f'#yes{{background:#c084fc;color:#fff;border:none;padding:14px 36px;border-radius:30px;font-family:"Caveat",cursive;font-size:1.5rem;cursor:pointer;box-shadow:0 6px 30px rgba(192,132,252,.4);transition:transform .15s}}'
            f'#yes:hover{{transform:scale(1.06)}}'
            f'#no{{position:fixed;background:rgba(0,0,0,.06);color:#999;border:1.5px solid #ddd;padding:12px 28px;border-radius:30px;font-family:"Caveat",cursive;font-size:1.4rem;cursor:pointer;transition:opacity .5s}}'
            f'#hint{{position:fixed;bottom:40px;left:50%;transform:translateX(-50%);color:rgba(0,0,0,.25);font-size:.95rem;letter-spacing:.1em}}'
            f'#c{{display:none;position:fixed;inset:0;pointer-events:none}}'
            f'#fin{{position:fixed;inset:0;background:rgba(253,246,255,.97);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 1.2s;padding:24px;text-align:center}}'
            f'#fin.show{{opacity:1;pointer-events:all}}'
            f'.ft{{font-family:"Dancing Script",cursive;font-size:clamp(2rem,9vw,3rem);color:#c084fc;margin-bottom:20px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.1rem,3.5vw,1.5rem);color:#3a0060;line-height:1.88;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.7rem;color:#c084fc;margin-top:18px}}'
            f'.fd{{font-size:.7rem;color:rgba(192,132,252,.4);margin-top:3px;letter-spacing:.08em}}</style></head><body>'
            f'<div id="question">Will you be mine?</div>'
            f'<div id="btns"><button id="yes">Yes 💗</button></div>'
            f'<button id="no">No</button>'
            f'<div id="hint">try clicking no</div>'
            f'<canvas id="c"></canvas>'
            f'<div id="fin"><div class="ft">{name}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_ocean(name, date_str):
    """TEXT ART HEART — 'i like you' repeated text forms a heart outline; click to scatter & reform."""
    msg = "You keep showing up in my thoughts.\nI stopped fighting it a while ago."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    phrases = json.dumps(["i like you", name.lower(), "a lot", "really", "quite a bit", "yes you", "just you"])
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          f'const PH={phrases};'
          'const cv=document.getElementById("c"),ctx=cv.getContext("2d");'
          'let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;'
          'const CX=W/2,CY=H*.44,SC=Math.min(W*.018,H*.015);'
          'function heartPt(t){const x=16*Math.pow(Math.sin(t),3),y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));return{x:CX+x*SC,y:CY+y*SC};}'
          'const N=120;const particles=[];'
          'for(let i=0;i<N;i++){'
          '  const t=(i/N)*Math.PI*2,hp=heartPt(t);'
          '  const txt=PH[i%PH.length];'
          '  particles.push({tx:hp.x,ty:hp.y,x:Math.random()*W,y:Math.random()*H,'
          '    vx:0,vy:0,txt,alpha:0,scattered:false,hue:330+Math.random()*40});}'
          'let scattered=false,scatterT=0;'
          'cv.addEventListener("click",()=>{if(scattered){particles.forEach(p=>{p.tx=p.homeX;p.ty=p.homeY;p.scattered=false;});scattered=false;}else{particles.forEach(p=>{p.homeX=p.tx;p.homeY=p.ty;const ang=Math.random()*Math.PI*2,r=50+Math.random()*200;p.tx=CX+Math.cos(ang)*r;p.ty=CY+Math.sin(ang)*r;p.scattered=true;});scattered=true;}});'
          'cv.addEventListener("touchend",e=>{e.preventDefault();cv.dispatchEvent(new Event("click"));},{passive:false});'
          'let t=0,msgShown=false;'
          'function loop(){'
          '  t+=.016;'
          '  ctx.fillStyle="rgba(5,0,14,.18)";ctx.fillRect(0,0,W,H);'
          '  particles.forEach((p,i)=>{'
          '    p.alpha=Math.min(1,p.alpha+.018);'
          '    const dx=p.tx-p.x,dy=p.ty-p.y;'
          '    p.x+=dx*.08;p.y+=dy*.08;'
          '    const glow=.5+.5*Math.sin(t*2+i*.3);'
          '    ctx.save();ctx.globalAlpha=p.alpha*(.55+glow*.35);'
          '    ctx.font=`${Math.floor(9+Math.random()*.5)}px "Caveat",cursive`;'
          '    ctx.fillStyle=`hsl(${p.hue},85%,${70+glow*15}%)`;'
          '    ctx.shadowColor=`hsl(${p.hue},85%,75%)`;ctx.shadowBlur=6*glow;'
          '    ctx.fillText(p.txt,p.x,p.y);ctx.restore();});'
          '  if(!msgShown&&t>6){msgShown=true;showFin();}'
          '  requestAnimationFrame(loop);}'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},50);}'
          'loop();')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#05000e;overflow:hidden}}'
            f'#hint{{position:fixed;bottom:28px;left:50%;transform:translateX(-50%);font-family:"Caveat",cursive;font-size:.9rem;color:rgba(255,160,220,.3);letter-spacing:.12em;animation:bl 2.5s infinite}}'
            f'@keyframes bl{{0%,100%{{opacity:.25}}50%{{opacity:.7}}}}'
            f'#fin{{position:fixed;bottom:-200px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(10,0,20,.95);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(192,132,252,.15);transition:bottom 1.2s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.8rem;color:rgba(192,132,252,.45);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.1rem,3.5vw,1.4rem);color:#e9d5ff;line-height:1.82;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#c084fc;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(192,132,252,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<canvas id="c"></canvas>'
            f'<div id="hint">tap to scatter</div>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_firefly(name, date_str):
    """LIVE TIMER — Today's elapsed time live-ticking; she's been on his mind for most of it."""
    msg = "Every one of those seconds.\nYou were somewhere in my head\nfor most of them."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'function fmt(n){return String(n).padStart(2,"0");}'
          'function tick(){'
          '  const now=new Date(),mn=now.getHours()*3600+now.getMinutes()*60+now.getSeconds();'
          '  const h=Math.floor(mn/3600),m=Math.floor((mn%3600)/60),s=mn%60;'
          '  document.getElementById("timer").textContent=fmt(h)+":"+fmt(m)+":"+fmt(s);'
          '  setTimeout(tick,1000);}'
          'tick();'
          'setTimeout(()=>{'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const me=document.getElementById("fm");me.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}me.textContent+=MSG[j++];},52);},'
          '5200);')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#020810;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:"Caveat",cursive;overflow:hidden}}'
            f'.lbl{{font-size:clamp(.85rem,3vw,1.1rem);color:rgba(56,189,248,.45);letter-spacing:.2em;text-transform:uppercase;margin-bottom:18px}}'
            f'#timer{{font-family:"Courier New",monospace;font-size:clamp(3.5rem,16vw,8rem);color:#38bdf8;text-shadow:0 0 60px rgba(56,189,248,.5),0 0 120px rgba(56,189,248,.2);letter-spacing:.04em;line-height:1}}'
            f'.sub{{font-family:"Caveat",cursive;font-size:clamp(1rem,3.5vw,1.4rem);color:rgba(56,189,248,.38);margin-top:22px;letter-spacing:.08em;text-align:center;padding:0 20px}}'
            f'.name-tag{{font-family:"Dancing Script",cursive;font-size:clamp(2rem,8vw,3rem);color:#38bdf8;margin-bottom:8px;text-shadow:0 0 40px rgba(56,189,248,.4)}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(2,8,16,.97);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(56,189,248,.15);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(56,189,248,.4);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.1rem,3.5vw,1.4rem);color:#e0f2fe;line-height:1.82;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#38bdf8;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(56,189,248,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<div class="name-tag">{name}</div>'
            f'<div class="lbl">today has lasted</div>'
            f'<div id="timer">00:00:00</div>'
            f'<div class="sub">you\'ve been on my mind\nfor most of it.</div>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_neon(name, date_str):
    """GEODE CRACK — Dark stone; tap 3× to crack it open; glowing crystals + message inside."""
    msg = "Most things that look plain on the outside\nare worth cracking open.\n\nYou taught me that."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'const cv=document.getElementById("c"),ctx=cv.getContext("2d");'
          'let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;'
          'const CX=W/2,CY=H*.44;const R=Math.min(W,H)*.28;'
          'let stage=0,glowT=0,animating=false;'
          'const CRACKS=[['
          '  [{x:.0,y:-.3},{x:-.25,y:-.1},{x:-.4,y:.2}],'
          '  [{x:.1,y:-.35},{x:.3,y:0},{x:.45,y:.15}],'
          '  [{x:-.1,y:.38},{x:.1,y:.25},{x:.3,y:.42}]'
          '],['
          '  [{x:-.2,y:-.4},{x:-.45,y:-.2},{x:-.5,y:.1}],'
          '  [{x:.2,y:-.38},{x:.48,y:-.1},{x:.52,y:.22}],'
          '  [{x:-.35,y:.3},{x:0,y:.48},{x:.38,y:.35}],'
          '  [{x:-.15,y:-.05},{x:.05,y:.2}]'
          '],['
          '  [{x:0,y:-.5},{x:-.3,y:-.4},{x:-.55,y:0},{x:-.5,y:.3}],'
          '  [{x:.05,y:-.48},{x:.38,y:-.3},{x:.55,y:.05},{x:.48,y:.35}],'
          '  [{x:-.48,y:.2},{x:-.2,y:.52},{x:.15,y:.5},{x:.45,y:.28}]'
          ']];'
          'const CRYSTALS=Array.from({length:22},(_,i)=>{'
          '  const a=(i/22)*Math.PI*2,r=R*(0.3+Math.random()*.55);'
          '  return{x:CX+Math.cos(a)*r,y:CY+Math.sin(a)*r,h:8+Math.random()*22,hue:180+Math.random()*80,a:0};});'
          'function drawStone(stage){'
          '  const gr=ctx.createRadialGradient(CX-R*.15,CY-R*.2,0,CX,CY,R);'
          '  if(stage<2){gr.addColorStop(0,"#3a3540");gr.addColorStop(1,"#1a1520");}'
          '  else{gr.addColorStop(0,"#4a3560");gr.addColorStop(.5,"#2a1a40");gr.addColorStop(1,"#180d28");}'
          '  ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);ctx.fillStyle=gr;ctx.fill();'
          '  ctx.strokeStyle="rgba(255,255,255,.08)";ctx.lineWidth=2;ctx.stroke();}'
          'function drawCracks(upTo){'
          '  for(let s=0;s<upTo&&s<CRACKS.length;s++){'
          '    CRACKS[s].forEach(crack=>{'
          '      if(crack.length<2)return;'
          '      ctx.beginPath();ctx.moveTo(CX+crack[0].x*R,CY+crack[0].y*R);'
          '      for(let i=1;i<crack.length;i++)ctx.lineTo(CX+crack[i].x*R,CY+crack[i].y*R);'
          '      ctx.strokeStyle=`rgba(${s===upTo-1?"180,140,255":"120,80,200"},${s===upTo-1?.9:.6})`;'
          '      ctx.lineWidth=s===upTo-1?2.5:1.5;ctx.stroke();});}}'
          'function drawCrystals(alpha){'
          '  CRYSTALS.forEach(c=>{'
          '    c.a=Math.min(1,c.a+.02);'
          '    const ga=c.a*alpha;if(ga<=0)return;'
          '    ctx.save();ctx.globalAlpha=ga;'
          '    ctx.translate(c.x,c.y);ctx.rotate(Math.PI*.15);'
          '    ctx.beginPath();ctx.moveTo(0,-c.h*.6);ctx.lineTo(c.h*.22,0);ctx.lineTo(0,c.h*.4);ctx.lineTo(-c.h*.22,0);ctx.closePath();'
          '    const cg=ctx.createLinearGradient(0,-c.h*.6,0,c.h*.4);'
          '    cg.addColorStop(0,`hsla(${c.hue},90%,85%,${ga})`);cg.addColorStop(1,`hsla(${c.hue},80%,55%,${ga*.6})`);'
          '    ctx.fillStyle=cg;ctx.shadowColor=`hsl(${c.hue},90%,75%)`;ctx.shadowBlur=12;ctx.fill();'
          '    ctx.restore();});}'
          'function drawGlow(alpha){'
          '  const gr=ctx.createRadialGradient(CX,CY,0,CX,CY,R*.8);'
          '  gr.addColorStop(0,`rgba(180,100,255,${alpha*.35})`);'
          '  gr.addColorStop(1,"rgba(0,0,0,0)");'
          '  ctx.fillStyle=gr;ctx.fillRect(0,0,W,H);}'
          'function drawHint(){'
          '  ctx.fillStyle="rgba(255,255,255,.35)";ctx.font=\'16px "Caveat",cursive\';ctx.textAlign="center";'
          '  ctx.fillText(`tap to crack (${stage}/3)`,CX,H*.82);}'
          'function render(){'
          '  ctx.fillStyle="#0d0a14";ctx.fillRect(0,0,W,H);'
          '  if(stage<3){'
          '    drawStone(stage);drawCracks(stage);'
          '    if(stage<3)drawHint();}'
          '  else{'
          '    glowT=Math.min(1,glowT+.015);'
          '    drawGlow(glowT);drawStone(3);drawCracks(3);drawCrystals(glowT);'
          '    if(glowT>=1&&!document.getElementById("fin").classList.contains("show")){showFin();}}'
          '  requestAnimationFrame(render);}'
          'cv.addEventListener("click",()=>{'
          '  if(stage>=3)return;stage++;'
          '  if(stage===3){document.getElementById("tap-hint").style.display="none";}});'
          'cv.addEventListener("touchend",e=>{e.preventDefault();cv.dispatchEvent(new Event("click"));},{passive:false});'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},50);}'
          'render();'
          'window.addEventListener("resize",()=>{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;});')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#0d0a14;overflow:hidden}}'
            f'#tap-hint{{position:fixed;top:24px;left:50%;transform:translateX(-50%);font-family:"Caveat",cursive;font-size:.9rem;color:rgba(180,140,255,.4);letter-spacing:.14em;animation:bl 2.5s infinite}}'
            f'@keyframes bl{{0%,100%{{opacity:.3}}50%{{opacity:.8}}}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(13,10,20,.97);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(180,100,255,.2);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(180,100,255,.4);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.05rem,3.5vw,1.35rem);color:#e9d5ff;line-height:1.85;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#c084fc;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(180,100,255,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<canvas id="c"></canvas>'
            f'<div id="tap-hint">tap to crack open</div>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_aurora(name, date_str):
    """CSS 3D HEARTS — Multiple hearts floating at different depths; mouse/touch tilts the scene."""
    msg = "There are too many reasons\nto count anymore.\n\nSo I stopped counting."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    heart_data = json.dumps([
        {"z": -300, "x": -35, "y": -20, "s": 1.8, "h": 340, "sp": 8},
        {"z": -180, "x": 40,  "y": -40, "s": 1.2, "h": 355, "sp": 11},
        {"z": -80,  "x": -55, "y": 30,  "s": 1.0, "h": 325, "sp": 7},
        {"z": 0,    "x": 10,  "y": -10, "s": 2.4, "h": 345, "sp": 6},
        {"z": 80,   "x": -30, "y": 50,  "s": 0.9, "h": 335, "sp": 13},
        {"z": 160,  "x": 60,  "y": 20,  "s": 1.5, "h": 350, "sp": 9},
        {"z": 250,  "x": -10, "y": -55, "s": 1.1, "h": 320, "sp": 10},
        {"z": -220, "x": 55,  "y": 45,  "s": 0.8, "h": 360, "sp": 14},
        {"z": 120,  "x": -60, "y": -30, "s": 1.3, "h": 330, "sp": 8},
    ])
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          f'const HD={heart_data};'
          'const scene=document.getElementById("scene");'
          'const hearts=HD.map((d,i)=>{'
          '  const el=document.createElement("div");el.className="heart";'
          '  el.innerHTML=`<div class="hh"></div>`;'
          '  el.style.cssText=`transform:translateZ(${d.z}px) translateX(${d.x}px) translateY(${d.y}px);`+'
          '    `animation:float${i%3} ${d.sp}s ease-in-out infinite;filter:hue-rotate(${d.h-340}deg);font-size:${d.s*2.5}rem;`;'
          '  scene.appendChild(el);return el;});'
          'let tx=0,ty=0,cx=0,cy=0;'
          'document.addEventListener("mousemove",e=>{tx=(e.clientX/window.innerWidth-.5)*25;ty=(e.clientY/window.innerHeight-.5)*-18;});'
          'document.addEventListener("touchmove",e=>{e.preventDefault();tx=(e.touches[0].clientX/window.innerWidth-.5)*25;ty=(e.touches[0].clientY/window.innerHeight-.5)*-18;},{passive:false});'
          'function tilt(){'
          '  cx+=(tx-cx)*.06;cy+=(ty-cy)*.06;'
          '  scene.style.transform=`rotateX(${cy}deg) rotateY(${cx}deg)`;'
          '  requestAnimationFrame(tilt);}'
          'tilt();'
          'setTimeout(()=>{'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},50);},'
          '4500);')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#0a0010;overflow:hidden;display:flex;align-items:center;justify-content:center}}'
            f'#wrap{{width:100%;height:100%;perspective:600px;display:flex;align-items:center;justify-content:center}}'
            f'#scene{{transform-style:preserve-3d;width:200px;height:200px;position:relative;transition:transform .1s}}'
            f'.heart{{position:absolute;top:50%;left:50%;transform-origin:center;color:rgba(255,80,150,1);text-shadow:0 0 20px rgba(255,80,150,.7),0 0 60px rgba(255,80,150,.3);line-height:1}}'
            f'.hh::before{{content:"♥";font-size:1em}}'
            f'@keyframes float0{{0%,100%{{transform:translateY(0px)}}50%{{transform:translateY(-18px)}}}}'
            f'@keyframes float1{{0%,100%{{transform:translateY(-10px)}}50%{{transform:translateY(12px)}}}}'
            f'@keyframes float2{{0%,100%{{transform:translateY(8px)}}50%{{transform:translateY(-14px)}}}}'
            f'.name{{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);font-family:"Dancing Script",cursive;font-size:clamp(2rem,10vw,4rem);color:rgba(255,100,160,.15);letter-spacing:.2em;pointer-events:none;white-space:nowrap}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(10,0,16,.97);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(255,80,150,.15);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(255,100,160,.4);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.05rem,3.5vw,1.35rem);color:#ffe4ef;line-height:1.85;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#ff6096;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(255,100,160,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<div id="wrap"><div id="scene"></div></div>'
            f'<div class="name">{name}</div>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_sunrise(name, date_str):
    """CANVAS PEN HANDWRITING — Ink pen draws message in cursive on canvas."""
    msg = "Wrote it by hand\nbecause typing felt too easy."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'const cv=document.getElementById("c"),ctx=cv.getContext("2d");'
          'let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;'
          'const lines=["for "+NAME+",","","I like you.","A lot, actually.","","More than I let on.","","— Dipesh"];'
          'const lh=Math.min(H*.1,52),startY=H*.2;'
          'ctx.fillStyle="#fdf8f2";ctx.fillRect(0,0,W,H);'
          'for(let i=0;i<H;i+=22){ctx.strokeStyle=`rgba(180,160,140,${i%88===0?.18:.07})`;ctx.beginPath();ctx.moveTo(0,i);ctx.lineTo(W,i);ctx.stroke();}'
          'let li=0,charI=0,x=W*.08,y=startY,inkTrail=[];'
          'function drawInk(){'
          '  if(li>=lines.length){setTimeout(showFin,800);return;}'
          '  const line=lines[li];'
          '  if(charI>=line.length){li++;charI=0;x=W*.08;y+=lh;if(li<lines.length)setTimeout(drawInk,320);else setTimeout(drawInk,320);return;}'
          '  const c=line[charI];charI++;'
          '  const fs=li===0?Math.min(W*.052,28):li===7?Math.min(W*.06,32):Math.min(W*.065,36);'
          '  ctx.font=`italic ${fs}px "Dancing Script",cursive`;'
          '  ctx.fillStyle=li===7?"#c84060":"#1a1008";'
          '  ctx.globalAlpha=li===7?.8:1;'
          '  ctx.fillText(c,x,y);'
          '  x+=ctx.measureText(c).width;'
          '  ctx.globalAlpha=1;'
          '  // Ink blot effect'
          '  if(Math.random()<.07){'
          '    ctx.beginPath();ctx.arc(x-2,y+1,1+Math.random()*2,0,Math.PI*2);'
          '    ctx.fillStyle="rgba(26,16,8,.25)";ctx.fill();}'
          '  setTimeout(drawInk,55+Math.random()*40+(c===" "?80:0));}'
          'drawInk();'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},60);}')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#fdf8f2;overflow:hidden}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(253,248,242,.98);border-radius:3px;padding:24px 26px 20px;border:1px solid rgba(180,140,100,.3);box-shadow:0 8px 40px rgba(0,0,0,.15);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(140,100,60,.45);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Dancing Script",cursive;font-size:clamp(1.1rem,3.5vw,1.4rem);color:#3a1a08;line-height:1.85;white-space:pre-wrap;font-style:italic}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#c84060;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(140,100,60,.3);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<canvas id="c"></canvas>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_rain(name, date_str):
    """ORBIT NAME — Particles travel in orbits that collectively trace her name; hypnotic."""
    msg = "You've been circling in my head like this.\nConstantly.\n\nI'm fine with it."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'const cv=document.getElementById("c"),ctx=cv.getContext("2d");'
          'let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;'
          # Render name to offscreen canvas, sample points
          'const OCV=document.createElement("canvas"),OCTX=OCV.getContext("2d");'
          'OCV.width=W;OCV.height=H;'
          'const fs=Math.min(W*.15,H*.18,80);'
          'OCTX.font=`900 ${fs}px "Dancing Script",cursive`;'
          'OCTX.textAlign="center";OCTX.textBaseline="middle";'
          'OCTX.fillStyle="#fff";OCTX.fillText(NAME,W/2,H/2);'
          'const imgd=OCTX.getImageData(0,0,W,H).data;'
          'const pts=[];'
          'for(let y=0;y<H;y+=4){for(let x=0;x<W;x+=4){'
          '  const idx=(y*W+x)*4;'
          '  if(imgd[idx+3]>80)pts.push({x,y});}}'
          # Sample ~200 points
          'const step=Math.max(1,Math.floor(pts.length/200));'
          'const targets=pts.filter((_,i)=>i%step===0).slice(0,200);'
          'const particles=targets.map(t=>({'
          '  tx:t.x,ty:t.y,'
          '  x:W/2+(Math.random()-.5)*W,'
          '  y:H/2+(Math.random()-.5)*H,'
          '  angle:Math.random()*Math.PI*2,'
          '  radius:20+Math.random()*60,'
          '  speed:.4+Math.random()*.8,'
          '  hue:300+Math.random()*80,size:1.5+Math.random()*1.5,alpha:0}));'
          'let t=0,msgShown=false,converged=false;'
          'function loop(){'
          '  t+=.016;'
          '  ctx.fillStyle="rgba(5,0,16,.15)";ctx.fillRect(0,0,W,H);'
          '  const conv=t>3;'
          '  particles.forEach((p,i)=>{'
          '    p.alpha=Math.min(1,p.alpha+.015);'
          '    p.angle+=p.speed*.025;'
          '    if(conv){'
          '      p.x+=(p.tx-p.x)*.04+Math.cos(p.angle)*0.8;'
          '      p.y+=(p.ty-p.y)*.04+Math.sin(p.angle)*0.8;}'
          '    else{'
          '      p.x+=Math.cos(p.angle)*p.speed;'
          '      p.y+=Math.sin(p.angle)*p.speed;'
          '      if(p.x<0||p.x>W)p.x=W/2+(Math.random()-.5)*50;'
          '      if(p.y<0||p.y>H)p.y=H/2+(Math.random()-.5)*50;}'
          '    const glow=.5+.5*Math.sin(t*3+i*.2);'
          '    ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);'
          '    ctx.fillStyle=`hsla(${p.hue},90%,${70+glow*20}%,${p.alpha})`;'
          '    ctx.shadowColor=`hsl(${p.hue},90%,70%)`;ctx.shadowBlur=6;'
          '    ctx.fill();ctx.shadowBlur=0;});'
          '  if(!msgShown&&t>7){msgShown=true;showFin();}'
          '  requestAnimationFrame(loop);}'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},50);}'
          'loop();'
          'window.addEventListener("resize",()=>{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;});')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#050010;overflow:hidden}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(5,0,16,.97);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(200,100,255,.15);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(200,100,255,.4);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.05rem,3.5vw,1.35rem);color:#f0d0ff;line-height:1.85;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#c084fc;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(200,100,255,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<canvas id="c"></canvas>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_particle(name, date_str):
    """GIFT BOX UNWRAP — Click ribbon, click lid, box opens, glow + message inside."""
    msg = "No occasion.\nNo reason.\n\nJust felt like it."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'let stage=0;'
          'function next(){'
          '  if(stage===0){stage=1;document.getElementById("ribbon").classList.add("untie");document.getElementById("bow").classList.add("fade");document.getElementById("tap-label").textContent="tap to open";}'
          '  else if(stage===1){stage=2;document.getElementById("lid").classList.add("open");document.getElementById("tap-label").textContent="";setTimeout(()=>{document.getElementById("glow").classList.add("show");setTimeout(showFin,800);},600);}'
          '}'
          'document.getElementById("box").addEventListener("click",next);'
          'document.getElementById("box").addEventListener("touchend",e=>{e.preventDefault();next();},{passive:false});'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},48);}')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#1a0810;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden}}'
            f'.name-tag{{font-family:"Dancing Script",cursive;font-size:clamp(1.5rem,6vw,2.2rem);color:rgba(255,120,140,.5);margin-bottom:32px;letter-spacing:.08em}}'
            f'#box{{position:relative;width:min(220px,55vw);height:min(200px,50vw);cursor:pointer;user-select:none}}'
            f'.box-body{{position:absolute;bottom:0;left:0;right:0;height:72%;background:linear-gradient(135deg,#c2185b,#880e4f);border-radius:4px;box-shadow:0 12px 40px rgba(0,0,0,.5);overflow:hidden}}'
            f'.box-body::after{{content:"";position:absolute;left:50%;top:0;bottom:0;width:12px;background:rgba(255,255,255,.15);transform:translateX(-50%)}}'
            f'.box-lid{{position:absolute;top:0;left:-5%;right:-5%;height:32%;background:linear-gradient(135deg,#e91e63,#ad1457);border-radius:4px;box-shadow:0 4px 20px rgba(0,0,0,.4);transform-origin:center bottom;transition:transform .8s cubic-bezier(.4,0,.2,1)}}'
            f'.box-lid.open{{transform:rotateX(-115deg)}}'
            f'#ribbon{{position:absolute;left:50%;top:0;bottom:0;width:14px;background:linear-gradient(180deg,rgba(255,230,240,.9),rgba(255,180,200,.7));transform:translateX(-50%);transition:opacity .5s}}'
            f'#ribbon.untie{{opacity:0;transform:translateX(-50%) rotate(8deg)}}'
            f'#bow{{position:absolute;top:-10px;left:50%;transform:translateX(-50%);font-size:2.4rem;transition:opacity .4s,transform .5s}}'
            f'#bow.fade{{opacity:0;transform:translateX(-50%) translateY(-20px)}}'
            f'#glow{{position:absolute;top:10%;left:10%;right:10%;bottom:0;background:radial-gradient(ellipse at 50% 20%,rgba(255,200,220,.9),rgba(255,100,160,.4),transparent 70%);opacity:0;transition:opacity 1.2s;pointer-events:none;border-radius:50%}}'
            f'#glow.show{{opacity:1}}'
            f'#tap-label{{font-family:"Caveat",cursive;font-size:1rem;color:rgba(255,180,200,.5);letter-spacing:.12em;margin-top:24px;animation:bl 2s infinite}}'
            f'@keyframes bl{{0%,100%{{opacity:.35}}50%{{opacity:.85}}}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(26,8,16,.97);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(233,30,99,.2);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(233,30,99,.4);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.05rem,3.5vw,1.35rem);color:#fce4ec;line-height:1.85;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#e91e63;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(233,30,99,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<div class="name-tag">for {name.lower()}</div>'
            f'<div id="box">'
            f'  <div class="box-lid" id="lid"><div id="ribbon"></div></div>'
            f'  <div class="box-body"><div id="glow"></div></div>'
            f'  <div id="bow">🎀</div>'
            f'</div>'
            f'<div id="tap-label">tap to unwrap</div>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_matrix(name, date_str):
    """MOOD ORB — Glowing orb; hover/touch different zones shows feelings; click = message."""
    msg = "It's all of this at once.\nEvery time."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    moods = json.dumps([
        {"a": 0,    "l": "chaos"},
        {"a": 72,   "l": "warmth"},
        {"a": 144,  "l": "home"},
        {"a": 216,  "l": "distraction"},
        {"a": 288,  "l": "something good"},
    ])
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          f'const MOODS={moods};'
          'const cv=document.getElementById("c"),ctx=cv.getContext("2d");'
          'let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;'
          'const CX=W/2,CY=H*.44,R=Math.min(W,H)*.28;'
          'let hovered="",hue=330,pulsT=0,clicked=false;'
          'function getZone(x,y){'
          '  const dx=x-CX,dy=y-CY;'
          '  if(Math.sqrt(dx*dx+dy*dy)>R)return "";'
          '  const ang=(Math.atan2(dy,dx)*180/Math.PI+360)%360;'
          '  return MOODS.find((_,i)=>{'
          '    const next=MOODS[(i+1)%MOODS.length];'
          '    const a=MOODS[i].a,b=i===MOODS.length-1?360:next.a;'
          '    return ang>=a&&ang<b;}).l;}'
          'cv.addEventListener("mousemove",e=>{hovered=getZone(e.clientX,e.clientY);});'
          'cv.addEventListener("touchmove",e=>{e.preventDefault();hovered=getZone(e.touches[0].clientX,e.touches[0].clientY);},{passive:false});'
          'cv.addEventListener("click",e=>{if(getZone(e.clientX,e.clientY)){clicked=true;setTimeout(showFin,600);}});'
          'cv.addEventListener("touchend",e=>{e.preventDefault();if(hovered)clicked=true;setTimeout(showFin,600);});'
          'function loop(){'
          '  pulsT+=.02;'
          '  ctx.fillStyle="#08000f";ctx.fillRect(0,0,W,H);'
          '  const pulse=.5+.5*Math.sin(pulsT);'
          '  // Outer glow'
          '  const og=ctx.createRadialGradient(CX,CY,R*.5,CX,CY,R*1.8);'
          '  og.addColorStop(0,`rgba(180,50,255,${(.12+pulse*.08)*1})`);og.addColorStop(1,"rgba(0,0,0,0)");'
          '  ctx.fillStyle=og;ctx.fillRect(0,0,W,H);'
          '  // Orb body'
          '  const gr=ctx.createRadialGradient(CX-R*.2,CY-R*.25,0,CX,CY,R);'
          '  gr.addColorStop(0,`hsl(${290+pulse*20},70%,55%)`);'
          '  gr.addColorStop(.5,`hsl(${270+pulse*15},80%,35%)`);'
          '  gr.addColorStop(1,`hsl(${250},90%,15%)`);'
          '  ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);ctx.fillStyle=gr;ctx.fill();'
          '  // Zone dividers (subtle)'
          '  MOODS.forEach(m=>{const a=m.a*Math.PI/180;ctx.beginPath();ctx.moveTo(CX,CY);ctx.lineTo(CX+Math.cos(a)*R,CY+Math.sin(a)*R);ctx.strokeStyle="rgba(255,255,255,.05)";ctx.lineWidth=1;ctx.stroke();});'
          '  // Hover highlight'
          '  if(hovered){'
          '    const mi=MOODS.findIndex(m=>m.l===hovered);'
          '    const a1=MOODS[mi].a*Math.PI/180;'
          '    const a2=(mi===MOODS.length-1?360:MOODS[mi+1].a)*Math.PI/180;'
          '    ctx.beginPath();ctx.moveTo(CX,CY);ctx.arc(CX,CY,R,a1,a2);ctx.closePath();'
          '    ctx.fillStyle="rgba(255,255,255,.07)";ctx.fill();}'
          '  // Mood label'
          '  if(hovered){'
          '    ctx.save();ctx.font=`bold ${Math.min(W*.07,28)}px "Dancing Script",cursive`;'
          '    ctx.textAlign="center";ctx.textBaseline="middle";'
          '    ctx.fillStyle=`rgba(255,220,255,${.7+pulse*.3})`;'
          '    ctx.shadowColor="rgba(200,100,255,.8)";ctx.shadowBlur=20;'
          '    ctx.fillText(hovered,CX,CY);ctx.restore();}'
          '  else{'
          '    ctx.font=`${Math.min(W*.04,16)}px "Caveat",cursive`;'
          '    ctx.textAlign="center";ctx.textBaseline="middle";'
          '    ctx.fillStyle=`rgba(255,200,255,${.3+pulse*.2})`;'
          '    ctx.fillText("hover me",CX,CY);}'
          '  requestAnimationFrame(loop);}'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},56);}'
          'loop();window.addEventListener("resize",()=>{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;});')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#08000f;overflow:hidden}}'
            f'.nametag{{position:fixed;top:24px;left:50%;transform:translateX(-50%);font-family:"Dancing Script",cursive;font-size:clamp(1.4rem,5vw,2rem);color:rgba(200,100,255,.4);letter-spacing:.08em}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(8,0,15,.97);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(180,50,255,.2);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(180,50,255,.4);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.05rem,3.5vw,1.35rem);color:#f0d0ff;line-height:1.85;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#c084fc;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(180,50,255,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<canvas id="c"></canvas>'
            f'<div class="nametag">{name}</div>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_butterfly(name, date_str):
    """RIGGED LOCK — Guess the 'secret number'; after 3 tries it unlocks anyway."""
    msg = "I was going to make you work for it.\nChanged my mind.\n\nYou get it for free."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'let tries=0,unlocked=false;'
          'const inp=document.getElementById("inp"),fb=document.getElementById("fb");'
          'document.getElementById("guess-btn").addEventListener("click",guess);'
          'inp.addEventListener("keydown",e=>{if(e.key==="Enter")guess();});'
          'function guess(){'
          '  if(unlocked)return;'
          '  const val=inp.value.trim();'
          '  if(!val){fb.textContent="enter a number.";return;}'
          '  tries++;inp.value="";'
          '  if(tries<3){'
          '    const hints=["not quite. try again.","still no. one more try."];'
          '    fb.textContent=hints[tries-1];'
          '    fb.style.color="rgba(255,180,100,.7)";}'
          '  else{'
          '    unlocked=true;'
          '    fb.textContent="okay. I was going to make this harder.";'
          '    fb.style.color="rgba(100,255,180,.7)";'
          '    document.getElementById("lock-icon").textContent="🔓";'
          '    setTimeout(()=>{document.getElementById("lock-icon").style.animation="spin .6s ease";setTimeout(showFin,800);},800);}}'
          'function showFin(){'
          '  document.getElementById("puzzle").style.opacity="0";'
          '  document.getElementById("puzzle").style.transform="scale(.95)";'
          '  setTimeout(()=>{'
          '    const el=document.getElementById("fin");el.classList.add("show");'
          '    const m=document.getElementById("fm");m.textContent="";let j=0;'
          '    const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},50);},500);}')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#050c14;display:flex;align-items:center;justify-content:center;font-family:"Caveat",cursive;overflow:hidden}}'
            f'#puzzle{{transition:opacity .5s,transform .5s;text-align:center;padding:20px}}'
            f'#lock-icon{{font-size:clamp(3rem,14vw,5rem);margin-bottom:20px;display:block;animation:wobble 3s ease-in-out infinite}}'
            f'@keyframes wobble{{0%,100%{{transform:rotate(-5deg)}}50%{{transform:rotate(5deg)}}}}'
            f'@keyframes spin{{to{{transform:rotate(360deg)}}}}'
            f'.q{{font-family:"Dancing Script",cursive;font-size:clamp(1.4rem,5vw,2rem);color:#38bdf8;margin-bottom:8px}}'
            f'.hint{{font-size:.9rem;color:rgba(56,189,248,.35);letter-spacing:.08em;margin-bottom:28px}}'
            f'.input-row{{display:flex;gap:12px;justify-content:center;margin-bottom:18px}}'
            f'#inp{{background:rgba(56,189,248,.08);border:1.5px solid rgba(56,189,248,.25);border-radius:12px;padding:12px 18px;font-family:"Caveat",cursive;font-size:1.3rem;color:#e0f2fe;width:120px;text-align:center;outline:none}}'
            f'#inp:focus{{border-color:rgba(56,189,248,.6)}}'
            f'#guess-btn{{background:#38bdf8;border:none;border-radius:12px;padding:12px 22px;font-family:"Caveat",cursive;font-size:1.3rem;color:#000;cursor:pointer;transition:transform .15s}}'
            f'#guess-btn:active{{transform:scale(.96)}}'
            f'#fb{{font-size:1.05rem;color:rgba(255,180,100,.7);min-height:24px;transition:all .3s}}'
            f'#fin{{position:fixed;inset:0;background:rgba(5,12,20,.97);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 1.2s;padding:24px;text-align:center}}'
            f'#fin.show{{opacity:1;pointer-events:all}}'
            f'.ft{{font-family:"Dancing Script",cursive;font-size:clamp(2rem,8vw,3rem);color:#38bdf8;margin-bottom:18px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.1rem,3.5vw,1.45rem);color:#e0f2fe;line-height:1.88;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.7rem;color:#38bdf8;margin-top:18px}}'
            f'.fd{{font-size:.7rem;color:rgba(56,189,248,.28);margin-top:3px;letter-spacing:.08em}}</style></head><body>'
            f'<div id="puzzle">'
            f'  <span id="lock-icon">🔒</span>'
            f'  <div class="q">guess the number</div>'
            f'  <div class="hint">it has something to do with you. (1 – 100)</div>'
            f'  <div class="input-row"><input id="inp" type="number" min="1" max="100" placeholder="?"/><button id="guess-btn">guess</button></div>'
            f'  <div id="fb"></div>'
            f'</div>'
            f'<div id="fin"><div class="ft">{name}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


def html_campfire(name, date_str):
    """DARKROOM DEVELOP — Photo develops from black; heart emerges like a darkroom print."""
    msg = "Some things take time\nto come into focus.\n\nYou did."
    mj = json.dumps(msg)
    nj = json.dumps(name)
    dj = json.dumps(date_str)
    js = (f'const MSG={mj};const NAME={nj};const DATE={dj};'
          'const cv=document.getElementById("c"),ctx=cv.getContext("2d");'
          'let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;'
          'const CX=W/2,CY=H*.42,SC=Math.min(W*.024,H*.02);'
          'function heartPt(t){const x=16*Math.pow(Math.sin(t),3),y=-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));return{x:CX+x*SC,y:CY+y*SC};}'
          'let t=0,msgShown=false;'
          'function loop(){'
          '  t+=.008;'
          '  const prog=Math.min(1,t/6);'
          '  // Dark paper background with amber tint developing'
          '  const bg=ctx.createRadialGradient(CX,CY,0,CX,CY,Math.max(W,H));'
          '  bg.addColorStop(0,`rgba(${Math.floor(30*prog)},${Math.floor(10*prog)},${Math.floor(5*prog)},1)`);'
          '  bg.addColorStop(1,`rgba(2,1,0,1)`);'
          '  ctx.fillStyle=bg;ctx.fillRect(0,0,W,H);'
          '  // Develop the heart — amber/crimson tones'
          '  if(prog>.1){'
          '    const p2=Math.max(0,(prog-.1)/.9);'
          '    // Glow behind heart'
          '    const hg=ctx.createRadialGradient(CX,CY,0,CX,CY,SC*18*p2);'
          '    hg.addColorStop(0,`rgba(180,60,20,${p2*.25})`);'
          '    hg.addColorStop(.5,`rgba(100,20,5,${p2*.15})`);'
          '    hg.addColorStop(1,"rgba(0,0,0,0)");'
          '    ctx.fillStyle=hg;ctx.fillRect(0,0,W,H);'
          '    // Draw heart outline developing'
          '    const pts=[];for(let i=0;i<120;i++){const ti=(i/120)*Math.PI*2;pts.push(heartPt(ti));}'
          '    ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);'
          '    pts.forEach(p=>ctx.lineTo(p.x,p.y));ctx.closePath();'
          '    const hc=ctx.createLinearGradient(CX-SC*16,CY-SC*13,CX+SC*16,CY+SC*14);'
          '    hc.addColorStop(0,`rgba(220,80,40,${p2*.9})`);'
          '    hc.addColorStop(.5,`rgba(180,40,20,${p2*.7})`);'
          '    hc.addColorStop(1,`rgba(140,20,10,${p2*.5})`);'
          '    ctx.fillStyle=hc;ctx.fill();'
          '    ctx.strokeStyle=`rgba(255,120,60,${p2*.4})`;ctx.lineWidth=2;ctx.stroke();'
          '    // NAME text'
          '    if(p2>.6){'
          '      const ta=Math.min(1,(p2-.6)/.4);'
          '      ctx.save();ctx.globalAlpha=ta;'
          '      ctx.font=`bold ${Math.min(W*.055,24)}px "Dancing Script",cursive`;'
          '      ctx.textAlign="center";ctx.textBaseline="middle";'
          '      ctx.fillStyle=`rgba(255,200,160,${ta})`;'
          '      ctx.shadowColor="rgba(255,120,60,.5)";ctx.shadowBlur=10;'
          '      ctx.fillText(NAME,CX,CY);ctx.restore();}}'
          '  if(!msgShown&&t>7){msgShown=true;showFin();}'
          '  requestAnimationFrame(loop);}'
          'function showFin(){'
          '  const el=document.getElementById("fin");el.classList.add("show");'
          '  const m=document.getElementById("fm");m.textContent="";let j=0;'
          '  const iv=setInterval(()=>{if(j>=MSG.length){clearInterval(iv);return;}m.textContent+=MSG[j++];},54);}'
          'loop();window.addEventListener("resize",()=>{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;});')
    return (f'<!DOCTYPE html><html lang="en"><head>'
            f'<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>'
            f'<title>For {name}</title>{FONTS}'
            f'<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:100%;height:100%;background:#020100;overflow:hidden}}'
            f'#fin{{position:fixed;bottom:-220px;left:50%;transform:translateX(-50%);width:min(380px,92vw);background:rgba(10,4,2,.97);border-radius:18px;padding:26px 28px 22px;border:1px solid rgba(180,60,20,.2);transition:bottom 1.3s cubic-bezier(.34,1.4,.64,1);text-align:left;z-index:10}}'
            f'#fin.show{{bottom:clamp(18px,4vh,50px)}}'
            f'.ft{{font-family:"Caveat",cursive;font-size:.78rem;color:rgba(180,80,40,.4);letter-spacing:.15em;text-transform:uppercase;margin-bottom:10px}}'
            f'.fm{{font-family:"Caveat",cursive;font-size:clamp(1.05rem,3.5vw,1.35rem);color:#fde8d8;line-height:1.85;white-space:pre-wrap}}'
            f'.ff{{font-family:"Dancing Script",cursive;font-size:1.5rem;color:#e06030;text-align:right;margin-top:14px}}'
            f'.fd{{font-size:.68rem;color:rgba(180,80,40,.28);text-align:right;margin-top:2px;letter-spacing:.06em}}</style></head><body>'
            f'<canvas id="c"></canvas>'
            f'<div id="fin"><div class="ft">for {name.lower()}</div><div class="fm" id="fm"></div>'
            f'<div class="ff">— Dipesh</div><div class="fd">{date_str}</div></div>'
            f'<script>{js}</script></body></html>')


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
