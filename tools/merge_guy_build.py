#!/usr/bin/env python3
"""Turn a game file from Guy (one big HTML) into the Space Hamster Run web build.

Usage:  python3 tools/merge_guy_build.py GUY_FILE.html OUT_DIR

Writes OUT_DIR/index.html. Every change below is a small, exact text replacement;
if Guy's code changed so that one no longer matches, the script stops and says
which one, instead of guessing. Same pattern as SK8 (noalembersky-pixel/sk8).

What it adds on top of Guy's game (gameplay untouched):
  - page title, description, link previews, icons, home-screen manifest
  - PostHog analytics (cookieless, no autocapture, no recordings), world on every event
  - ?tester=1 marks a browser as internal (is_internal: true)
  - title screen: sound on/off button, FEEDBACK / SHARE / CREDITS links, touch-only hint on phones
  - CREDITS card with Privacy and Help links (Apple needs Privacy reachable in-app)
  - SHARE on the win and game-over cards, SOUND button on the pause card
  - share links: web shares the playable game, store apps share SITE/get/ (SHARE_URL_WEB / SHARE_URL_APP)
  - "needs 3D graphics" message instead of a black screen when WebGL is missing
  - fix: taps on RUN! or a world during the 1.6 s warp animation are ignored
    (before: RUN! mid-warp started the run with the wrong world loaded)
  - Android back button: closes credits, ignored during the warp
  - home lock: runs only on oatmealmorning.com and inside our apps; copies elsewhere
    (or framed by another site) send the player to our site
  - small phones (under 380 px wide): thinner logo outline so the H in HAMSTER keeps its crossbar
"""
import sys, pathlib

src_path, out_dir = sys.argv[1], pathlib.Path(sys.argv[2])
s = open(src_path, encoding='utf-8').read()
out_dir.mkdir(parents=True, exist_ok=True)


def sub(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f'STOP: expected {count} match(es), found {n}, for:\n  {old[:140]!r}')
    s = s.replace(old, new)


SITE = 'https://spacehamster.oatmealmorning.com'
# Google Form for feedback. Empty = the FEEDBACK link opens an email to support@ instead.
FEEDBACK = ''
FEEDBACK_HREF = FEEDBACK or 'mailto:support@oatmealmorning.com?subject=Space%20Hamster%20Run%20feedback'
# Share links (one setting, two values): the web game shares its own playable address;
# the store apps share the /get/ page, which shows the store badges (or "Coming soon").
SHARE_URL_WEB = SITE + '/'
SHARE_URL_APP = SITE + '/get/'
PH_KEY = 'phc_qo4wiAUHZxUNwLi2nGGmHVEUX4cZxUcMNEMy5vxG6jBW'   # shared "Oatmeal Morning apps" project
VERSION = '1.0'

