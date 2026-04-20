"""
Daily Jenisha Love Page Generator
Works locally AND on GitHub Actions — no PC needed.
"""

import os, json, subprocess, datetime, sys, time, tempfile
from pathlib import Path

# ── Config — reads env vars (GitHub Actions) OR local .env file ───────────────
def load_config():
    cfg = {
        "GITHUB_TOKEN": os.environ.get("GH_PAT", ""),
        "GITHUB_USERNAME": os.environ.get("GH_USERNAME", "dipeshrayg"),
        "GITHUB_EMAIL": os.environ.get("GH_EMAIL", "dipesh.ray.g@gmail.com"),
        "HER_NAME": os.environ.get("HER_NAME", "Jenisha"),
    }
    # Fall back to local .env for local runs
    env_file = Path(__file__).parent / ".env"
    if env_file.exists() and not cfg["GITHUB_TOKEN"]:
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                if k == "GITHUB_TOKEN":   cfg["GITHUB_TOKEN"]   = v
                if k == "GITHUB_USERNAME": cfg["GITHUB_USERNAME"] = v
                if k == "GITHUB_EMAIL":    cfg["GITHUB_EMAIL"]    = v
                if k == "HER_NAME":        cfg["HER_NAME"]        = v
    return cfg

cfg      = load_config()
TOKEN    = cfg["GITHUB_TOKEN"]
USERNAME = cfg["GITHUB_USERNAME"]
EMAIL    = cfg["GITHUB_EMAIL"]
HER_NAME = cfg["HER_NAME"]

if not TOKEN:
    print("❌  No token found. Set GH_PAT env var or create a .env file.")
    sys.exit(1)

# ── Theme rotation ─────────────────────────────────────────────────────────────
THEMES = {
    0: {"name": "Galaxy",         "slug": "galaxy",   "mood": "Emotional"},
    1: {"name": "Cherry Blossom", "slug": "sakura",   "mood": "Loving"},
    2: {"name": "Ocean Waves",    "slug": "ocean",    "mood": "Romantic"},
    3: {"name": "Firefly Forest", "slug": "firefly",  "mood": "Dreamy"},
    4: {"name": "Neon Glow",      "slug": "neon",     "mood": "Flirty"},
    5: {"name": "Aurora",         "slug": "aurora",   "mood": "Breathtaking"},
    6: {"name": "Sunrise",        "slug": "sunrise",  "mood": "Hopeful"},
}

