"""
Daily Jenisha Love Page Generator  v2.0
- Interactive unlock mechanics (star hunt, scratch reveal, constellation)
- Flirty professional email format  (every 11th day)
- Heart-shaped QR code format       (every 7th day)
- Theme drives colors, particles, messages
- Runs locally AND on GitHub Actions
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


# ── Theme pool ─────────────────────────────────────────────────────────────────
ALL_THEMES = [
    {
        "name": "Galaxy & Universe", "slug": "galaxy", "mood": "Emotional, Deep",
        "bg": "radial-gradient(ellipse at 30% 20%,#1a0a2e,#080012 55%,#000008)",
        "primary": "#ff6b9d", "secondary": "#c44dff", "glow": "255,107,157",
        "emojis": ["💗","✨","💫","🌸","⭐","💕","🌟","🪐","💖"],
        "mechanic": "starhunt",
        "hunt_label": "Find all 7 hidden stars ✦",
        "unlock_emoji": "💗",
        "message": [
            "Of all the stars in this universe,",
            "you are the one that makes the whole sky make sense.",
            "",
            "Every time I think of you, it feels like",
            "watching a constellation appear for the first time —",
            "<em>breathtaking, extraordinary, and rare.</em>",
            "",
            "This universe became more beautiful",
            f"the moment you were in it, <strong>Jenisha.</strong>",
        ],
        "btn_text": "✨ Send Love Back ✨",
    },
    {
        "name": "Cherry Blossom", "slug": "sakura", "mood": "Loving, Gentle",
        "bg": "linear-gradient(160deg,#1a0812,#2d0a1a 40%,#0d0810)",
        "primary": "#ffb7d5", "secondary": "#ff7eb3", "glow": "255,150,200",
        "emojis": ["🌸","💗","🌷","✨","🌺","💕","🍃","🌼","💖"],
        "mechanic": "starhunt",
        "hunt_label": "Find 7 hidden blossoms 🌸",
        "unlock_emoji": "🌸",
        "message": [
            "Cherry blossoms fall for just a week —",
            "brief, beautiful, impossible to look away from.",
            "",
            "That's what it's like when you smile.",
            "<em>Everything else stops.</em>",
            "",
            "You are the kind of beautiful",
            f"that seasons are named after, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🌸 Bloom Together 🌸",
    },
    {
        "name": "Ocean Waves", "slug": "ocean", "mood": "Romantic, Peaceful",
        "bg": "radial-gradient(ellipse at 50% 100%,#001a33,#000c1a 50%,#00070f)",
        "primary": "#4fc3f7", "secondary": "#0288d1", "glow": "79,195,247",
        "emojis": ["🌊","💙","✨","🐚","💎","🌟","💗","🫧","🪸"],
        "mechanic": "starhunt",
        "hunt_label": "Collect 7 hidden sea stars 🌊",
        "unlock_emoji": "🌊",
        "message": [
            "The ocean doesn't apologize for its depth.",
            "It doesn't shrink for anyone.",
            "",
            "<em>Neither do you.</em>",
            "",
            "You are vast and moving and full of things",
            "that take your breath away the more you explore —",
            f"and I want to spend a lifetime exploring, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🌊 Ride the Wave 🌊",
    },
    {
        "name": "Firefly Forest", "slug": "firefly", "mood": "Dreamy, Magical",
        "bg": "radial-gradient(ellipse at 50% 80%,#0a1a08,#050e04 50%,#020602)",
        "primary": "#b8ff6e", "secondary": "#7bcc2a", "glow": "184,255,110",
        "emojis": ["✨","💛","🌿","🍃","⭐","💚","🌟","🌙","💫"],
        "mechanic": "starhunt",
        "hunt_label": "Catch 7 fireflies in the dark 🌿",
        "unlock_emoji": "🌿",
        "message": [
            "In the quietest part of the forest,",
            "fireflies make the dark worth staying in.",
            "",
            "<em>You do that.</em>",
            "",
            "You make the ordinary world glow",
            "with something I can't explain —",
            f"only feel, deeply, <strong>Jenisha.</strong>",
        ],
        "btn_text": "✨ Light Up the Night ✨",
    },
    {
        "name": "Neon Glow", "slug": "neon", "mood": "Flirty, Fun",
        "bg": "linear-gradient(135deg,#0a0015,#15002a,#0a000f)",
        "primary": "#ff2d78", "secondary": "#00ffcc", "glow": "255,45,120",
        "emojis": ["💗","⚡","🔥","💋","✨","💥","🌟","💫","🎯"],
        "mechanic": "starhunt",
        "hunt_label": "Find 7 glowing signals 💥",
        "unlock_emoji": "⚡",
        "message": [
            "Warning: prolonged exposure to you",
            "causes excessive smiling,",
            "loss of focus on everything else,",
            "",
            "<em>and an inability to stop thinking about you.</em>",
            "",
            "Side effects are permanent.",
            f"No cure wanted, <strong>Jenisha.</strong>",
        ],
        "btn_text": "⚡ Spark It Back ⚡",
    },
    {
        "name": "Aurora Borealis", "slug": "aurora", "mood": "Breathtaking",
        "bg": "linear-gradient(180deg,#000810,#001020 50%,#000508)",
        "primary": "#00ffcc", "secondary": "#7b2fff", "glow": "0,255,204",
        "emojis": ["🌌","💚","💜","✨","🌟","💗","🫧","⭐","💫"],
        "mechanic": "starhunt",
        "hunt_label": "Discover 7 aurora fragments 🌌",
        "unlock_emoji": "🌌",
        "message": [
            "The aurora only appears when the conditions",
            "are exactly right — rare, specific, unrepeatable.",
            "",
            "<em>So are you.</em>",
            "",
            "I have seen a lot of things.",
            "Nothing comes close to the feeling",
            f"of knowing you exist, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🌌 Paint the Sky 🌌",
    },
    {
        "name": "Sunrise", "slug": "sunrise", "mood": "Hopeful, Warm",
        "bg": "linear-gradient(180deg,#0a0400,#2a0e00 30%,#5a1e00 60%,#8a3000)",
        "primary": "#ffb347", "secondary": "#ff6b35", "glow": "255,160,60",
        "emojis": ["🌅","☀️","✨","🌤️","💛","🌸","💗","🌻","⭐"],
        "mechanic": "starhunt",
        "hunt_label": "Gather 7 rays of golden light 🌅",
        "unlock_emoji": "🌅",
        "message": [
            "Every morning the world gets a second chance —",
            "warm, golden, quietly full of hope.",
            "",
            "<em>That's what you feel like.</em>",
            "",
            "Like a sunrise I never get tired of watching.",
            "Every day is softer",
            f"just because you're in it, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🌅 Brighten My Day 🌅",
    },
    {
        "name": "Rain on Window", "slug": "rain", "mood": "Cozy, Emotional",
        "bg": "linear-gradient(160deg,#060b14,#0a1020 50%,#060810)",
        "primary": "#7eb8e8", "secondary": "#4a90d9", "glow": "126,184,232",
        "emojis": ["🌧️","💙","💗","🫧","✨","🌊","💎","🌟","💕"],
        "mechanic": "starhunt",
        "hunt_label": "Find 7 raindrops in the dark 🌧️",
        "unlock_emoji": "🌧️",
        "message": [
            "There's a specific kind of peace",
            "that comes with rain on a window —",
            "the world outside blurring into something soft.",
            "",
            "<em>You give me that.</em>",
            "",
            "A quiet comfort I didn't know I needed",
            f"until I found you, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🌧️ Stay Cozy 🌧️",
    },
    {
        "name": "Particle Heart", "slug": "particle", "mood": "Dramatic, Loving",
        "bg": "radial-gradient(ellipse at 50% 50%,#1a0010,#0d0008 50%,#050005)",
        "primary": "#ff1464", "secondary": "#ff6b9d", "glow": "255,20,100",
        "emojis": ["💗","💖","💕","💝","❤️","🌹","✨","💘","💓"],
        "mechanic": "starhunt",
        "hunt_label": "Find 7 fragments of a broken heart 💗",
        "unlock_emoji": "💗",
        "message": [
            "A heart doesn't break all at once.",
            "It cracks slowly, quietly,",
            "in all the places where love was supposed to live.",
            "",
            "<em>But it also heals that way —</em>",
            "slowly, quietly, one moment at a time.",
            "",
            f"You are every moment it's been healing, <strong>Jenisha.</strong>",
        ],
        "btn_text": "💗 Send My Heart 💗",
    },
    {
        "name": "Matrix Love", "slug": "matrix", "mood": "Bold, Unique",
        "bg": "linear-gradient(135deg,#000800,#001200,#000500)",
        "primary": "#00ff41", "secondary": "#00cc33", "glow": "0,255,65",
        "emojis": ["💚","⚡","🔮","✨","💫","🌟","💗","🎯","🔥"],
        "mechanic": "starhunt",
        "hunt_label": "Decode 7 encrypted signals 🔮",
        "unlock_emoji": "🔮",
        "message": [
            "In a world of endless noise and simulation,",
            "some things are irreducibly real —",
            "",
            "<em>the way I feel when I think of you</em>",
            "is one of them.",
            "",
            "No algorithm predicts it.",
            "No code describes it.",
            f"Only your name explains it, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🔮 Enter the Code 🔮",
    },
    {
        "name": "Butterfly Garden", "slug": "butterfly", "mood": "Playful, Cute",
        "bg": "radial-gradient(ellipse at 40% 30%,#0a0a18,#050510 55%,#020208)",
        "primary": "#f9a8d4", "secondary": "#a78bfa", "glow": "249,168,212",
        "emojis": ["🦋","🌸","💜","🌺","✨","💗","🌼","🪻","💕"],
        "mechanic": "starhunt",
        "hunt_label": "Chase 7 hidden butterflies 🦋",
        "unlock_emoji": "🦋",
        "message": [
            "Butterflies don't try to be beautiful.",
            "They just emerge and the world stops",
            "to stare.",
            "",
            "<em>You do that without trying.</em>",
            "",
            "You walk into a room and the whole place",
            f"quietly rearranges itself around you, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🦋 Flutter My Heart 🦋",
    },
    {
        "name": "Campfire & Stars", "slug": "campfire", "mood": "Cozy, Romantic",
        "bg": "radial-gradient(ellipse at 50% 90%,#1a0800,#0d0500 50%,#050200)",
        "primary": "#ff8c42", "secondary": "#ffcc70", "glow": "255,140,66",
        "emojis": ["🔥","⭐","🌟","✨","🌙","💗","🪵","💛","🌾"],
        "mechanic": "starhunt",
        "hunt_label": "Find 7 embers in the dark 🔥",
        "unlock_emoji": "🔥",
        "message": [
            "There's something about a campfire —",
            "the way it pulls people close,",
            "the way the cold disappears.",
            "",
            "<em>Talking to you feels like that.</em>",
            "",
            "Warm. Safe. No place I'd rather be",
            f"than right here, with you, <strong>Jenisha.</strong>",
        ],
        "btn_text": "🔥 Keep Me Warm 🔥",
    },
]


# ── Format rotation ─────────────────────────────────────────────────────────────
def get_format(ordinal):
    """Returns 'interactive', 'email', or 'qr'"""
    if ordinal % 11 == 0:
        return "email"
    if ordinal % 7 == 0:
        return "qr"
    return "interactive"


# ── Interactive star-hunt page ──────────────────────────────────────────────────
def html_interactive(theme, name, date_str):
    p = theme["primary"]
    s = theme["secondary"]
    g = theme["glow"]
    bg = theme["bg"]
    emojis_js = json.dumps(theme["emojis"])
    unlock_emoji = theme["unlock_emoji"]
    hunt_label = theme["hunt_label"]
    btn_text = theme["btn_text"]
    msg_lines = theme["message"]
    # Build message HTML
    msg_html = ""
    for line in msg_lines:
        if line == "":
            msg_html += "<br>"
        else:
            msg_html += line + "<br>"

    # 7 star positions: (left%, top%, size_rem, opacity, color, twinkle_speed)
    stars_config = [
        (13, 17, 2.0, 0.92, p,  3.5),
        (78, 11, 1.4, 0.55, s,  4.2),
        (62, 74, 1.8, 0.78, p,  2.9),
        (22, 82, 1.2, 0.38, s,  5.1),
        (88, 55, 1.6, 0.65, p,  3.8),
        (45, 38, 1.0, 0.22, s,  6.3),  # hardest — nearly invisible
        (35, 91, 1.4, 0.48, p,  4.7),
    ]
    stars_html = ""
    for i, (lft, top, sz, op, col, tw) in enumerate(stars_config):
        stars_html += (
            f'<div class="cstar" id="cs{i}" '
            f'style="left:{lft}%;top:{top}%;--sz:{sz}rem;--op:{op};--col:{col};--tw:{tw}s" '
            f'onclick="collect({i})">✦</div>\n'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no"/>
<title>For {name} ✦</title>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Raleway:ital,wght@0,200;0,300;0,400;1,300&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;background:{bg};overflow:hidden;font-family:'Raleway',sans-serif;cursor:none}}
canvas{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none}}
#bg{{z-index:1}}#fx{{z-index:6}}
.cur{{position:fixed;z-index:999;width:16px;height:16px;border-radius:50%;background:radial-gradient(circle,rgba({g},.9),transparent 70%);pointer-events:none;transform:translate(-50%,-50%);transition:transform .08s;mix-blend-mode:screen}}
.cstar{{position:fixed;z-index:10;font-size:var(--sz,1.5rem);opacity:var(--op,.7);color:var(--col,{p});text-shadow:0 0 12px var(--col),0 0 28px var(--col);cursor:pointer;user-select:none;transition:transform .15s,opacity .15s,filter .15s;animation:twinkle var(--tw,3.5s) ease-in-out infinite;transform:translate(-50%,-50%)}}
.cstar:hover{{transform:translate(-50%,-50%) scale(1.7)!important;opacity:1!important;filter:brightness(2)}}
.cstar.gone{{display:none}}
@keyframes twinkle{{0%,100%{{filter:brightness(1)}}50%{{filter:brightness(1.5) drop-shadow(0 0 8px var(--col))}}}}
.hub{{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);width:130px;height:130px;z-index:15;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;transition:opacity .8s ease}}
.prog-svg{{position:absolute;width:130px;height:130px;overflow:visible}}
.lock{{font-size:2.4rem;z-index:2;animation:lockPulse 2.2s ease-in-out infinite;filter:drop-shadow(0 0 10px rgba({g},.5))}}
.counter{{font-size:.65rem;font-weight:300;letter-spacing:.25em;color:rgba({g},.6);z-index:2}}
.dots{{display:flex;gap:5px;z-index:2}}
.dot{{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.15);border:1px solid rgba({g},.3);transition:all .35s}}
.dot.lit{{background:{p};border-color:{p};box-shadow:0 0 8px rgba({g},.8)}}
@keyframes lockPulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.08)}}}}
@keyframes lockShake{{0%,100%{{transform:scale(1) rotate(0deg)}}15%{{transform:scale(1.1) rotate(-8deg)}}30%{{transform:scale(1.1) rotate(8deg)}}45%{{transform:scale(1.05) rotate(-5deg)}}60%{{transform:scale(1.05) rotate(5deg)}}}}
.hint{{position:fixed;bottom:28px;left:50%;transform:translateX(-50%);font-size:.65rem;letter-spacing:.25em;color:rgba({g},.45);z-index:20;pointer-events:none;text-align:center;animation:hintPulse 3s ease-in-out infinite}}
@keyframes hintPulse{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}
.card-wrap{{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:24px;opacity:0;pointer-events:none;transition:opacity 1s ease}}
.card-wrap.visible{{opacity:1;pointer-events:all}}
.card{{background:rgba(10,5,20,.92);border:1px solid rgba({g},.25);border-radius:20px;padding:clamp(28px,5vw,52px) clamp(24px,5vw,48px);max-width:min(520px,92vw);text-align:center;color:#fff;box-shadow:0 0 60px rgba({g},.12),inset 0 1px 0 rgba({g},.1);backdrop-filter:blur(16px);transform-style:preserve-3d;will-change:transform;transition:box-shadow .1s}}
.card-name{{font-family:'Dancing Script',cursive;font-size:clamp(2.2rem,8vw,3.6rem);font-weight:700;color:{p};text-shadow:0 0 30px rgba({g},.5);margin-bottom:8px}}
.card-line{{width:60px;height:1.5px;background:linear-gradient(90deg,transparent,{p},transparent);margin:0 auto 24px}}
.card-msg{{font-size:clamp(.85rem,2.2vw,1.05rem);font-weight:300;line-height:1.95;color:rgba(255,255,255,.85);min-height:4em}}
.card-msg em{{color:{p};font-style:italic}}
.card-msg strong{{font-weight:500;color:{s}}}
.card-btn{{margin-top:28px;background:transparent;border:1.5px solid rgba({g},.4);color:#fff;font-family:'Raleway',sans-serif;font-size:.82rem;font-weight:400;letter-spacing:.22em;text-transform:uppercase;padding:13px 36px;border-radius:50px;cursor:pointer;backdrop-filter:blur(8px);transition:all .3s}}
.card-btn:hover{{border-color:{p};box-shadow:0 0 24px rgba({g},.5);transform:translateY(-2px)}}
.ds{{position:fixed;bottom:14px;right:16px;font-size:.62rem;letter-spacing:.15em;color:rgba({g},.25);z-index:60}}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<canvas id="fx"></canvas>
<div class="cur" id="cur"></div>

{stars_html}

<div class="hub" id="hub">
  <svg class="prog-svg" viewBox="0 0 130 130">
    <circle cx="65" cy="65" r="56" fill="none" stroke="rgba({g},.12)" stroke-width="3"/>
    <circle id="arc" cx="65" cy="65" r="56" fill="none" stroke="{p}"
      stroke-width="3" stroke-linecap="round"
      stroke-dasharray="351.86" stroke-dashoffset="351.86"
      transform="rotate(-90 65 65)"
      style="transition:stroke-dashoffset .5s ease,filter .3s"/>
  </svg>
  <div class="lock" id="lockIcon">🔒</div>
  <div class="dots" id="dots">
    {''.join(f'<div class="dot" id="d{i}"></div>' for i in range(7))}
  </div>
  <div class="counter" id="ctr">0 / 7</div>
</div>

<div class="hint" id="hint">{hunt_label}</div>

<div class="card-wrap" id="cardWrap">
  <div class="card" id="card">
    <div class="card-name">{name}</div>
    <div class="card-line"></div>
    <div class="card-msg" id="cardMsg"></div>
    <button class="card-btn" onclick="sendLoveBack()">{btn_text}</button>
  </div>
</div>

<div class="ds">{date_str}</div>

<script>
// ── Background ──
const bgC=document.getElementById('bg'),bgX=bgC.getContext('2d');
const fxC=document.getElementById('fx'),fxX=fxC.getContext('2d');
let W=bgC.width=fxC.width=window.innerWidth,H=bgC.height=fxC.height=window.innerHeight;

const STARS=Array.from({{length:340}},()=>{{
  return{{x:Math.random()*W,y:Math.random()*H,r:.15+Math.random()*1.8,
    base:.15+Math.random()*.7,tp:Math.random()*Math.PI*2,ts:.003+Math.random()*.015,
    vx:(Math.random()-.5)*.05,vy:(Math.random()-.5)*.05}};
}});
let mx=0,my=0;
function drawBg(){{
  bgX.clearRect(0,0,W,H);
  STARS.forEach(s=>{{
    s.tp+=s.ts;s.x+=s.vx+mx*.01;s.y+=s.vy+my*.01;
    if(s.x<0)s.x=W;if(s.x>W)s.x=0;if(s.y<0)s.y=H;if(s.y>H)s.y=0;
    const op=Math.max(.05,Math.min(1,s.base+Math.sin(s.tp)*.25));
    bgX.beginPath();bgX.arc(s.x,s.y,s.r,0,Math.PI*2);
    bgX.fillStyle=`rgba(255,255,255,${{op}})`;bgX.fill();
  }});
  requestAnimationFrame(drawBg);
}}
drawBg();

// ── Particles ──
const EMOJIS={emojis_js};
const parts=[];
class P{{
  constructor(x,y,burst){{
    this.x=x;this.y=y;this.em=EMOJIS[Math.floor(Math.random()*EMOJIS.length)];
    if(burst){{this.vx=(Math.random()-.5)*16;this.vy=(Math.random()-.8)*18;this.g=.32;this.decay=.012+Math.random()*.012;this.sz=14+Math.random()*20;}}
    else{{this.vx=(Math.random()-.5)*1.2;this.vy=-(Math.random()*1.5+.5);this.g=-.006;this.decay=.002+Math.random()*.002;this.sz=8+Math.random()*12;}}
    this.rot=Math.random()*Math.PI*2;this.rs=(Math.random()-.5)*.1;this.life=1;
  }}
  tick(){{this.x+=this.vx;this.y+=this.vy;this.vy+=this.g;this.vx*=.985;this.rot+=this.rs;this.life-=this.decay;}}
  draw(){{fxX.save();fxX.globalAlpha=Math.max(0,this.life);fxX.translate(this.x,this.y);fxX.rotate(this.rot);fxX.font=`${{this.sz}}px Arial`;fxX.textAlign='center';fxX.textBaseline='middle';fxX.fillText(this.em,0,0);fxX.restore();}}
}}
let ambT=0;
function drawFx(t){{
  fxX.clearRect(0,0,W,H);
  if(t-ambT>1800){{parts.push(new P(Math.random()*W,H+20,false));ambT=t;}}
  for(let i=parts.length-1;i>=0;i--){{parts[i].tick();parts[i].draw();if(parts[i].life<=0)parts.splice(i,1);}}
  requestAnimationFrame(drawFx);
}}
requestAnimationFrame(drawFx);

function burst(x,y,n){{for(let i=0;i<n;i++)setTimeout(()=>parts.push(new P(x,y,true)),i*12);}}

// ── Cursor ──
const cur=document.getElementById('cur');
document.addEventListener('mousemove',e=>{{
  cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px';
  mx=(e.clientX-W/2)/W*2;my=(e.clientY-H/2)/H*2;
}});

// ── Star hunt ──
let collected=0;
const TOTAL=7;
const arc=document.getElementById('arc');
const FULL=351.86;

function collect(i){{
  const el=document.getElementById('cs'+i);
  if(!el||el.classList.contains('gone'))return;
  el.classList.add('gone');

  // fly clone to hub
  const r=el.getBoundingClientRect();
  const clone=el.cloneNode(true);
  clone.style.cssText=`position:fixed;left:${{r.left}}px;top:${{r.top}}px;z-index:30;transition:all .55s cubic-bezier(.4,0,.2,1);opacity:1;pointer-events:none;font-size:${{parseFloat(getComputedStyle(el).getPropertyValue('--sz'))}}rem`;
  document.body.appendChild(clone);
  burst(r.left+r.width/2,r.top+r.height/2,10);
  requestAnimationFrame(()=>{{
    clone.style.left='50%';clone.style.top='50%';
    clone.style.transform='translate(-50%,-50%) scale(.4)';
    clone.style.opacity='0';
  }});
  setTimeout(()=>clone.remove(),600);

  collected++;
  document.getElementById('d'+(collected-1)).classList.add('lit');
  document.getElementById('ctr').textContent=collected+' / '+TOTAL;
  arc.style.strokeDashoffset=FULL-(FULL*collected/TOTAL);
  arc.style.filter='drop-shadow(0 0 6px {p})';

  if(collected===TOTAL)setTimeout(unlock,600);
}}

function unlock(){{
  const hub=document.getElementById('hub');
  const lock=document.getElementById('lockIcon');
  lock.style.animation='lockShake .6s ease';
  setTimeout(()=>{{
    burst(W/2,H/2,30);
    setTimeout(()=>{{burst(W*.3,H*.4,20);burst(W*.7,H*.6,20);}},200);
    lock.textContent='{unlock_emoji}';
    lock.style.animation='lockPulse 1.5s ease-in-out infinite';
    setTimeout(()=>{{hub.style.opacity='0';hub.style.pointerEvents='none';}},800);
    document.getElementById('hint').style.opacity='0';
    setTimeout(showCard,1400);
  }},650);
}}

// ── Card reveal ──
const MSG=`{msg_html}`;
function typewrite(el,html,speed){{
  const tmp=document.createElement('div');tmp.innerHTML=html;
  const text=tmp.textContent;
  let i=0;el.innerHTML='';
  const iv=setInterval(()=>{{
    if(i>=text.length){{el.innerHTML=html;clearInterval(iv);return;}}
    el.textContent=text.slice(0,++i);
  }},speed);
}}
function showCard(){{
  const cw=document.getElementById('cardWrap');
  cw.classList.add('visible');
  setTimeout(()=>typewrite(document.getElementById('cardMsg'),MSG,38),400);
}}

// ── 3D card tilt ──
const card=document.getElementById('card');
document.addEventListener('mousemove',e=>{{
  if(!document.getElementById('cardWrap').classList.contains('visible'))return;
  const rect=card.getBoundingClientRect();
  const cx=rect.left+rect.width/2,cy=rect.top+rect.height/2;
  const dx=(e.clientX-cx)/rect.width,dy=(e.clientY-cy)/rect.height;
  const tX=dx*14,tY=dy*-14;
  card.style.transform=`perspective(900px) rotateY(${{tX}}deg) rotateX(${{tY}}deg)`;
  card.style.boxShadow=`${{-tX*1.5}}px ${{tY*1.5}}px 60px rgba({g},.18),0 0 80px rgba({g},.08)`;
}});
document.addEventListener('mouseleave',()=>{{
  card.style.transform='perspective(900px) rotateY(0deg) rotateX(0deg)';
}});
// touch tilt
document.addEventListener('touchmove',e=>{{
  if(!document.getElementById('cardWrap').classList.contains('visible'))return;
  const t=e.touches[0];
  const rect=card.getBoundingClientRect();
  const cx=rect.left+rect.width/2,cy=rect.top+rect.height/2;
  const tX=(t.clientX-cx)/rect.width*12,tY=(t.clientY-cy)/rect.height*-12;
  card.style.transform=`perspective(900px) rotateY(${{tX}}deg) rotateX(${{tY}}deg)`;
}},{{passive:true}});

function sendLoveBack(){{
  for(let i=0;i<5;i++)setTimeout(()=>burst(Math.random()*W,Math.random()*H*.8,18),i*160);
}}

window.addEventListener('resize',()=>{{
  W=bgC.width=fxC.width=window.innerWidth;
  H=bgC.height=fxC.height=window.innerHeight;
}});
</script>
</body>
</html>"""