# ---------- 1. page head: meta + analytics ----------
sub('<title>Space Hamster Run</title>', f'''<title>Space Hamster Run — a hamster runner through 5 worlds</title>
<meta name="description" content="Run, jump and grab the nuts through five worlds: space, ocean, cave, sky and the deep sea. Free to play in your browser, made for phones.">
<meta name="theme-color" content="#22104f">
<meta property="og:title" content="Space Hamster Run">
<meta property="og:description" content="Run, jump and grab the nuts through five worlds. Free, plays in your browser.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Space Hamster">
<script>
/* ---- home lock: this file only runs on our own site and inside our apps.
   A copy uploaded anywhere else, or shown inside another site's frame, sends the player to our site. ---- */
(function(){{var H='https://spacehamster.oatmealmorning.com/',h=location.hostname,
 ok=location.protocol==='file:'||h===''||h==='localhost'||h==='127.0.0.1'||h==='appassets.androidplatform.net'||/(^|\\.)oatmealmorning\\.com$/.test(h);
 var framed=false;try{{framed=window.top!==window.self;}}catch(e){{framed=true;}}
 if(ok&&!framed)return;
 try{{if(framed)window.top.location.href=H;else location.replace(H);}}catch(e){{}}
 document.write('<p style="font:18px sans-serif;text-align:center;margin-top:40vh">Play Space Hamster Run at <a href="'+H+'" target="_top">spacehamster.oatmealmorning.com</a></p><plaintext style="display:none">');
}})();
</script>
<script>
/* ---- analytics (PostHog, cookieless, no autocapture, no recordings) ---- */
const PH_KEY = '{PH_KEY}';
window.track = function(){{}};
const SHR_BUILD = {{ platform: 'web', version: '' }};   // app builds rewrite this one line
// SHARE LINKS (one setting): the web game shares its own playable address; the store apps share the /get/ page (store badges, or "Coming soon")
const SHARE_URL = {{ web: '{SHARE_URL_WEB}', app: '{SHARE_URL_APP}' }};
if (PH_KEY) {{
  !function(t,e){{var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){{function g(t,e){{var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){{var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}},u.people.toString=function(){{return u.toString(1)+".people (stub)"}},o="init capture register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group identify setPersonProperties alias".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])}},e.__SV=1)}}(document,window.posthog||[]);
  let shrPid = null;   // app builds only: a random ID kept on the phone so a returning player counts once. The web game keeps no ID.
  if (SHR_BUILD.platform !== 'web') {{ try {{ shrPid = localStorage.getItem('shr-pid'); if (!shrPid) {{ shrPid = 'shr-' + Array.from(crypto.getRandomValues(new Uint8Array(16)), x => ('0' + x.toString(16)).slice(-2)).join(''); localStorage.setItem('shr-pid', shrPid); }} }} catch (e) {{ shrPid = null; }} }}
  posthog.init(PH_KEY, Object.assign({{ api_host: 'https://us.i.posthog.com', persistence: 'memory', capture_pageview: true, capture_pageleave: false, autocapture: false, disable_session_recording: true, disable_surveys: true }}, shrPid ? {{ bootstrap: {{ distinctID: shrPid }} }} : {{}}));
  posthog.register(Object.assign({{ app: 'spacehamster', platform: SHR_BUILD.platform }}, SHR_BUILD.version ? {{ app_version: SHR_BUILD.version }} : {{}}));
  try {{ if (location.search.indexOf('tester=1') > -1) localStorage.setItem('om-tester', '1'); if (localStorage.getItem('om-tester') === '1') posthog.register({{ is_internal: true }}); }} catch (e) {{}}
  window.track = (ev, props, opts) => {{ try {{ posthog.capture(ev, props, opts); }} catch (e) {{}} }};
}}
</script>''')

# ---------- 2. extra styles ----------
sub('</style>\n</head>', '''/* web build additions */
#sndBtn{position:absolute;top:calc(14px + var(--sat,0px));right:14px;width:50px;height:50px;padding:0;font:24px/1 system-ui,sans-serif;letter-spacing:0;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.9);border-width:3px;box-shadow:0 5px 0 #1b0b35}
#sndBtn:active{transform:translateY(4px);box-shadow:0 1px 0 #1b0b35}
.links{margin-top:12px;display:flex;gap:20px;justify-content:center;font-family:Rubik,sans-serif;font-weight:800;font-size:12px;letter-spacing:2px}
.links a,.links button{all:unset;cursor:pointer;color:#7cf0ff;border-bottom:2px solid currentColor;padding-bottom:1px;text-shadow:0 1px 4px rgba(0,0,0,.8)}
#credits .card{box-sizing:border-box;width:calc(100% - 40px);max-width:360px;background:rgba(27,11,53,.94);border:4px solid #1b0b35;border-radius:24px;padding:22px 20px 18px;box-shadow:0 8px 0 #1b0b35,0 0 40px rgba(124,240,255,.15)}
#credits .ttl{font-family:'Luckiest Guy';font-size:34px;line-height:.95;color:#ffd166;-webkit-text-stroke:2px #1b0b35;text-shadow:0 4px 0 #000}
#credits .ttl span{color:#ff8fab;display:block}
.cr{display:grid;grid-template-columns:auto 1fr;gap:9px 14px;text-align:left;font-size:13px;line-height:1.35;margin:16px 0 6px}
.cr b{font-family:'Luckiest Guy';font-weight:400;letter-spacing:1px;color:#ffd166;font-size:13px;padding-top:1px;white-space:nowrap}
.cr span{min-width:0;overflow-wrap:anywhere}
@media (max-width:380px){.logo h1{-webkit-text-stroke:3px #1b0b35}}
.cr a{color:#7cf0ff;font-weight:700;text-decoration:none;border-bottom:1px solid currentColor}
#credits .copy{font-size:11px;opacity:.7;margin-top:10px;letter-spacing:1px}
#credits button{margin-top:14px}
#nogl{z-index:99;background:#1b0b35;padding:28px;box-sizing:border-box;gap:14px;font-size:16px;line-height:1.5}
#nogl b{font-family:'Luckiest Guy';font-weight:400;font-size:30px;color:#ffd166}
</style>
</head>''')