# ── HTML templates ─────────────────────────────────────────────────────────────
def html_galaxy(name, date_str):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0"/>
  <title>For {name} 💫</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Raleway:wght@300;400;500&display=swap" rel="stylesheet"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{width:100%;height:100%;background:radial-gradient(ellipse at 30% 20%,#1a0a2e,#080012 50%,#000005);overflow:hidden;font-family:'Raleway',sans-serif;color:#fff;cursor:none}}
    #sc,#pc{{position:fixed;top:0;left:0;width:100%;height:100%}}#sc{{z-index:1}}#pc{{z-index:5;pointer-events:none}}
    .cur{{position:fixed;z-index:9999;width:18px;height:18px;border-radius:50%;background:radial-gradient(circle,rgba(255,107,157,.9),transparent 70%);pointer-events:none;transform:translate(-50%,-50%);mix-blend-mode:screen}}
    .scene{{position:relative;z-index:10;width:100%;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:clamp(14px,3vh,28px)}}
    .title{{font-family:'Dancing Script',cursive;font-size:clamp(3.5rem,12vw,8rem);font-weight:700;background:linear-gradient(135deg,#ff9de2,#ff6b9d 30%,#c44dff 65%,#79cfff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;opacity:0;filter:blur(24px);transform:translateY(24px) scale(.92);animation:reveal 1.6s cubic-bezier(.22,1,.36,1) forwards 2.6s;letter-spacing:.04em}}
    .title::after{{content:'';display:block;margin:8px auto 0;height:2px;width:0;background:linear-gradient(90deg,transparent,#ff6b9d,#c44dff,transparent);animation:linegrow 1s ease forwards 4.3s}}
    .sub{{font-size:clamp(.7rem,2.2vw,1rem);font-weight:300;letter-spacing:.45em;text-transform:uppercase;color:rgba(255,255,255,.5);opacity:0;animation:fup 1s ease forwards 4.6s}}
    .hw{{opacity:0;animation:fup .8s ease forwards 5.4s}}.hi{{display:inline-block;font-size:clamp(2.2rem,7vw,3.6rem);animation:hpulse 1.6s ease-in-out infinite 5.4s;filter:drop-shadow(0 0 18px rgba(255,107,157,.85))}}
    .mw{{max-width:min(580px,92vw);opacity:0;animation:fup 1.2s ease forwards 6.4s}}.msg{{font-size:clamp(.88rem,2.4vw,1.1rem);font-weight:300;line-height:1.95;color:rgba(255,255,255,.82)}}.msg em{{font-style:italic;color:#ff6b9d}}.msg strong{{font-weight:500;color:#e0c0ff}}
    .btn{{opacity:0;animation:fup .8s ease forwards 9s;background:transparent;border:1.5px solid rgba(255,107,157,.55);color:#fff;font-family:'Raleway',sans-serif;font-size:clamp(.78rem,2.2vw,.92rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:14px 40px;border-radius:50px;cursor:pointer;transition:all .35s;backdrop-filter:blur(8px)}}
    .btn:hover{{border-color:#ff6b9d;box-shadow:0 0 28px rgba(255,107,157,.5),0 0 56px rgba(196,77,255,.2);transform:translateY(-2px)}}
    .ds{{position:fixed;bottom:18px;right:20px;font-size:.7rem;letter-spacing:.18em;color:rgba(255,255,255,.22);z-index:20;opacity:0;animation:fi 1s ease forwards 11s}}
    .ht{{position:fixed;bottom:18px;left:20px;font-size:.7rem;letter-spacing:.12em;color:rgba(255,255,255,.2);z-index:20;opacity:0;animation:fi 1s ease forwards 12s}}
    @keyframes reveal{{to{{opacity:1;filter:blur(0);transform:translateY(0) scale(1)}}}}@keyframes linegrow{{to{{width:55%}}}}@keyframes fup{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}@keyframes fi{{to{{opacity:1}}}}@keyframes hpulse{{0%,100%{{transform:scale(1)}}14%{{transform:scale(1.25)}}28%{{transform:scale(1)}}42%{{transform:scale(1.15)}}70%{{transform:scale(1)}}}}
  </style>
</head>
<body>
<canvas id="sc"></canvas><canvas id="pc"></canvas><div class="cur" id="cur"></div>
<div class="scene">
  <div class="title">{name}</div><div class="sub">this is for you</div>
  <div class="hw"><span class="hi">💗</span></div>
  <div class="mw"><p class="msg">Of all the stars scattered across this universe,<br><em>you are the one that makes the whole sky make sense.</em><br><br>Every time I think of you, it feels like<br>watching a constellation appear for the first time —<br><strong>breathtaking, extraordinary, and rare.</strong><br><br>This universe became more beautiful<br>the moment you were in it, <em>{name}.</em></p></div>
  <button class="btn" id="btn" onclick="sendLove()">✨ Feel My Love ✨</button>
</div>
<div class="ds">{date_str}</div><div class="ht">click anywhere for shooting stars</div>
<script>
const sc=document.getElementById('sc'),sx=sc.getContext('2d');const pc=document.getElementById('pc'),px=pc.getContext('2d');
let W=sc.width=pc.width=window.innerWidth,H=sc.height=pc.height=window.innerHeight;let mx=0,my=0;
const PAL=['255,255,255','255,200,225','210,185,255','175,220,255'];
class Star{{constructor(){{this.init()}}init(){{this.x=Math.random()*W;this.y=Math.random()*H;this.r=Math.random()*2.2+.15;this.base=Math.random()*.65+.25;this.op=this.base;this.ts=Math.random()*.018+.004;this.tp=Math.random()*Math.PI*2;this.col=PAL[Math.floor(Math.random()*PAL.length)];this.vx=(Math.random()-.5)*.06;this.vy=(Math.random()-.5)*.06;this.layer=Math.random()}}update(){{this.tp+=this.ts;this.op=Math.max(.08,Math.min(1,this.base+Math.sin(this.tp)*.28));const p=this.layer*.018;this.x+=this.vx+mx*p;this.y+=this.vy+my*p;if(this.x<0)this.x=W;if(this.x>W)this.x=0;if(this.y<0)this.y=H;if(this.y>H)this.y=0}}draw(){{sx.beginPath();sx.arc(this.x,this.y,this.r,0,Math.PI*2);sx.fillStyle=`rgba(${{this.col}},${{this.op}})`;sx.fill();if(this.r>1.4){{const g=sx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*4);g.addColorStop(0,`rgba(${{this.col}},${{this.op*.35}})`);g.addColorStop(1,'rgba(0,0,0,0)');sx.beginPath();sx.arc(this.x,this.y,this.r*4,0,Math.PI*2);sx.fillStyle=g;sx.fill()}}}}}}
class Streak{{constructor(ox,oy){{this.x=ox??Math.random()*W*.75;this.y=oy??Math.random()*H*.35;this.speed=Math.random()*9+6;this.angle=Math.PI/4+(Math.random()-.5)*.35;this.trail=[];this.op=1;this.alive=true}}update(){{this.x+=Math.cos(this.angle)*this.speed;this.y+=Math.sin(this.angle)*this.speed;this.trail.push({{x:this.x,y:this.y}});if(this.trail.length>22)this.trail.shift();this.op-=.022;if(this.op<=0||this.x>W+50||this.y>H+50)this.alive=false}}draw(){{if(this.trail.length<2)return;sx.beginPath();sx.moveTo(this.trail[0].x,this.trail[0].y);for(let i=1;i<this.trail.length;i++)sx.lineTo(this.trail[i].x,this.trail[i].y);const t0=this.trail[0],tN=this.trail[this.trail.length-1];const g=sx.createLinearGradient(t0.x,t0.y,tN.x,tN.y);g.addColorStop(0,'rgba(255,255,255,0)');g.addColorStop(1,`rgba(255,230,245,${{this.op}})`);sx.strokeStyle=g;sx.lineWidth=1.8;sx.stroke();const hg=sx.createRadialGradient(tN.x,tN.y,0,tN.x,tN.y,7);hg.addColorStop(0,`rgba(255,255,255,${{this.op}})`);hg.addColorStop(1,'rgba(255,255,255,0)');sx.beginPath();sx.arc(tN.x,tN.y,7,0,Math.PI*2);sx.fillStyle=hg;sx.fill()}}}}
const stars=Array.from({{length:420}},()=>new Star());const streaks=[];let lastS=0;
function drawNebula(){{const n1=sx.createRadialGradient(W*.18,H*.28,0,W*.18,H*.28,W*.42);n1.addColorStop(0,'rgba(255,100,160,.035)');n1.addColorStop(.55,'rgba(190,70,255,.02)');n1.addColorStop(1,'rgba(0,0,0,0)');sx.fillStyle=n1;sx.fillRect(0,0,W,H);const n2=sx.createRadialGradient(W*.82,H*.72,0,W*.82,H*.72,W*.38);n2.addColorStop(0,'rgba(70,180,255,.04)');n2.addColorStop(1,'rgba(0,0,0,0)');sx.fillStyle=n2;sx.fillRect(0,0,W,H)}}
function loopS(t){{sx.clearRect(0,0,W,H);drawNebula();if(t-lastS>4800+Math.random()*4000){{streaks.push(new Streak());lastS=t}}stars.forEach(s=>{{s.update();s.draw()}});for(let i=streaks.length-1;i>=0;i--){{streaks[i].update();streaks[i].draw();if(!streaks[i].alive)streaks.splice(i,1)}}requestAnimationFrame(loopS)}}
requestAnimationFrame(loopS);
const EM=['💗','💕','✨','💖','💝','🌸','⭐','🌟','💫','🪐'];const parts=[];
class Part{{constructor(x,y,burst){{this.x=x;this.y=y;this.em=EM[Math.floor(Math.random()*EM.length)];if(burst){{this.vx=(Math.random()-.5)*14;this.vy=(Math.random()-.85)*16;this.grav=.28;this.decay=Math.random()*.016+.01;this.sz=Math.random()*22+10}}else{{this.vx=(Math.random()-.5)*1.4;this.vy=-(Math.random()*1.8+.6);this.grav=-.008;this.decay=.0025+Math.random()*.002;this.sz=Math.random()*14+7}}this.rot=Math.random()*Math.PI*2;this.rs=(Math.random()-.5)*.12;this.life=1}}update(){{this.x+=this.vx;this.y+=this.vy;this.vy+=this.grav;this.vx*=.985;this.rot+=this.rs;this.life-=this.decay}}draw(){{px.save();px.globalAlpha=Math.max(0,this.life);px.translate(this.x,this.y);px.rotate(this.rot);px.font=`${{this.sz}}px Arial`;px.textAlign='center';px.textBaseline='middle';px.fillText(this.em,0,0);px.restore()}}}}
let ambT=0;function loopP(t){{px.clearRect(0,0,W,H);if(t-ambT>2200){{parts.push(new Part(Math.random()*W,H+20,false));ambT=t}}for(let i=parts.length-1;i>=0;i--){{parts[i].update();parts[i].draw();if(parts[i].life<=0)parts.splice(i,1)}}requestAnimationFrame(loopP)}}
requestAnimationFrame(loopP);
const cur=document.getElementById('cur');
document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px';mx=(e.clientX-W/2)/W*2;my=(e.clientY-H/2)/H*2}});
document.addEventListener('click',e=>{{if(e.target.id!=='btn'){{const ss=new Streak(e.clientX-80,e.clientY-80);ss.angle=Math.PI/4+(Math.random()-.5)*.5;streaks.push(ss)}}}});
document.addEventListener('touchstart',e=>{{const t=e.touches[0];const ss=new Streak(t.clientX-80,t.clientY-80);ss.angle=Math.PI/4+(Math.random()-.5)*.5;streaks.push(ss)}},{{passive:true}});
function sendLove(){{const btn=document.getElementById('btn');const r=btn.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;for(let i=0;i<60;i++)setTimeout(()=>parts.push(new Part(cx,cy,true)),i*18);btn.textContent='💗 Sent with Love 💗';btn.style.cssText+='border-color:rgba(255,107,157,1);box-shadow:0 0 40px rgba(255,107,157,.65),0 0 80px rgba(196,77,255,.3);';setTimeout(()=>{{btn.textContent='✨ Feel My Love ✨';btn.style.borderColor='rgba(255,107,157,.55)';btn.style.boxShadow=''}},3200)}}
window.addEventListener('resize',()=>{{W=sc.width=pc.width=window.innerWidth;H=sc.height=pc.height=window.innerHeight}});
</script></body></html>"""


def html_sakura(name, date_str):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>For {name} 🌸</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Raleway:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}body{{background:linear-gradient(160deg,#fff0f5,#ffe4f0 40%,#ffd6e8);min-height:100vh;overflow:hidden;font-family:'Raleway',sans-serif;color:#5a1a3a;cursor:none}}
    canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none}}.cur{{position:fixed;z-index:9999;width:16px;height:16px;border-radius:50%;background:rgba(255,107,157,.7);pointer-events:none;transform:translate(-50%,-50%)}}
    .scene{{position:relative;z-index:10;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:clamp(12px,2.5vh,24px)}}
    .title{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,11vw,7rem);font-weight:700;color:#c0396b;text-shadow:0 0 40px rgba(255,100,150,.4);opacity:0;animation:bloom 1.8s ease forwards 1.5s}}
    .sub{{font-size:clamp(.7rem,2vw,.95rem);letter-spacing:.4em;text-transform:uppercase;color:rgba(160,60,100,.6);opacity:0;animation:fup 1s ease forwards 3.5s}}
    .hw{{opacity:0;animation:fup .8s ease forwards 4.2s}}.hi{{font-size:clamp(2rem,6vw,3.2rem);display:inline-block;animation:swing 2s ease-in-out infinite 4.2s}}
    .mw{{max-width:min(560px,90vw);opacity:0;animation:fup 1.2s ease forwards 5.2s}}.msg{{font-size:clamp(.86rem,2.3vw,1.08rem);font-weight:300;line-height:2;color:rgba(80,20,50,.8)}}.msg em{{color:#d44070;font-style:italic}}.msg strong{{color:#8b1a4a}}
    .btn{{opacity:0;animation:fup .8s ease forwards 8s;background:rgba(255,255,255,.6);border:1.5px solid rgba(200,60,100,.5);color:#8b1a4a;font-family:'Raleway',sans-serif;font-size:clamp(.78rem,2vw,.9rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:13px 38px;border-radius:50px;cursor:pointer;backdrop-filter:blur(10px);transition:all .3s}}
    .btn:hover{{background:rgba(255,150,180,.2);border-color:#d44070;box-shadow:0 0 24px rgba(212,64,112,.3);transform:translateY(-2px)}}
    .ds{{position:fixed;bottom:16px;right:18px;font-size:.68rem;letter-spacing:.15em;color:rgba(160,60,100,.4);z-index:20;opacity:0;animation:fi 1s ease forwards 10s}}
    @keyframes bloom{{from{{opacity:0;transform:scale(.7);filter:blur(12px)}}to{{opacity:1;transform:scale(1);filter:blur(0)}}}}@keyframes fup{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}@keyframes fi{{to{{opacity:1}}}}@keyframes swing{{0%,100%{{transform:rotate(-8deg)}}50%{{transform:rotate(8deg)}}}}
  </style>
</head>
<body>
<canvas id="cv"></canvas><div class="cur" id="cur"></div>
<div class="scene">
  <div class="title">{name}</div><div class="sub">a garden blooms for you</div>
  <div class="hw"><span class="hi">🌸</span></div>
  <div class="mw"><p class="msg">Like cherry blossoms that bloom only once a year,<br><em>you are that rare and beautiful thing</em><br>I never want to stop looking at.<br><br>Every petal that falls reminds me<br>how <strong>gently and completely</strong><br>you've filled my world with colour,<br><em>{name}.</em></p></div>
  <button class="btn" id="btn" onclick="sendLove()">🌸 Bloom with Love 🌸</button>
</div>
<div class="ds">{date_str}</div>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const petals=[];const PCOLS=['rgba(255,182,210,.8)','rgba(255,150,190,.75)','rgba(255,210,225,.85)','rgba(240,160,200,.7)'];
class Petal{{constructor(){{this.reset(true)}}reset(init){{this.x=Math.random()*W;this.y=init?Math.random()*H:-20;this.size=Math.random()*14+7;this.speed=Math.random()*1.5+.5;this.wind=Math.random()*.8-.4;this.wobble=Math.random()*Math.PI*2;this.wobbleSpeed=Math.random()*.04+.01;this.rot=Math.random()*Math.PI*2;this.rotS=(Math.random()-.5)*.06;this.col=PCOLS[Math.floor(Math.random()*PCOLS.length)];this.op=Math.random()*.6+.3}}update(){{this.y+=this.speed;this.wobble+=this.wobbleSpeed;this.x+=this.wind+Math.sin(this.wobble)*.8;this.rot+=this.rotS;if(this.y>H+20)this.reset(false)}}draw(){{ctx.save();ctx.translate(this.x,this.y);ctx.rotate(this.rot);ctx.globalAlpha=this.op;ctx.fillStyle=this.col;ctx.beginPath();ctx.ellipse(0,0,this.size/2,this.size,0,0,Math.PI*2);ctx.fill();ctx.restore()}}}}
for(let i=0;i<120;i++)petals.push(new Petal());
function loop(){{ctx.clearRect(0,0,W,H);petals.forEach(p=>{{p.update();p.draw()}});requestAnimationFrame(loop)}}loop();
const cur=document.getElementById('cur');document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px'}});
function sendLove(){{const btn=document.getElementById('btn');btn.textContent='💗 With All My Love 💗';setTimeout(()=>btn.textContent='🌸 Bloom with Love 🌸',3000)}}
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight}});
</script></body></html>"""


def html_ocean(name, date_str):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>For {name} 🌊</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Raleway:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}body{{background:linear-gradient(180deg,#001428,#002850 30%,#003d70 60%,#004d88);min-height:100vh;overflow:hidden;font-family:'Raleway',sans-serif;color:#e0f4ff;cursor:none}}
    canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none}}.cur{{position:fixed;z-index:9999;width:16px;height:16px;border-radius:50%;background:rgba(100,200,255,.8);pointer-events:none;transform:translate(-50%,-50%)}}
    .scene{{position:relative;z-index:10;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:clamp(12px,2.5vh,24px)}}
    .title{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,11vw,7rem);font-weight:700;background:linear-gradient(135deg,#a0e8ff,#60c8ff,#fff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;opacity:0;animation:fup 1.8s ease forwards 2s}}
    .sub{{font-size:clamp(.7rem,2vw,.95rem);letter-spacing:.4em;text-transform:uppercase;color:rgba(160,220,255,.55);opacity:0;animation:fup 1s ease forwards 4s}}
    .hw{{opacity:0;animation:fup .8s ease forwards 4.8s}}.hi{{font-size:clamp(2rem,6vw,3.2rem);display:inline-block;animation:wave 2.5s ease-in-out infinite 4.8s}}
    .mw{{max-width:min(560px,90vw);opacity:0;animation:fup 1.2s ease forwards 5.8s}}.msg{{font-size:clamp(.86rem,2.3vw,1.08rem);font-weight:300;line-height:2;color:rgba(220,240,255,.82)}}.msg em{{color:#80d8ff;font-style:italic}}.msg strong{{color:#b0e8ff;font-weight:500}}
    .btn{{opacity:0;animation:fup .8s ease forwards 8.5s;background:transparent;border:1.5px solid rgba(100,200,255,.5);color:#e0f4ff;font-family:'Raleway',sans-serif;font-size:clamp(.78rem,2vw,.9rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:13px 38px;border-radius:50px;cursor:pointer;backdrop-filter:blur(8px);transition:all .3s}}
    .btn:hover{{border-color:#80d8ff;box-shadow:0 0 24px rgba(80,180,255,.4);transform:translateY(-2px)}}
    .ds{{position:fixed;bottom:16px;right:18px;font-size:.68rem;letter-spacing:.15em;color:rgba(160,220,255,.3);z-index:20;opacity:0;animation:fi 1s ease forwards 11s}}
    @keyframes fup{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}@keyframes fi{{to{{opacity:1}}}}@keyframes wave{{0%,100%{{transform:translateY(0) rotate(-5deg)}}50%{{transform:translateY(-8px) rotate(5deg)}}}}
  </style>
</head>
<body>
<canvas id="cv"></canvas><div class="cur" id="cur"></div>
<div class="scene">
  <div class="title">{name}</div><div class="sub">deep as the ocean</div>
  <div class="hw"><span class="hi">🌊</span></div>
  <div class="mw"><p class="msg">Like the ocean has no end,<br><em>what I feel for you has no boundary.</em><br><br>In the stillness of the deep water,<br>in the crash of every wave —<br><strong>every rhythm, every tide</strong><br>finds its way back to you,<br><em>{name}.</em></p></div>
  <button class="btn" id="btn" onclick="sendLove()">🌊 Ride the Wave 🌊</button>
</div>
<div class="ds">{date_str}</div>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;let t=0;
const bubbles=[];
class Bubble{{constructor(){{this.x=Math.random()*W;this.y=H+20;this.r=Math.random()*6+2;this.speed=Math.random()*1.2+.4;this.wobble=Math.random()*Math.PI*2;this.ws=Math.random()*.04+.01;this.op=Math.random()*.5+.2}}update(){{this.y-=this.speed;this.wobble+=this.ws;this.x+=Math.sin(this.wobble)*.6;this.op-=.002;if(this.y<-10||this.op<=0){{this.y=H+20;this.x=Math.random()*W;this.op=Math.random()*.5+.2}}}}draw(){{ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);ctx.strokeStyle=`rgba(150,220,255,${{this.op}})`;ctx.lineWidth=1;ctx.stroke()}}}}
for(let i=0;i<80;i++)bubbles.push(new Bubble());
function drawWaves(){{for(let w=0;w<3;w++){{const off=w*30,spd=(.0008+w*.0003)*t,amp=12+w*8,y=H*.75+off;ctx.beginPath();ctx.moveTo(0,y);for(let x=0;x<=W;x+=4)ctx.lineTo(x,y+Math.sin(x*.012+spd)*amp+Math.sin(x*.024+spd*1.5)*amp*.5);ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();const g=ctx.createLinearGradient(0,y,0,H);g.addColorStop(0,`rgba(0,100,160,${{.25-w*.06}})`);g.addColorStop(1,'rgba(0,60,120,0)');ctx.fillStyle=g;ctx.fill()}}}}
function loop(ts){{t=ts;ctx.clearRect(0,0,W,H);drawWaves();bubbles.forEach(b=>{{b.update();b.draw()}});requestAnimationFrame(loop)}}loop(0);
const cur=document.getElementById('cur');document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px'}});
function sendLove(){{const btn=document.getElementById('btn');btn.textContent='💙 Endless as the Ocean 💙';setTimeout(()=>btn.textContent='🌊 Ride the Wave 🌊',3000)}}
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight}});
</script></body></html>"""


def html_firefly(name, date_str):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>For {name} ✨</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Raleway:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}body{{background:radial-gradient(ellipse at 50% 80%,#0a1a08,#060f04 60%,#020804);min-height:100vh;overflow:hidden;font-family:'Raleway',sans-serif;color:#d4ffb0;cursor:none}}
    canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none}}.cur{{position:fixed;z-index:9999;width:14px;height:14px;border-radius:50%;background:rgba(180,255,100,.8);pointer-events:none;transform:translate(-50%,-50%);box-shadow:0 0 8px rgba(180,255,100,.6)}}
    .scene{{position:relative;z-index:10;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:clamp(12px,2.5vh,24px)}}
    .title{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,11vw,7rem);font-weight:700;color:#c8ff80;text-shadow:0 0 40px rgba(150,255,80,.5),0 0 80px rgba(100,200,60,.3);opacity:0;animation:glow 2s ease forwards 2s}}
    .sub{{font-size:clamp(.7rem,2vw,.95rem);letter-spacing:.4em;text-transform:uppercase;color:rgba(180,255,120,.45);opacity:0;animation:fup 1s ease forwards 4.2s}}
    .hw{{opacity:0;animation:fup .8s ease forwards 5s}}.hi{{font-size:clamp(2rem,6vw,3.2rem);display:inline-block;animation:drift 3s ease-in-out infinite 5s;filter:drop-shadow(0 0 12px rgba(255,220,100,.8))}}
    .mw{{max-width:min(560px,90vw);opacity:0;animation:fup 1.2s ease forwards 6s}}.msg{{font-size:clamp(.86rem,2.3vw,1.08rem);font-weight:300;line-height:2;color:rgba(200,255,160,.8)}}.msg em{{color:#b0ff60;font-style:italic}}.msg strong{{color:#d8ff90}}
    .btn{{opacity:0;animation:fup .8s ease forwards 8.8s;background:transparent;border:1.5px solid rgba(150,255,80,.45);color:#d4ffb0;font-family:'Raleway',sans-serif;font-size:clamp(.78rem,2vw,.9rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:13px 38px;border-radius:50px;cursor:pointer;backdrop-filter:blur(8px);transition:all .3s}}
    .btn:hover{{border-color:rgba(150,255,80,.9);box-shadow:0 0 24px rgba(120,220,60,.4);transform:translateY(-2px)}}
    .ds{{position:fixed;bottom:16px;right:18px;font-size:.68rem;letter-spacing:.15em;color:rgba(150,255,80,.25);z-index:20;opacity:0;animation:fi 1s ease forwards 11s}}
    @keyframes glow{{from{{opacity:0;filter:blur(20px)}}to{{opacity:1;filter:blur(0)}}}}@keyframes fup{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}@keyframes fi{{to{{opacity:1}}}}@keyframes drift{{0%,100%{{transform:translateY(0) translateX(0)}}33%{{transform:translateY(-6px) translateX(4px)}}66%{{transform:translateY(4px) translateX(-4px)}}}}
  </style>
</head>
<body>
<canvas id="cv"></canvas><div class="cur" id="cur"></div>
<div class="scene">
  <div class="title">{name}</div><div class="sub">you light up the dark</div>
  <div class="hw"><span class="hi">✨</span></div>
  <div class="mw"><p class="msg">In the quiet of a dark forest night,<br><em>fireflies remind me of you —</em><br>small, soft, impossible to ignore.<br><br>You carry a light inside you<br>that <strong>turns ordinary nights</strong> into magic.<br><br><em>{name}</em>, you are that light in my world.</p></div>
  <button class="btn" id="btn" onclick="sendLove()">✨ Spark My World ✨</button>
</div>
<div class="ds">{date_str}</div>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const flies=[];
class Fly{{constructor(){{this.reset()}}reset(){{this.x=Math.random()*W;this.y=Math.random()*H*.85+H*.1;this.tx=this.x+(Math.random()-.5)*120;this.ty=this.y+(Math.random()-.5)*120;this.op=0;this.maxOp=Math.random()*.7+.3;this.phase='in';this.speed=Math.random()*.015+.005}}update(){{const dx=this.tx-this.x,dy=this.ty-this.y;this.x+=dx*.02;this.y+=dy*.02;if(this.phase==='in'){{this.op+=.03;if(this.op>=this.maxOp){{this.op=this.maxOp;if(Math.random()<.01)this.phase='out'}}}}else{{this.op-=.02;if(this.op<=0)this.reset()}}}}draw(){{ctx.beginPath();ctx.arc(this.x,this.y,3,0,Math.PI*2);ctx.fillStyle=`rgba(180,255,100,${{this.op}})`;ctx.fill();const g=ctx.createRadialGradient(this.x,this.y,0,this.x,this.y,15);g.addColorStop(0,`rgba(180,255,100,${{this.op*.4}})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.beginPath();ctx.arc(this.x,this.y,15,0,Math.PI*2);ctx.fillStyle=g;ctx.fill()}}}}
for(let i=0;i<100;i++)flies.push(new Fly());
function drawTrees(){{ctx.fillStyle='rgba(5,15,3,.9)';for(let i=0;i<12;i++){{const x=i*(W/11);const h=H*.35+Math.sin(i*2.3)*H*.08;ctx.beginPath();ctx.moveTo(x,H);ctx.lineTo(x-30,H-h*.4);ctx.lineTo(x,H-h);ctx.lineTo(x+30,H-h*.4);ctx.closePath();ctx.fill()}}}}
function loop(){{ctx.clearRect(0,0,W,H);drawTrees();flies.forEach(f=>{{f.update();f.draw()}});requestAnimationFrame(loop)}}loop();
const cur=document.getElementById('cur');document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px'}});
function sendLove(){{const btn=document.getElementById('btn');btn.textContent='💚 You Are My Light 💚';setTimeout(()=>btn.textContent='✨ Spark My World ✨',3000)}}
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight}});
</script></body></html>"""


def html_neon(name, date_str):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>For {name} 💜</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Raleway:wght@300;400;700&display=swap" rel="stylesheet"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}body{{background:#05010f;min-height:100vh;overflow:hidden;font-family:'Raleway',sans-serif;color:#fff;cursor:none}}
    canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none}}.cur{{position:fixed;z-index:9999;width:16px;height:16px;border-radius:50%;background:rgba(255,50,200,.9);pointer-events:none;transform:translate(-50%,-50%);mix-blend-mode:screen}}
    .scene{{position:relative;z-index:10;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:clamp(12px,2.5vh,24px)}}
    .title{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,11vw,7rem);font-weight:700;color:#ff40e0;text-shadow:0 0 20px #ff40e0,0 0 60px rgba(255,64,224,.5),0 0 100px rgba(255,64,224,.3);opacity:0;animation:neonOn 2s ease forwards 1.8s}}
    .sub{{font-size:clamp(.7rem,2vw,.95rem);letter-spacing:.5em;text-transform:uppercase;color:rgba(255,150,255,.5);opacity:0;animation:fup 1s ease forwards 3.8s}}
    .hw{{opacity:0;animation:fup .8s ease forwards 4.6s}}.hi{{font-size:clamp(2rem,6vw,3.2rem);display:inline-block;animation:flicker 3s ease-in-out infinite 4.6s}}
    .mw{{max-width:min(560px,90vw);opacity:0;animation:fup 1.2s ease forwards 5.6s}}.msg{{font-size:clamp(.86rem,2.3vw,1.08rem);font-weight:300;line-height:2;color:rgba(255,220,255,.8)}}.msg em{{color:#ff80ff;font-style:italic}}.msg strong{{color:#ffb0ff}}
    .btn{{opacity:0;animation:fup .8s ease forwards 8.4s;background:transparent;border:1.5px solid rgba(255,64,224,.6);color:#fff;font-family:'Raleway',sans-serif;font-size:clamp(.78rem,2vw,.9rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:13px 38px;border-radius:50px;cursor:pointer;transition:all .3s;text-shadow:0 0 8px rgba(255,64,224,.8)}}
    .btn:hover{{border-color:#ff40e0;box-shadow:0 0 20px rgba(255,64,224,.6),0 0 40px rgba(255,64,224,.3);transform:translateY(-2px)}}
    .ds{{position:fixed;bottom:16px;right:18px;font-size:.68rem;letter-spacing:.18em;color:rgba(255,150,255,.25);z-index:20;opacity:0;animation:fi 1s ease forwards 11s}}
    @keyframes neonOn{{0%{{opacity:0;text-shadow:none}}50%{{opacity:.6;text-shadow:0 0 10px #ff40e0}}100%{{opacity:1;text-shadow:0 0 20px #ff40e0,0 0 60px rgba(255,64,224,.5)}}}}@keyframes fup{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}@keyframes fi{{to{{opacity:1}}}}@keyframes flicker{{0%,100%{{opacity:1}}92%{{opacity:1}}93%{{opacity:.4}}94%{{opacity:1}}96%{{opacity:.7}}97%{{opacity:1}}}}
  </style>
</head>
<body>
<canvas id="cv"></canvas><div class="cur" id="cur"></div>
<div class="scene">
  <div class="title">{name}</div><div class="sub">you make me glow</div>
  <div class="hw"><span class="hi">💜</span></div>
  <div class="mw"><p class="msg">In a city of a million lights,<br><em>you are the neon sign I keep looking for.</em><br><br>Bright, bold, impossible to walk past.<br>You make everywhere you go<br><strong>feel like the place to be</strong> —<br>and I want to be wherever you are,<br><em>{name}.</em></p></div>
  <button class="btn" id="btn" onclick="sendLove()">💜 Light Me Up 💜</button>
</div>
<div class="ds">{date_str}</div>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;
const sparks=[];
class Spark{{constructor(){{this.x=Math.random()*W;this.y=Math.random()*H;this.vx=(Math.random()-.5)*3;this.vy=(Math.random()-.5)*3;this.life=Math.random()*.8+.2;this.decay=Math.random()*.008+.004;this.r=Math.random()*2+.5;const h=['255,40,224','200,40,255','255,100,255','100,200,255'];this.col=h[Math.floor(Math.random()*h.length)]}}update(){{this.x+=this.vx;this.y+=this.vy;this.vx*=.97;this.vy*=.97;this.life-=this.decay;if(this.x<0||this.x>W)this.vx*=-1;if(this.y<0||this.y>H)this.vy*=-1}}draw(){{ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);ctx.fillStyle=`rgba(${{this.col}},${{this.life}})`;ctx.fill();const g=ctx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*6);g.addColorStop(0,`rgba(${{this.col}},${{this.life*.3}})`);g.addColorStop(1,'rgba(0,0,0,0)');ctx.beginPath();ctx.arc(this.x,this.y,this.r*6,0,Math.PI*2);ctx.fillStyle=g;ctx.fill()}}}}
for(let i=0;i<200;i++)sparks.push(new Spark());
function loop(){{ctx.clearRect(0,0,W,H);sparks.forEach((s,i)=>{{s.update();s.draw();if(s.life<=0)sparks[i]=new Spark()}});requestAnimationFrame(loop)}}loop();
const cur=document.getElementById('cur');document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px'}});
function sendLove(){{const btn=document.getElementById('btn');btn.textContent='💜 You Are My Glow 💜';setTimeout(()=>btn.textContent='💜 Light Me Up 💜',3000)}}
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight}});
</script></body></html>"""


def html_aurora(name, date_str):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>For {name} 🌌</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Raleway:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}body{{background:#000d1a;min-height:100vh;overflow:hidden;font-family:'Raleway',sans-serif;color:#e0fff8;cursor:none}}
    canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none}}.cur{{position:fixed;z-index:9999;width:14px;height:14px;border-radius:50%;background:rgba(80,255,200,.8);pointer-events:none;transform:translate(-50%,-50%)}}
    .scene{{position:relative;z-index:10;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:clamp(12px,2.5vh,24px)}}
    .title{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,11vw,7rem);font-weight:700;background:linear-gradient(135deg,#80ffcc,#40e0d0,#60d0ff,#b060ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;opacity:0;animation:fup 2s ease forwards 2.5s}}
    .sub{{font-size:clamp(.7rem,2vw,.95rem);letter-spacing:.4em;text-transform:uppercase;color:rgba(120,255,210,.45);opacity:0;animation:fup 1s ease forwards 4.8s}}
    .hw{{opacity:0;animation:fup .8s ease forwards 5.6s}}.hi{{font-size:clamp(2rem,6vw,3.2rem);display:inline-block;animation:aur 4s ease-in-out infinite 5.6s}}
    .mw{{max-width:min(560px,90vw);opacity:0;animation:fup 1.2s ease forwards 6.6s}}.msg{{font-size:clamp(.86rem,2.3vw,1.08rem);font-weight:300;line-height:2;color:rgba(200,255,240,.8)}}.msg em{{color:#80ffcc;font-style:italic}}.msg strong{{color:#b0ffe8}}
    .btn{{opacity:0;animation:fup .8s ease forwards 9.4s;background:transparent;border:1.5px solid rgba(80,220,180,.5);color:#e0fff8;font-family:'Raleway',sans-serif;font-size:clamp(.78rem,2vw,.9rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:13px 38px;border-radius:50px;cursor:pointer;backdrop-filter:blur(8px);transition:all .3s}}
    .btn:hover{{border-color:rgba(80,255,200,.9);box-shadow:0 0 24px rgba(60,200,160,.5);transform:translateY(-2px)}}
    .ds{{position:fixed;bottom:16px;right:18px;font-size:.68rem;letter-spacing:.15em;color:rgba(100,255,200,.25);z-index:20;opacity:0;animation:fi 1s ease forwards 12s}}
    @keyframes fup{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}@keyframes fi{{to{{opacity:1}}}}@keyframes aur{{0%,100%{{filter:hue-rotate(0deg) drop-shadow(0 0 12px rgba(80,255,200,.6))}}50%{{filter:hue-rotate(60deg) drop-shadow(0 0 20px rgba(80,200,255,.8))}}}}
  </style>
</head>
<body>
<canvas id="cv"></canvas><div class="cur" id="cur"></div>
<div class="scene">
  <div class="title">{name}</div><div class="sub">as rare as the northern lights</div>
  <div class="hw"><span class="hi">🌌</span></div>
  <div class="mw"><p class="msg">The northern lights don't appear every night —<br><em>they are rare, and for that, more beautiful.</em><br><br>You are like that.<br><strong>Something so uncommon, so stunning,</strong><br>that when you show up,<br>the whole sky changes.<br><br><em>{name}</em>, you are my northern light.</p></div>
  <button class="btn" id="btn" onclick="sendLove()">🌌 Dance with Me 🌌</button>
</div>
<div class="ds">{date_str}</div>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;let t=0;
const BANDS=[{{col:'rgba(40,255,160,',y:.15,amp:.08,freq:.6,sp:.0004}},{{col:'rgba(40,200,255,',y:.25,amp:.06,freq:.8,sp:.0006}},{{col:'rgba(140,60,255,',y:.10,amp:.10,freq:.5,sp:.0003}},{{col:'rgba(80,255,220,',y:.20,amp:.07,freq:.7,sp:.0005}}];
function drawAurora(){{BANDS.forEach(b=>{{for(let i=0;i<3;i++){{const yB=H*b.y+i*H*.04;const op=(.06-i*.015)+Math.sin(t*b.sp*1000+i)*.02;ctx.beginPath();ctx.moveTo(0,yB);for(let x=0;x<=W;x+=6){{const y=yB+Math.sin(x*b.freq*.01+t*b.sp*1000)*H*b.amp+Math.sin(x*.02+t*b.sp*800)*(H*b.amp*.4);ctx.lineTo(x,y)}}ctx.lineTo(W,0);ctx.lineTo(0,0);ctx.closePath();const g=ctx.createLinearGradient(0,0,0,H*.5);g.addColorStop(0,b.col+'0)');g.addColorStop(.5,b.col+op+')');g.addColorStop(1,b.col+'0)');ctx.fillStyle=g;ctx.fill()}}}}}}
const stars2=Array.from({{length:200}},()=>{{return{{x:Math.random()*W,y:Math.random()*H*.6,r:Math.random()*1.5+.3,op:Math.random()*.6+.2,tp:Math.random()*Math.PI*2,ts:Math.random()*.02+.005}}}});
function loop(ts){{t=ts/1000;ctx.clearRect(0,0,W,H);stars2.forEach(s=>{{s.tp+=s.ts;const o=s.op+Math.sin(s.tp)*.2;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(255,255,255,${{o}})`;ctx.fill()}});drawAurora();requestAnimationFrame(loop)}}loop(0);
const cur=document.getElementById('cur');document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px'}});
function sendLove(){{const btn=document.getElementById('btn');btn.textContent='💚 You Are My Aurora 💚';setTimeout(()=>btn.textContent='🌌 Dance with Me 🌌',3000)}}
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight}});
</script></body></html>"""


def html_sunrise(name, date_str):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>For {name} 🌅</title>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Raleway:wght@300;400&display=swap" rel="stylesheet"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}body{{background:linear-gradient(180deg,#1a0a00,#3d1500 20%,#7a2d00 40%,#c45200 60%,#f5822a 80%,#ffb347);min-height:100vh;overflow:hidden;font-family:'Raleway',sans-serif;color:#fff5e0;cursor:none}}
    canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none}}.cur{{position:fixed;z-index:9999;width:16px;height:16px;border-radius:50%;background:rgba(255,180,50,.9);pointer-events:none;transform:translate(-50%,-50%);box-shadow:0 0 8px rgba(255,150,30,.8)}}
    .scene{{position:relative;z-index:10;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:24px;gap:clamp(12px,2.5vh,24px)}}
    .title{{font-family:'Dancing Script',cursive;font-size:clamp(3rem,11vw,7rem);font-weight:700;color:#ffedbb;text-shadow:0 0 40px rgba(255,160,30,.6),0 0 80px rgba(255,100,0,.3);opacity:0;animation:rise 2s ease forwards 2s}}
    .sub{{font-size:clamp(.7rem,2vw,.95rem);letter-spacing:.4em;text-transform:uppercase;color:rgba(255,220,150,.5);opacity:0;animation:fup 1s ease forwards 4.3s}}
    .hw{{opacity:0;animation:fup .8s ease forwards 5.1s}}.hi{{font-size:clamp(2rem,6vw,3.2rem);display:inline-block;animation:sunp 2s ease-in-out infinite 5.1s;filter:drop-shadow(0 0 16px rgba(255,180,0,.8))}}
    .mw{{max-width:min(560px,90vw);opacity:0;animation:fup 1.2s ease forwards 6.1s}}.msg{{font-size:clamp(.86rem,2.3vw,1.08rem);font-weight:300;line-height:2;color:rgba(255,240,200,.85)}}.msg em{{color:#ffcc60;font-style:italic}}.msg strong{{color:#ffd88a}}
    .btn{{opacity:0;animation:fup .8s ease forwards 8.9s;background:transparent;border:1.5px solid rgba(255,180,50,.5);color:#fff5e0;font-family:'Raleway',sans-serif;font-size:clamp(.78rem,2vw,.9rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:13px 38px;border-radius:50px;cursor:pointer;backdrop-filter:blur(8px);transition:all .3s}}
    .btn:hover{{border-color:rgba(255,180,50,.9);box-shadow:0 0 24px rgba(255,150,30,.5);transform:translateY(-2px)}}
    .ds{{position:fixed;bottom:16px;right:18px;font-size:.68rem;letter-spacing:.15em;color:rgba(255,200,100,.3);z-index:20;opacity:0;animation:fi 1s ease forwards 11s}}
    @keyframes rise{{from{{opacity:0;transform:translateY(30px);filter:blur(16px)}}to{{opacity:1;transform:translateY(0);filter:blur(0)}}}}@keyframes fup{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}@keyframes fi{{to{{opacity:1}}}}@keyframes sunp{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.12)}}}}
  </style>
</head>
<body>
<canvas id="cv"></canvas><div class="cur" id="cur"></div>
<div class="scene">
  <div class="title">{name}</div><div class="sub">every morning, you</div>
  <div class="hw"><span class="hi">🌅</span></div>
  <div class="mw"><p class="msg">Every morning the sun rises<br>and <em>the world gets a second chance</em> —<br>warm, golden, full of hope.<br><br>That's what you feel like.<br><strong>Like a sunrise I never get tired of.</strong><br><br>Every day is better just because<br>you're in it, <em>{name}.</em></p></div>
  <button class="btn" id="btn" onclick="sendLove()">🌅 Brighten My Day 🌅</button>
</div>
<div class="ds">{date_str}</div>
<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W=cv.width=window.innerWidth,H=cv.height=window.innerHeight;let t=0;
const motes=Array.from({{length:60}},()=>{{return{{x:Math.random()*W,y:H*.4+Math.random()*H*.6,vx:(Math.random()-.5)*.4,vy:-(Math.random()*.6+.2),op:Math.random()*.5+.3,r:Math.random()*3+1,decay:.003+Math.random()*.003}}}});
function loop(ts){{t=ts/1000;ctx.clearRect(0,0,W,H);const sG=ctx.createRadialGradient(W*.5,H*.55,0,W*.5,H*.55,W*.4);sG.addColorStop(0,'rgba(255,220,80,.18)');sG.addColorStop(.4,'rgba(255,140,20,.06)');sG.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=sG;ctx.fillRect(0,0,W,H);motes.forEach(m=>{{m.x+=m.vx;m.y+=m.vy;m.op-=m.decay;if(m.op<=0){{m.x=Math.random()*W;m.y=H+10;m.op=Math.random()*.5+.3;m.vy=-(Math.random()*.6+.2)}}ctx.beginPath();ctx.arc(m.x,m.y,m.r,0,Math.PI*2);ctx.fillStyle=`rgba(255,200,80,${{m.op}})`;ctx.fill()}});requestAnimationFrame(loop)}}loop(0);
const cur=document.getElementById('cur');document.addEventListener('mousemove',e=>{{cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px'}});
function sendLove(){{const btn=document.getElementById('btn');btn.textContent='☀️ You Are My Sunshine ☀️';setTimeout(()=>btn.textContent='🌅 Brighten My Day 🌅',3000)}}
window.addEventListener('resize',()=>{{W=cv.width=window.innerWidth;H=cv.height=window.innerHeight}});
</script></body></html>"""


# ── Theme dispatcher ────────────────────────────────────────────────────────────
GENERATORS = {
    "galaxy":  html_galaxy,
    "sakura":  html_sakura,
    "ocean":   html_ocean,
    "firefly": html_firefly,
    "neon":    html_neon,
    "aurora":  html_aurora,
    "sunrise": html_sunrise,
}

def get_html(slug, name, date_str):
    return GENERATORS.get(slug, html_galaxy)(name, date_str)


# ── GitHub API ──────────────────────────────────────────────────────────────────
import urllib.request, urllib.error

def gh_api(method, path, data=None):
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "jenisha-love-bot",
    }
    body = json.dumps(data).encode() if data else None
    req  = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    today     = datetime.date.today()
    dow       = today.weekday()
    theme     = THEMES[dow]
    date_str  = today.strftime("%B %d · %Y")
    repo_name = f"for-jenisha-{today.strftime('%Y%m%d')}"

    print(f"\n{'='*52}")
    print(f"  💗  Daily Love Page — {HER_NAME}")
    print(f"  📅  {date_str}  |  Theme: {theme['name']} ({theme['mood']})")
    print(f"{'='*52}\n")

    # 1. Generate HTML in a temp dir
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        html = get_html(theme["slug"], HER_NAME, date_str)
        (tmp / "index.html").write_text(html, encoding="utf-8")
        print("✅  HTML generated")

        # 2. Create GitHub repo
        desc = f"A little piece of the {theme['name'].lower()}, made just for {HER_NAME} 💗 ({date_str})"
        repo_data, status = gh_api("POST", "/user/repos", {
            "name": repo_name, "description": desc,
            "private": False, "auto_init": False,
        })
        if status not in (200, 201):
            if "already exists" in str(repo_data):
                print(f"⚠️   Repo already exists — continuing")
            else:
                print(f"❌  Repo creation failed (HTTP {status}): {repo_data}")
                sys.exit(1)
        else:
            print(f"✅  Repo created → https://github.com/{USERNAME}/{repo_name}")

        # 3. Git init & push
        run(f'git config --global user.email "{EMAIL}"')
        run(f'git config --global user.name "Dipesh"')
        remote = f"https://{TOKEN}@github.com/{USERNAME}/{repo_name}.git"
        for cmd in [
            "git init -b main",
            "git add index.html",
            'git commit -m "💗 Daily love page for Jenisha"',
            f"git remote add origin {remote}",
            "git push -u origin main",
        ]:
            code, out, err = run(cmd, cwd=tmp)
            display = cmd.replace(TOKEN, "***")
            if code != 0 and "already exists" not in err:
                print(f"⚠️   {display} → {err}")
            else:
                print(f"✅  {display}")

        # 4. Enable GitHub Pages
        time.sleep(4)
        gh_api("POST", f"/repos/{USERNAME}/{repo_name}/pages",
               {"source": {"branch": "main", "path": "/"}})
        page_url = f"https://{USERNAME}.github.io/{repo_name}/"
        print(f"✅  Pages enabled → {page_url}")

    print(f"\n  🎉  Live in ~60s: {page_url}\n")
    return page_url, theme, date_str, repo_name


if __name__ == "__main__":
    main()