# ── Flirty professional email format ───────────────────────────────────────────
def html_email(theme, name, date_str):
    p = theme["primary"]
    s = theme["secondary"]
    g = theme["glow"]

    # Random "from" details
    subjects = [
        f"RE: RE: RE: You — a follow-up",
        f"Action Required: You Are Too Beautiful",
        f"FWD: Thinking About You Again",
        f"URGENT: I Miss You",
        f"Monthly Review: Why You're Extraordinary",
        f"Reminder: You Are My Favourite Person",
    ]
    import hashlib
    day_hash = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    subject = subjects[day_hash % len(subjects)]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>For {name} — 1 New Message</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Dancing+Script:wght@700&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0e0e12;font-family:'Inter',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:16px}}
.shell{{width:min(780px,100%);background:#141418;border-radius:12px;overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.06)}}
.topbar{{background:#1a1a20;padding:14px 20px;display:flex;align-items:center;gap:12px;border-bottom:1px solid rgba(255,255,255,.06)}}
.dots span{{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:6px}}
.dots .r{{background:#ff5f56}}.dots .y{{background:#ffbd2e}}.dots .gr{{background:#27c93f}}
.topbar-title{{flex:1;text-align:center;font-size:.78rem;color:rgba(255,255,255,.35);letter-spacing:.08em}}
.sidebar{{display:flex}}
.nav{{background:#111115;width:200px;min-width:200px;padding:20px 0;border-right:1px solid rgba(255,255,255,.05);display:flex;flex-direction:column;gap:2px}}
.nav-item{{padding:9px 20px;font-size:.8rem;color:rgba(255,255,255,.35);cursor:pointer;display:flex;align-items:center;gap:10px;border-radius:0;transition:background .2s}}
.nav-item.active{{background:rgba({g},.1);color:{p};border-left:2px solid {p}}}
.badge{{background:{p};color:#000;font-size:.6rem;font-weight:700;padding:1px 6px;border-radius:10px;margin-left:auto}}
.main{{flex:1;display:flex;flex-direction:column}}
.thread-header{{padding:22px 28px 16px;border-bottom:1px solid rgba(255,255,255,.06)}}
.subject{{font-size:1.15rem;font-weight:600;color:rgba(255,255,255,.92);margin-bottom:8px}}
.meta{{display:flex;gap:8px;flex-wrap:wrap;font-size:.75rem;color:rgba(255,255,255,.35)}}
.tag{{background:rgba({g},.12);color:{p};padding:2px 10px;border-radius:10px;font-size:.68rem}}
.email-body{{padding:28px;flex:1}}
.from-row{{display:flex;align-items:center;gap:12px;margin-bottom:24px}}
.avatar{{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,{p},{s});display:flex;align-items:center;justify-content:center;font-family:'Dancing Script',cursive;font-weight:700;font-size:1.2rem;color:#000;flex-shrink:0}}
.from-info .name{{font-size:.88rem;font-weight:500;color:rgba(255,255,255,.85)}}
.from-info .addr{{font-size:.72rem;color:rgba(255,255,255,.3);margin-top:1px}}
.timestamp{{margin-left:auto;font-size:.7rem;color:rgba(255,255,255,.25)}}
.letter{{font-size:.9rem;line-height:1.9;color:rgba(255,255,255,.75);white-space:pre-line}}
.letter .salutation{{font-size:1.05rem;font-weight:500;color:rgba(255,255,255,.9);margin-bottom:16px}}
.letter .highlight{{color:{p};font-style:italic}}
.letter .closing{{margin-top:20px;font-size:.88rem;color:rgba(255,255,255,.6)}}
.letter .sig{{font-family:'Dancing Script',cursive;font-size:1.5rem;color:{p};margin-top:6px}}
.actions{{padding:16px 28px;border-top:1px solid rgba(255,255,255,.06);display:flex;gap:10px}}
.btn{{background:transparent;border:1px solid rgba({g},.35);color:{p};font-family:'Inter',sans-serif;font-size:.75rem;letter-spacing:.1em;padding:9px 20px;border-radius:8px;cursor:pointer;transition:all .25s}}
.btn:hover{{background:rgba({g},.1);border-color:{p};box-shadow:0 0 16px rgba({g},.25)}}
.btn.primary{{background:rgba({g},.15);border-color:{p}}}
.notification{{position:fixed;top:20px;right:20px;background:#1e1e24;border:1px solid rgba({g},.3);border-radius:10px;padding:14px 18px;font-size:.78rem;color:rgba(255,255,255,.7);box-shadow:0 8px 32px rgba(0,0,0,.4);opacity:0;transform:translateY(-8px);transition:all .4s;z-index:100;max-width:260px}}
.notification.show{{opacity:1;transform:translateY(0)}}
.notification .nhead{{color:{p};font-weight:500;margin-bottom:3px}}
@media(max-width:600px){{.nav{{display:none}}.topbar-title{{font-size:.68rem}}}}
</style>
</head>
<body>
<div class="shell">
  <div class="topbar">
    <div class="dots"><span class="r"></span><span class="y"></span><span class="gr"></span></div>
    <div class="topbar-title">💗 Inbox — 1 Unread</div>
  </div>
  <div class="sidebar">
    <div class="nav">
      <div class="nav-item active">📥 Inbox <span class="badge">1</span></div>
      <div class="nav-item">⭐ Starred</div>
      <div class="nav-item">📤 Sent</div>
      <div class="nav-item">💗 Loved</div>
      <div class="nav-item">📁 Archive</div>
    </div>
    <div class="main">
      <div class="thread-header">
        <div class="subject">{subject}</div>
        <div class="meta">
          <span class="tag">💗 Personal</span>
          <span class="tag">⭐ Important</span>
          <span>{date_str}</span>
        </div>
      </div>
      <div class="email-body">
        <div class="from-row">
          <div class="avatar">D</div>
          <div class="from-info">
            <div class="name">Dipesh Ray G</div>
            <div class="addr">dipesh.ray.g@gmail.com</div>
          </div>
          <div class="timestamp">Today, just now</div>
        </div>
        <div class="letter">
<span class="salutation">Dear {name},</span>
I am reaching out to formally notify you of several unresolved matters
that have been pending on my end for some time.

First and most critically: <span class="highlight">you have been on my mind constantly,</span>
and I have been unable to resolve this through normal channels.
I have tried distraction, productivity, and reasonable prioritisation.
None of these have worked.

Upon review, I believe the root cause is that you are, objectively,
<span class="highlight">too wonderful to simply stop thinking about.</span>
This is not a complaint. This is a formal acknowledgment.

Additionally, I would like to flag that your smile constitutes
an unreasonable interruption to my cognitive workflow.
Further investigation is recommended (preferably in person).

Please consider this message a standing invitation —
for coffee, for conversation, for any format that gets me
<span class="highlight">a little more of your time.</span>

I look forward to your earliest possible reply.

<span class="closing">With the highest professional regard (and considerably more),</span>
<span class="sig">Dipesh</span>
<span style="font-size:.72rem;color:rgba(255,255,255,.25);margin-top:4px;display:block">— {date_str}</span>
        </div>
      </div>
      <div class="actions">
        <button class="btn primary" onclick="reply()">💗 Reply with Love</button>
        <button class="btn" onclick="forward()">✨ Forward to My Heart</button>
        <button class="btn" onclick="archive()">⭐ Star This</button>
      </div>
    </div>
  </div>
</div>
<div class="notification" id="notif">
  <div class="nhead">💗 Message Delivered</div>
  <div id="notifMsg">Preparing response...</div>
</div>
<script>
const replies=[
  "Reply sent: 'Read & felt every word 💗'",
  "Forwarded to: every corner of my heart ✨",
  "Starred ⭐ — permanently unforgettable",
  "Marked as: My Favourite Email Ever 💕",
  "Auto-reply set: 'Same. Always.' 🌸",
];
let ri=0;
function showNotif(msg){{
  const n=document.getElementById('notif');
  document.getElementById('notifMsg').textContent=msg;
  n.classList.add('show');
  setTimeout(()=>n.classList.remove('show'),3000);
}}
function reply(){{showNotif(replies[ri++%replies.length]);}}
function forward(){{showNotif("Forwarded to: every corner of my heart ✨");}}
function archive(){{showNotif("Starred ⭐ — permanently unforgettable");}}
</script>
</body>
</html>"""


# ── Heart QR code format ────────────────────────────────────────────────────────
def html_qr(theme, name, date_str, url):
    p = theme["primary"]
    s = theme["secondary"]
    g = theme["glow"]
    bg = theme["bg"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>For {name} — Scan Me 💗</title>
<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Raleway:wght@300;400&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"><\/script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{bg};min-height:100vh;font-family:'Raleway',sans-serif;color:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.scene{{display:flex;flex-direction:column;align-items:center;gap:28px;padding:32px;text-align:center;z-index:10;position:relative}}
.title{{font-family:'Dancing Script',cursive;font-size:clamp(2.5rem,9vw,5rem);color:{p};text-shadow:0 0 30px rgba({g},.5);opacity:0;animation:fadeUp 1s ease forwards .5s}}
.sub{{font-size:.75rem;letter-spacing:.4em;text-transform:uppercase;color:rgba({g},.5);opacity:0;animation:fadeUp 1s ease forwards 1.2s}}
.heart-wrap{{position:relative;width:260px;height:260px;opacity:0;animation:fadeUp 1.2s ease forwards 1.8s}}
#heartCanvas{{position:absolute;top:0;left:0}}
#qrCanvas{{display:none}}
.caption{{font-size:.8rem;font-weight:300;line-height:1.8;color:rgba(255,255,255,.65);max-width:320px;opacity:0;animation:fadeUp 1s ease forwards 2.8s}}
.caption em{{color:{p}}}
.pulse{{animation:pulse 2s ease-in-out infinite 3s}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.04)}}}}
canvas#bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;pointer-events:none}}
.scene{{z-index:10}}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<div class="scene">
  <div class="title">{name}</div>
  <div class="sub">scan this with your heart</div>
  <div class="heart-wrap pulse">
    <canvas id="qrCanvas" width="200" height="200"></canvas>
    <canvas id="heartCanvas" width="260" height="260"></canvas>
  </div>
  <div class="caption">
    A secret message lives inside this heart.<br>
    <em>Point your camera at it to open it.</em><br>
    <br>
    Made just for you — {date_str}
  </div>
</div>
<script>
// Draw background stars
const bg=document.getElementById('bg'),bx=bg.getContext('2d');
let W=bg.width=window.innerWidth,H=bg.height=window.innerHeight;
const ST=Array.from({{length:280}},()=>{{return{{x:Math.random()*W,y:Math.random()*H,r:.1+Math.random()*1.6,op:Math.random()*.6+.2,tp:Math.random()*Math.PI*2,ts:.004+Math.random()*.01}}}});
function drawBg(){{bx.clearRect(0,0,W,H);ST.forEach(s=>{{s.tp+=s.ts;const op=Math.max(.05,s.op+Math.sin(s.tp)*.2);bx.beginPath();bx.arc(s.x,s.y,s.r,0,Math.PI*2);bx.fillStyle=`rgba(255,255,255,${{op}})`;bx.fill()}});requestAnimationFrame(drawBg);}}
drawBg();

// Generate QR then draw heart-clipped version
const TARGET_URL = "{url}";
const qrC=document.getElementById('qrCanvas');
const hC=document.getElementById('heartCanvas');
const hX=hC.getContext('2d');
const S=260;

QRCode.toCanvas(qrC,TARGET_URL,{{width:200,margin:1,color:{{dark:'#000000',light:'#ffffff'}}}},function(err){{
  if(err)return;
  drawHeartQR();
}});

function heartPath(ctx,cx,cy,size){{
  const s=size/2;
  ctx.beginPath();
  ctx.moveTo(cx,cy+s*.4);
  ctx.bezierCurveTo(cx,cy,cx-s*1.2,cy-s*.6,cx-s*1.2,cy-s*.1);
  ctx.bezierCurveTo(cx-s*1.2,cy-s*.8,cx,cy-s*.8,cx,cy-s*.2);
  ctx.bezierCurveTo(cx,cy-s*.8,cx+s*1.2,cy-s*.8,cx+s*1.2,cy-s*.1);
  ctx.bezierCurveTo(cx+s*1.2,cy-s*.6,cx,cy,cx,cy+s*.4);
  ctx.closePath();
}}

function drawHeartQR(){{
  // clear
  hX.clearRect(0,0,S,S);

  // glow background heart
  const grd=hX.createRadialGradient(S/2,S/2,10,S/2,S/2,S*.55);
  grd.addColorStop(0,'rgba({g},.3)');
  grd.addColorStop(1,'rgba({g},0)');
  hX.fillStyle=grd;
  hX.fillRect(0,0,S,S);

  // clip to heart
  heartPath(hX,S/2,S/2+10,S*.8);
  hX.save();
  hX.clip();

  // draw qr code inside heart
  hX.drawImage(qrC,30,40,200,200);

  // color tint over QR
  hX.fillStyle='rgba({p},.18)';
  hX.fillRect(0,0,S,S);
  hX.restore();

  // heart border stroke
  heartPath(hX,S/2,S/2+10,S*.8);
  hX.strokeStyle='{p}';
  hX.lineWidth=3;
  hX.shadowColor='{p}';
  hX.shadowBlur=18;
  hX.stroke();
  hX.shadowBlur=0;
}}

window.addEventListener('resize',()=>{{W=bg.width=window.innerWidth;H=bg.height=window.innerHeight}});
</script>
</body>
</html>"""


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
    fmt        = get_format(ordinal)
    date_str   = today.strftime("%B %d · %Y")
    repo_name  = f"for-jenisha-{today.strftime('%Y%m%d')}"
    page_url   = f"https://{USERNAME}.github.io/{repo_name}/"

    fmt_label = {"interactive": "🎮 Interactive Unlock", "email": "📧 Flirty Email", "qr": "💗 Heart QR Code"}

    print(f"\n{'='*58}")
    print(f"  💗  Daily Love Page — {HER_NAME}")
    print(f"  📅  {date_str}")
    print(f"  🎨  Theme : {theme['name']} ({theme['mood']})")
    print(f"  📐  Format: {fmt_label.get(fmt, fmt)}")
    print(f"  ➡️   Tomorrow: {next_theme['name']} ({next_theme['mood']})")
    print(f"{'='*58}\n")

    # Generate HTML
    if fmt == "email":
        html = html_email(theme, HER_NAME, date_str)
    elif fmt == "qr":
        html = html_qr(theme, HER_NAME, date_str, page_url)
    else:
        html = html_interactive(theme, HER_NAME, date_str)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "index.html").write_text(html, encoding="utf-8")
        print("✅  HTML generated")

        desc = f"For {HER_NAME} — {theme['name']} ({fmt_label.get(fmt,'')}) 💗 {date_str}"
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
        return page_url, theme, next_theme, date_str, repo_name, fmt

if __name__ == "__main__":
    main()