# ---------- 3. title screen: sound button, links, phone hint ----------
sub('<div id="start" class="screen"', '<div id="nogl" class="screen hidden"><b>SPACE HAMSTER RUN</b><div>This game needs 3D graphics (WebGL), which this browser or device doesn\'t support.<br>Try an up-to-date Chrome, Safari or Firefox.</div></div>\n<div id="start" class="screen"')
sub('<div class="hint">◀ ▶ BUTTONS, ARROW KEYS OR DRAG TO STEER<br>JUMP BUTTON, SPACE OR ↑ TO JUMP</div>',
    '<div class="hint" id="hint">◀ ▶ BUTTONS, ARROW KEYS OR DRAG TO STEER<br>JUMP BUTTON, SPACE OR ↑ TO JUMP</div>\n'
    f'    <div class="links"><a id="fbLink" href="{FEEDBACK_HREF}" target="_blank" rel="noopener">FEEDBACK</a><button id="shareTitle" type="button">SHARE</button><button id="creditsBtn" type="button">CREDITS</button></div>\n'
    '    <button id="sndBtn" type="button" aria-label="Sound on or off">🔊</button>')

# ---------- 4. credits card ----------
sub('<div id="over" class="screen hidden">', f'''<div id="credits" class="screen hidden">
  <div class="card">
    <div class="ttl">SPACE<span>HAMSTER RUN</span></div>
    <div class="cr">
      <b>GAME + ART</b><span>Guy</span>
      <b>MADE BY</b><span><a href="https://oatmealmorning.com/" target="_blank" rel="noopener">Oatmeal Morning</a>, a husband-and-wife studio</span>
      <b>FONTS</b><span>Luckiest Guy (Apache License 2.0), Rubik (SIL Open Font License)</span>
      <b>3D</b><span>three.js (MIT License)</span>
      <b>PRIVACY</b><span><a href="{SITE}/privacy/" target="_blank" rel="noopener">Privacy policy</a></span>
      <b>HELP</b><span><a href="{SITE}/support/" target="_blank" rel="noopener">Help &amp; support</a></span>
    </div>
    <div class="copy">© 2026 OATMEAL MORNING · VERSION {VERSION}</div>
    <button id="creditsBack" type="button">BACK</button>
  </div>
</div>
<div id="over" class="screen hidden">''')

# ---------- 5. share on win / game over, sound on pause ----------
sub('<button class="alt" id="menu1">WORLDS</button>', '<button class="alt" id="shareOver" type="button">SHARE</button>\n  <button class="alt" id="menu1">WORLDS</button>')
sub('<button class="alt" id="menu2">WORLDS</button>', '<button class="alt" id="shareWin" type="button">SHARE</button>\n  <button class="alt" id="menu2">WORLDS</button>')
sub('<button class="alt" id="menu3">MAIN MENU</button>', '<button class="alt" id="menu3">MAIN MENU</button>\n  <button class="alt" id="sndPause" type="button">SOUND: ON</button>')

# ---------- 6. no WebGL: show a message instead of a black screen ----------
sub('const renderer=new THREE.WebGLRenderer({antialias:true});', '''(function(){let ok=false;try{const c=document.createElement('canvas');ok=!!(window.WebGLRenderingContext&&(c.getContext('webgl2')||c.getContext('webgl')));}catch(e){}
 if(!ok){document.getElementById('start').classList.add('hidden');document.getElementById('nogl').classList.remove('hidden');track('webgl_unsupported',{});throw new Error('WebGL not available');}})();
const renderer=new THREE.WebGLRenderer({antialias:true});''')

# ---------- 7. sound on/off (setting kept in the game's own save) ----------
sub("function tone(f,d,type='sine',vol=.1,slide=0,delay=0){if(!ac)return;", "function tone(f,d,type='sine',vol=.1,slide=0,delay=0){if(!ac||save.muted)return;")
sub("function noiseBurst(d,vol=.08){if(!ac)return;", "function noiseBurst(d,vol=.08){if(!ac||save.muted)return;")

# ---------- 8. analytics events ----------
sub("reset();updHearts();state='play';showOnly(null);",
    "reset();updHearts();state='play';showOnly(null);\n runT0=performance.now();pausedMs=0;quitSent=false;\n track('game_start',{level:levelIdx+1,world:L.id,muted:!!save.muted,touch:'ontouchstart' in window});")
sub("function pauseGame(){if(state!=='play')return;state='paused';", "function pauseGame(){if(state!=='play')return;state='paused';pauseT0=performance.now();")
sub("function resumeGame(){if(state!=='paused')return;", "function resumeGame(){if(state!=='paused')return;pausedMs+=performance.now()-pauseT0;")
sub("tone(420,.7,'sawtooth',.09,.15);score=Math.floor(dist)+nutCount*50+pops*30;",
    "tone(420,.7,'sawtooth',.09,.15);score=Math.floor(dist)+nutCount*50+pops*30;\n track('game_over',{level:levelIdx+1,world:L.id,score,nuts:nutCount,distance_m:Math.floor(dist),goal_m:L.goal,progress_pct:Math.min(100,Math.round(100*dist/L.goal)),seconds:runSecs()});")
sub("state='win';score=Math.floor(dist)+nutCount*50+pops*30+lives*250;",
    "state='win';score=Math.floor(dist)+nutCount*50+pops*30+lives*250;\n track('level_win',{level:levelIdx+1,world:L.id,score,nuts:nutCount,hearts_left:lives,seconds:runSecs(),first_time:!save.done.includes(levelIdx)});")
sub("$('resumeBtn').onclick=resumeGame;$('restartBtn').onclick=start;$('menu3').onclick=goMenu;",
    "$('resumeBtn').onclick=resumeGame;$('restartBtn').onclick=()=>{trackQuit('restart');start();};$('menu3').onclick=()=>{trackQuit('quit_button');goMenu();};")
sub("document.addEventListener('visibilitychange',()=>{if(document.hidden)pauseGame();});",
    "document.addEventListener('visibilitychange',()=>{if(document.hidden){trackQuit('app_hidden');pauseGame();}});")
sub("function startWarp(i){if(state!=='menu'||i===levelIdx)return;", "function startWarp(i){if(state!=='menu'||i===levelIdx)return;track('world_select',{level:i+1,world:LEVELS[i].id});")
sub("if(!unlocked(i)){el.classList.remove('shake');", "if(!unlocked(i)){track('locked_level_tap',{level:i+1,world:LEVELS[i].id});el.classList.remove('shake');")

# ---------- 9. warp fix: ignore RUN! / world taps during the warp animation ----------
sub("$('go').onclick=start;", "$('go').onclick=()=>{if(state==='warp')return;start();};")
sub("el.onclick=()=>{const i=+el.dataset.i;", "el.onclick=()=>{if(state==='warp')return;const i=+el.dataset.i;")

# ---------- 10. Android back button: close credits, ignore during warp ----------
sub("window.handleBack=function(){", "window.handleBack=function(){if(!$('credits').classList.contains('hidden')){closeCredits();return 'ok';}if(state==='warp')return 'ok';")

# ---------- 11. wiring: helpers, sound, credits, share, feedback, phone hint ----------
sub("renderLevels();reset();\nrequestAnimationFrame(frame);", r"""// ---- web build additions ----
let runT0=0,pausedMs=0,pauseT0=0,quitSent=false;
function runSecs(){const now=performance.now();return Math.round((now-runT0-pausedMs-(state==='paused'?now-pauseT0:0))/1000);}
function trackQuit(reason){   // a run left before winning or losing: quit button, restart, or app put away mid-run
 if((state!=='play'&&state!=='paused')||quitSent)return;quitSent=true;
 track('game_quit',{level:levelIdx+1,world:L.id,reason,seconds:runSecs(),distance_m:Math.floor(dist),goal_m:L.goal,progress_pct:Math.min(100,Math.round(100*dist/L.goal)),score:Math.floor(dist)+nutCount*50+pops*30,nuts:nutCount},{send_instantly:true,transport:'sendBeacon'});}
function paintSound(){$('sndBtn').textContent=save.muted?'🔇':'🔊';$('sndPause').textContent=save.muted?'SOUND: OFF':'SOUND: ON';}
function toggleSound(){save.muted=!save.muted;persist();paintSound();track('sound_toggle',{muted:save.muted});
 if(!save.muted){if(!ac){try{ac=new (window.AudioContext||window.webkitAudioContext)();}catch(e){}}if(ac&&ac.state==='suspended')ac.resume();tone(660,.08,'square',.04,1.5);}}
$('sndBtn').onclick=e=>{e.stopPropagation();toggleSound();};$('sndPause').onclick=toggleSound;
function openCredits(){if(state!=='menu')return;$('start').classList.add('hidden');$('credits').classList.remove('hidden');track('credits_open',{});}
function closeCredits(){$('credits').classList.add('hidden');$('start').classList.remove('hidden');}
$('creditsBtn').onclick=openCredits;$('creditsBack').onclick=closeCredits;
$('fbLink').addEventListener('click',()=>track('feedback_click',{}));
async function share(where){
 const app=SHR_BUILD.platform!=='web',url=app?SHARE_URL.app:SHARE_URL.web,pts=(score||0).toLocaleString('en-US'),w=L.name.charAt(0)+L.name.slice(1).toLowerCase();
 const text=where==='win'?(levelIdx===LEVELS.length-1?`I beat all 5 worlds of Space Hamster Run with ${pts} points! Can you?`:`I made it through the ${w} world in Space Hamster Run with ${pts} points. Beat me:`)
  :where==='over'?`I got ${pts} points in the ${w} world of Space Hamster Run. Beat me:`:'Space Hamster Run: run, jump and grab the nuts through 5 worlds. '+(app?'Free on your phone:':'Free in your browser:');
 const btn=$(where==='win'?'shareWin':where==='over'?'shareOver':'shareTitle');
 track('share_click',{where,level:levelIdx+1,world:L.id,score:where==='title'?0:score});
 try{if(navigator.share){await navigator.share({title:'Space Hamster Run',text,url});return;}
  await navigator.clipboard.writeText(text+' '+url);const old=btn.textContent;btn.textContent='LINK COPIED';setTimeout(()=>{btn.textContent=old;},1600);}catch(e){}}
$('shareWin').onclick=()=>share('win');$('shareOver').onclick=()=>share('over');$('shareTitle').onclick=()=>share('title');
if(matchMedia('(pointer:coarse)').matches&&!matchMedia('(any-pointer:fine)').matches)$('hint').innerHTML='◀ ▶ BUTTONS OR DRAG TO STEER<br>TAP JUMP TO JUMP';
paintSound();
renderLevels();reset();
requestAnimationFrame(frame);""")

(out_dir / 'index.html').write_text(s, encoding='utf-8')
print('ok:', out_dir / 'index.html', round(len(s.encode()) / 1e6, 2), 'MB')
