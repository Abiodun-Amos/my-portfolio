#!/usr/bin/env python3
"""Builds the portfolio pages into dist/. Edit the content below, then run: python3 build.py"""
import math, random, html, pathlib, json, datetime

OUT = pathlib.Path(__file__).parent / "dist"
# The public address of the site, with no slash at the end. When you move to your own domain,
# change this one line to "https://amosabiodun.com" and run: python3 build.py
SITE_URL = "https://amosabiodun.netlify.app"
EMAIL = "abiodunamos59@gmail.com"
PHONE_SHOW = "+234 (0) 808 613 0089"
PHONE_TEL = "+2348086130089"
WA = "https://wa.me/2348086130089"
LINKEDIN = "https://linkedin.com/in/abiodun-amos"
GITHUB = "https://github.com/Abiodun-Amos"

def ico(d):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'
ARROW = ico("M5 12h14M13 6l6 6-6 6")
UPRIGHT = ico("M7 17 17 7M8 7h9v9")
DL = ico("M12 4v11M7 10l5 5 5-5M5 20h14")
CV = "Amos_Abiodun_CV.pdf"  # the CV file in dist/. Replace that file to update the download.
PLUS = ico("M12 5v14M5 12h14")
MENU = ico("M4 8h16M4 16h16")
CLOSE = ico("M6 6l12 12M18 6 6 18")
UP = ico("M12 19V5M6 11l6-6 6 6")
LEFT = ico("M19 12H5M11 6l-6 6 6 6")
SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
LOGO = '<img class="logo--dark" src="img/logo-dark.png" alt="" width="30" height="30"><img class="logo--light" src="img/logo-light.png" alt="" width="30" height="30">'
CV_BTN = f'<a class="cv-btn" href="{CV}" download aria-label="Download my CV (PDF)"><span>CV</span>{DL}</a>'
THEME_BTN = f'<button class="theme-btn" type="button" aria-label="Switch between dark and light mode">{SUN}{MOON}</button>'

NAV = [("projects.html", "Projects"), ("expertise.html", "Expertise"), ("about.html", "About"),
       ("speaking.html", "Speaking"), ("gallery.html", "Gallery"), ("contact.html", "Contact")]

def lines(parts):
    return "".join(f'<span><i style="--i:{i}">{p}</i></span>' for i, p in enumerate(parts))

def eyebrow(n, label):
    return f'<p class="eyebrow reveal"><b>{n}</b>{label}</p>'

def tags(items):
    return '<ul class="tags">' + "".join(f"<li>{t}</li>" for t in items) + "</ul>"

# ---------- project artwork (drawn, not screenshots; swap for real screenshots later) ----------
def art(kind):
    rnd = random.Random({"fruit": 7, "network": 21, "face": 3}[kind])
    W, H = 800, 500
    s = [f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Abstract illustration for this project">',
         f'<rect width="{W}" height="{H}" fill="#171717"/>']
    for x in range(0, W + 1, 50):
        s.append(f'<path d="M{x} 0V{H}" stroke="#222" stroke-width="1"/>')
    for y in range(0, H + 1, 50):
        s.append(f'<path d="M0 {y}H{W}" stroke="#222" stroke-width="1"/>')
    if kind == "fruit":
        for k, col in enumerate(["#F5F3EE", "#8a8a8a", "#22C7E8"]):
            pts, y = [], 150 + k * 70
            for x in range(40, W - 30, 20):
                y += rnd.uniform(-16, 16) + (0.9 if k == 2 and x > 430 else 0) * 6
                y = max(70, min(H - 70, y))
                pts.append(f"{x},{y:.0f}")
            s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{3 if k==2 else 2}" stroke-linejoin="round"/>')
        s.append(f'<path d="M40 380H{W-40}" stroke="#22C7E8" stroke-width="1.5" stroke-dasharray="6 8"/>')
        s.append('<text x="44" y="60" fill="#A3A3A3" font-family="monospace" font-size="15" letter-spacing="3">SENSOR READINGS / FRESHNESS</text>')
        s.append(f'<text x="{W-44}" y="372" text-anchor="end" fill="#22C7E8" font-family="monospace" font-size="13" letter-spacing="2">SPOILAGE THRESHOLD</text>')
    elif kind == "network":
        nodes = [(rnd.uniform(70, W - 70), rnd.uniform(90, H - 60)) for _ in range(26)]
        hot = set(rnd.sample(range(26), 5))
        for i, a in enumerate(nodes):
            near = sorted(range(26), key=lambda j: math.dist(a, nodes[j]))[1:4]
            for j in near:
                c = "#22C7E8" if i in hot and j in hot else "#3a3a3a"
                s.append(f'<path d="M{a[0]:.0f} {a[1]:.0f}L{nodes[j][0]:.0f} {nodes[j][1]:.0f}" stroke="{c}" stroke-width="{2.5 if c!="#3a3a3a" else 1.2}"/>')
        for i, (x, y) in enumerate(nodes):
            if i in hot:
                s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="none" stroke="#22C7E8" stroke-width="1"/>')
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{7 if i in hot else 5}" fill="{"#22C7E8" if i in hot else "#F5F3EE"}"/>')
        s.append('<text x="44" y="60" fill="#A3A3A3" font-family="monospace" font-size="15" letter-spacing="3">NETWORK TRAFFIC / PREDICTED CONGESTION</text>')
    else:
        cx, cy = W / 2, H / 2 + 10
        for r in range(0, 9):
            for c in range(0, 9):
                x, y = cx - 120 + c * 30, cy - 150 + r * 37
                if ((x - cx) / 130) ** 2 + ((y - cy) / 170) ** 2 <= 1:
                    s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.2" fill="#F5F3EE"/>')
        for (x, y, dx, dy) in [(cx - 170, cy - 200, 1, 1), (cx + 170, cy - 200, -1, 1), (cx - 170, cy + 200, 1, -1), (cx + 170, cy + 200, -1, -1)]:
            s.append(f'<path d="M{x:.0f} {y + dy*46:.0f}V{y:.0f}H{x + dx*46:.0f}" fill="none" stroke="#22C7E8" stroke-width="4"/>')
        s.append(f'<path d="M{cx-200:.0f} {cy-30:.0f}H{cx+200:.0f}" stroke="#22C7E8" stroke-width="1.5" stroke-dasharray="4 7"/>')
        s.append('<text x="44" y="60" fill="#A3A3A3" font-family="monospace" font-size="15" letter-spacing="3">FACE DETECTION / ATTENDANCE</text>')
    s.append("</svg>")
    return "".join(s)

PROJECTS = [
    dict(slug="project-fruit", n="01", kind="fruit", img="proj-fruit.jpg", alt="Fruit Monitor live dashboard with inventory, temperature, humidity and gas charts",
         shots=[("shot-fruit-inventory.jpg","Dashboard","Inventory view listing each fruit with its status, days left and recent alerts"),
                ("shot-fruit-charts.jpg","Sensor data","Temperature, humidity and MQ-135 gas readings plotted over time"),
                ("shot-fruit-circuit.jpg","Circuit","ESP32 wired to a DHT22 sensor, a gas sensor and an ESP32-CAM"),
                ("shot-fruit-fritzing.jpg","Circuit","The circuit drawn in Fritzing: ESP32, gas sensor, DHT sensor, ESP32-CAM and two 18650 batteries"),
                ("shot-fruit-camera.jpg","Camera","View from the ESP32-CAM over the fruit tray")], cat="iot ai", year="2026",
         title="Smart Fruit Spoilage and Freshness Detection",
         catlabel="IoT and Machine Learning", role="Client project: design, hardware and model",
         short="An IoT system that reads environmental sensors around stored fruit and uses a machine learning model to predict freshness and shelf life in real time.",
         tools=["ESP32", "DHT22 sensor", "MQ-135 gas sensor", "ESP32-CAM", "Machine learning", "Python", "Live web dashboard"],
         live="https://fruit-monitor.onrender.com/dashboard/", livelabel="Open the live dashboard", liveshort="Live dashboard",
         problem=["Fruit loses value quickly once it starts to spoil, and by the time spoilage is visible the loss has already happened. Traders and stores need an early signal, not a late one."],
         built=["For a client, I developed an integrated IoT system that uses environmental sensors to monitor the conditions that indicate food and agricultural produce is degrading.",
                "On top of the sensor data I built and deployed a machine learning model that analyses readings in real time and predicts food freshness and shelf life. The readings and predictions are shown on a live web dashboard."],
         points=["Temperature, humidity and gas sensors feeding live data", "A camera view of the fruit in storage", "A deployed model that predicts freshness and shelf life", "An inventory with a status and alert for each fruit", "Telegram and email alerts when fruit starts to spoil", "A dashboard anyone can open in a browser"],
         note="The dashboard is hosted on a free plan, so the first visit can take up to a minute to load."),
    dict(slug="project-network", n="02", kind="network", img="proj-network.jpg", alt="Command Center view with a map of Lagos showing congestion risk and an action log",
         shots=[("shot-network-tree.jpg","Model","Decision tree from the notebook, with a recommended action at each leaf")], cat="ai data", year="2026",
         title="Nigerian Network Congestion Prediction System",
         catlabel="Machine Learning and Data Science", role="Data analysis and modelling",
         short="A predictive model that learns from telecommunications network data to forecast traffic congestion before it happens.",
         tools=["Python", "pandas", "scikit-learn", "Decision Tree models", "seaborn", "Streamlit"],
         live="https://network-congestion-prediction.onrender.com/", livelabel="Open the live app", liveshort="Live app",
         problem=["Network congestion slows calls and data for everyone on a cell. Operators who can see congestion coming can act earlier, by rerouting traffic or adding capacity."],
         built=["I developed a predictive model, optimised for telecommunications network data, that forecasts network traffic congestion so it can be mitigated.",
                "I implemented and evaluated machine learning architectures, including Decision Tree models, using Python data science and visualisation libraries. The model runs as a web app that takes network conditions and returns a prediction."],
         points=["A model trained on telecom network data", "Decision Tree models built and evaluated in scikit-learn", "A map view showing congestion risk by location", "An action log that can be downloaded as CSV", "A web app for trying predictions"],
         note="The app is hosted on a free plan, so the first visit can take up to a minute to load."),
    dict(slug="project-attendance", n="03", kind="face", img="proj-attendance.jpg", alt="FRAS live overview dashboard showing attendance figures and today's sessions",
         shots=[("shot-attendance-wiring.jpg","Wiring","Webcam, Orange Pi, cooling fan and a battery backup (UPS) module"),
                ("build-camera.jpg","Hardware","Camera on the workbench during the build"),
                ("build-sbc.jpg","Hardware","Single-board computer with a battery pack in its enclosure")], cat="ai", year="2026",
         title="AI Facial Recognition Attendance System",
         catlabel="Artificial Intelligence and Computer Vision", role="Final-year project",
         short="An automated attendance system that recognises faces with computer vision, replacing manual registers with a faster and more secure record.",
         tools=["Computer vision", "Facial detection", "Facial recognition", "Orange Pi", "Web admin dashboard", "Firebase"],
         live="https://ai-facial-recognition-system.firebaseapp.com/", livelabel="Open the admin dashboard (login required)", liveshort="Admin dashboard (login)",
         problem=["Paper registers and manual roll calls are slow, easy to falsify and hard to audit. Institutions need attendance records they can trust without adding work for staff."],
         built=["For my final-year project in Electrical/Electronic Engineering I designed and implemented an automated attendance management system built on artificial intelligence and computer vision.",
                "I developed the facial detection and recognition algorithms that identify each person and record their attendance, giving a seamless, secure and efficient alternative to manual tracking. Administrators review sessions and records through a web dashboard."],
         points=["Facial detection and recognition for check-in", "Automatic attendance records per session", "A live overview with intruder alerts and attendance rate", "CSV export of records", "An admin dashboard for review"],
         note="The dashboard is protected by a login because it holds attendance records. Contact me for a walkthrough."),
]

def head(title, desc, active):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{l}</a>' for h, l in NAV)
    drawer = "".join(f'<a href="{h}">{l}<span>0{i+1}</span></a>' for i, (h, l) in enumerate(NAV))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="Amos Olaoluwa Abiodun">
<meta name="robots" content="index, follow">
<meta property="og:site_name" content="Amos Abiodun">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_NG">
<meta property="og:image" content="{SITE_URL}/img/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Amos Abiodun, Electrical/Electronics engineer">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE_URL}/img/share.jpg">
<!--SEO-->
<meta name="theme-color" content="#101010">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="img/touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
<script>(function(){{var d=document.documentElement,t='dark';d.classList.add('js');try{{t=localStorage.getItem('aa-theme')||'dark'}}catch(e){{}}d.setAttribute('data-theme',t)}})()</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="curtain" aria-hidden="true"></div>
<div class="progress" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"></div>
<header class="header">
  <a class="brand" href="index.html" aria-label="Amos Abiodun, home">{LOGO}Amos Abiodun</a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <div class="head-tools">{CV_BTN}{THEME_BTN}<button class="menu-btn" data-menu="open" aria-label="Open menu" aria-expanded="false">{MENU}</button></div>
</header>
<div class="drawer" aria-label="Menu">
  <div class="drawer__top">
    <a class="brand" href="index.html">{LOGO}Amos Abiodun</a>
    <div class="head-tools">{THEME_BTN}<button class="menu-btn" data-menu="close" aria-label="Close menu" style="display:grid">{CLOSE}</button></div>
  </div>
  <nav aria-label="Mobile">{drawer}</nav>
  <div class="drawer__foot"><a href="{CV}" download>Download CV</a><a href="{WA}">WhatsApp</a><a href="{LINKEDIN}">LinkedIn</a><a href="{GITHUB}">GitHub</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
</div>
<main id="main">
'''

def cta_section():
    return f'''<section class="section cta wrap">
  {eyebrow("→", "Contact")}
  <h2 class="reveal">Have an idea?<br><span class="hl">Let's build</span> something meaningful.</h2>
  <p class="lead mute reveal" style="margin-top:28px">Whether you're exploring an engineering project, seeking a STEM instructor, planning a technology initiative, or looking for a speaker, I'd love to hear from you.</p>
  <a class="cta__mail reveal" href="mailto:{EMAIL}">{EMAIL}</a>
  <div class="cta__row reveal">
    <a class="btn" href="contact.html"><span class="ico">{ARROW}</span>Start a conversation</a>
    <a class="btn btn--ghost" href="{WA}">Chat on WhatsApp</a>
    <a class="btn btn--ghost" href="speaking.html">Invite me to speak</a>
    <a class="btn btn--ghost" href="{CV}" download>Download my CV</a>
  </div>
</section>'''

def foot():
    nav = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV[:3])
    nav2 = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV[3:])
    return f'''</main>
<footer class="footer">
  <div class="footer__top">
    <div class="footer__id">
      <img class="footer__logo logo--dark" src="img/logo-dark.png" alt="Amos Abiodun logo" width="120" height="120"><img class="footer__logo logo--light" src="img/logo-light.png" alt="Amos Abiodun logo" width="120" height="120">
      <p>Amos Olaoluwa Abiodun. Electrical/Electronics engineer working across embedded systems, IoT, machine learning and data science. Based in Ibadan, Nigeria.</p>
    </div>
    <div class="footer__col"><h4>Site</h4><a href="index.html">Home</a>{nav}</div>
    <div class="footer__col"><h4>More</h4>{nav2}</div>
    <div class="footer__col"><h4>Connect</h4><a href="{CV}" download>Download CV</a><a href="{LINKEDIN}">LinkedIn</a><a href="{GITHUB}">GitHub</a><a href="{WA}">WhatsApp</a><a href="mailto:{EMAIL}">Email</a></div>
  </div>
  <div class="footer__bot">
    <span>© 2026 Amos Olaoluwa Abiodun. All rights reserved.</span>
    <a class="totop" href="#main">Back to top <i>{UP}</i></a>
  </div>
</footer>
<script src="js/site.js"></script>
</body>
</html>
'''

def lightbox():
    return f'''<div class="lb" role="dialog" aria-modal="true" aria-label="Image viewer">
  <div class="lb__bar"><span class="lb__count">1 / 1</span><button data-lb="close" aria-label="Close viewer">{CLOSE}</button></div>
  <div class="lb__stage"><img src="" alt=""></div>
  <div class="lb__foot"><p></p><div class="lb__nav"><button data-lb="prev" aria-label="Previous image">{LEFT}</button><button data-lb="next" aria-label="Next image">{ARROW}</button></div></div>
</div>'''

def phead(word, eyebrow_txt, title_lines, lead):
    return f'''<section class="phead" data-word="{word}">
  <p class="eyebrow fade"><b>{eyebrow_txt[0]}</b>{eyebrow_txt[1]}</p>
  <h1 class="h-xl">{lines(title_lines)}</h1>
  <p class="lead fade">{lead}</p>
</section>'''

EXPERTISE = [
    dict(id="electronics", n="01", title="Electrical &amp; Electronics Engineering",
         desc="Working with electronic systems, circuit design, electrical principles, and hardware innovation.",
         more="I hold a B.Sc. in Electrical/Electronic Engineering from Olabisi Onabanjo University and trained on aviation communication and navigation systems at the Nigerian Airspace Management Agency.",
         skills=["Circuit design", "Power and energy metering", "Solar power installation sizing", "VSAT systems", "VHF radio, ILS and VOR equipment", "Fault finding"],
         rel=[("about.html", "Industrial training at NAMA"), ("gallery.html", "Field and bench work in the gallery")]),
    dict(id="embedded", n="02", title="Embedded Systems, IoT &amp; Robotics",
         desc="Designing microcontroller devices, connected sensor systems, robotic builds, and automation.",
         more="I design devices around microcontrollers and single-board computers: sensing, control, connectivity and the enclosure they live in. The fruit spoilage monitor and the attendance system both run on hardware I built.",
         skills=["Arduino", "ESP32", "Single-board computers", "Sensors and actuators", "RFID and GSM modules", "C/C++ for microcontrollers"],
         rel=[("project-fruit.html", "Smart Fruit Spoilage Detection"), ("gallery.html", "Hardware builds in the gallery")]),
    dict(id="ai", n="03", title="Artificial Intelligence &amp; Machine Learning",
         desc="Exploring intelligent systems, predictive models, machine learning applications, and data-driven solutions.",
         more="My AI work is applied: a model has to run on real data and do a real job, whether that is recognising a face or predicting spoilage.",
         skills=["Computer vision", "Facial recognition", "Decision Tree models", "scikit-learn", "Predictive modelling", "Python"],
         rel=[("project-attendance.html", "AI Facial Recognition Attendance System"), ("project-network.html", "Network Congestion Prediction System"), ("project-fruit.html", "Smart Fruit Spoilage Detection")]),
    dict(id="data", n="04", title="Data Science &amp; Analytics",
         desc="Transforming complex datasets into meaningful insights through analysis, modelling, and visualization.",
         more="I took first place in a data science and machine learning competition organised by Data Science Nigeria, TRAIL and exploreCSR, and ranked first on a Zindi leaderboard.",
         skills=["pandas", "seaborn", "Data visualisation", "Excel", "Power BI", "Research methodology"],
         rel=[("project-network.html", "Network Congestion Prediction System"), ("about.html#credentials", "Competition results and certificates")]),
    dict(id="speaking", n="05", title="Public Speaking &amp; Knowledge Sharing",
         desc="Delivering engaging presentations, facilitating technical discussions, and communicating complex ideas to diverse audiences.",
         more="I have moderated more than five events, including panel discussions at a technical symposium, and pitched an engineering project at the Nigeria Energy Forum.",
         skills=["Panel moderation", "Technical talks", "Project pitching", "Workshop facilitation", "STEM outreach"],
         rel=[("speaking.html", "Speaking and moderation"), ("contact.html", "Invite me to speak")]),
    dict(id="instruction", n="06", title="STEM Instruction &amp; Technical Training",
         desc="Training students and beginners in robotics, electronics, and programming through hands-on projects.",
         more="As a STEM Instructor I have trained more than 300 students across three schools, using project guides I write myself so that beginners finish with something that works.",
         skills=["Curriculum design", "Project-based training", "Project guides", "Arduino and LEGO WeDo 2.0", "Mentorship"],
         rel=[("about.html", "STEM Instructor roles"), ("gallery.html", "Robotics kit builds in the gallery")]),
]

def xp_rows(expand=True):
    out = ['<div class="xp">']
    for i, e in enumerate(EXPERTISE):
        if expand:
            rel = "".join(f'<li><a href="{h}">{l} →</a></li>' for h, l in e["rel"])
            out.append(f'''<div class="xp__row reveal" id="{e["id"]}" style="--d:{i%3}">
  <button class="xp__head" aria-expanded="false" aria-controls="xp-{e["id"]}">
    <span class="xp__num">{e["n"]}</span><span class="xp__title">{e["title"]}</span><span class="xp__desc">{e["desc"]}</span><span class="xp__plus">{PLUS}</span>
  </button>
  <div class="xp__body" id="xp-{e["id"]}"><div class="xp__inner"><div class="xp__cols">
    <div><h4>In practice</h4><p>{e["more"]}</p><h4 style="margin-top:22px">Skills and tools</h4>{tags(e["skills"])}</div>
    <div><h4>Related work</h4><ul class="rel">{rel}</ul></div>
  </div></div></div>
</div>''')
        else:
            out.append(f'''<div class="xp__row reveal" style="--d:{i%3}">
  <a class="xp__head" href="expertise.html#{e["id"]}">
    <span class="xp__num">{e["n"]}</span><span class="xp__title">{e["title"]}</span><span class="xp__desc">{e["desc"]}</span><span class="xp__plus">{UPRIGHT}</span>
  </a>
</div>''')
    out.append("</div>")
    return "".join(out)

def work_items(items):
    out = ['<div class="work">']
    for p in items:
        out.append(f'''<article class="work__item reveal" data-cat="{p["cat"]}">
  <a class="work__media" href="{p["slug"]}.html" aria-label="{p["title"]}"><img src="img/{p["img"]}" alt="{p["alt"]}" loading="lazy"></a>
  <div class="work__info">
    <span class="work__n">{p["n"]} / {p["year"]}</span>
    <p class="work__cat">{p["catlabel"]}</p>
    <h3><a href="{p["slug"]}.html">{p["title"]}</a></h3>
    <p>{p["short"]}</p>
    {tags(p["tools"][:4])}
    <div class="work__links"><a class="link" href="{p["slug"]}.html">View project {UPRIGHT}</a><a class="link" href="{p["live"]}" target="_blank" rel="noopener">{p["liveshort"]} {UPRIGHT}</a></div>
  </div>
</article>''')
    out.append("</div>")
    return "".join(out)

STATS = '''<div class="stats">
  <div class="stat reveal" style="--d:0"><b><span data-count="300">300</span><em>+</em></b><span>Students trained</span></div>
  <div class="stat reveal" style="--d:1"><b><span data-count="3">3</span></b><span>Schools worked with</span></div>
  <div class="stat reveal" style="--d:2"><b><span data-count="20">20</span><em>+</em></b><span>Projects built</span></div>
  <div class="stat reveal" style="--d:3"><b><span data-count="5">5</span><em>+</em></b><span>Events moderated</span></div>
</div>'''

MARQUEE_WORDS = ["Electronics Engineering", "Embedded Systems", "Internet of Things", "Machine Learning", "Data Science", "Robotics", "Public Speaking"]
def marquee():
    row = "".join(f"<span>{w}</span>" for w in MARQUEE_WORDS)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee__track">{row}{row}{row}{row}</div></div>'

# ---------------- pages ----------------
def page_home():
    name = "".join(f'<span style="--i:{i}">{c}</span>' for i, c in enumerate("Amos"))
    return head("Amos Abiodun: Electrical/Electronics Engineer, Embedded Systems, IoT and Machine Learning", "Amos Abiodun is an Electrical/Electronics engineer in Ibadan, Nigeria, working across embedded systems, IoT, machine learning and data science.", "index.html") + f'''
<section class="hero">
  <div class="hero__left">
    <span class="pill fade" style="--i:0">Available for work</span>
    <h1 class="hero__roles" aria-label="Engineer. Educator. Innovator. Technologist.">{lines(["Engineer.", "Educator.", "Innovator.", '<span class="hl" style="display:inline">Technologist.</span>'])}</h1>
  </div>
  <div class="hero__stage">
    <img class="hero__portrait" src="img/amos-portrait.png" alt="Portrait of Amos Abiodun in a suit and blue tie" width="906" height="1090">
    <p class="hero__name" aria-hidden="true">{name}</p>
  </div>
  <div class="hero__right">
    <p class="hero__intro fade" style="--i:1">Hi, I'm Amos Abiodun. I work at the intersection of engineering, technology, education, and innovation, transforming complex ideas into practical solutions and empowering the next generation of problem solvers.</p>
    <div class="hero__cta fade" style="--i:2">
      <a class="btn" href="projects.html"><span class="ico">{ARROW}</span>Explore my work</a>
      <a class="link" href="contact.html">Let's connect {UPRIGHT}</a>
      <a class="link" href="{CV}" download>Download CV {DL}</a>
    </div>
  </div>
</section>
{marquee()}

<section class="section wrap">
  {eyebrow("01", "Introduction")}
  <div class="statement">
    <h2 class="h-xl reveal">Building technology. Solving problems. <span class="hl">Empowering minds.</span></h2>
    <p class="statement__a reveal">I am a multidisciplinary technology professional passionate about developing <span class="hl">intelligent systems</span>, exploring emerging technologies, and making <span class="hl">technical knowledge accessible</span>. My work spans engineering, robotics, artificial intelligence, data science, and STEM education.</p>
    <p class="statement__b reveal" style="--d:1">I solve problems by getting close to them: I research what already exists, build a small version quickly, test it with real data and real users, and improve it with the people who will rely on it. The result has to work outside the lab.</p>
  </div>
</section>

<section class="section section--alt"><div class="wrap">
  {eyebrow("02", "Areas of expertise")}
  <h2 class="h-lg reveal" style="margin-bottom:clamp(32px,5vw,64px)">Six disciplines, one way of working.</h2>
  {xp_rows(expand=False)}
</div></section>

<section class="section wrap">
  {eyebrow("03", "Selected projects")}
  <div class="next" style="margin-bottom:clamp(40px,6vw,80px)">
    <h2 class="h-lg reveal">Work that runs on real data.</h2>
    <a class="link reveal" href="projects.html">All projects {UPRIGHT}</a>
  </div>
  {work_items(PROJECTS)}
</section>

<section class="section section--alt"><div class="wrap">
  {eyebrow("04", "In numbers")}
  {STATS}
</div></section>

<section class="section wrap">
  <div class="split">
    <div class="split__text">
      {eyebrow("05", "Engineering in the field")}
      <h2 class="h-lg reveal">From the workbench to live systems.</h2>
      <p class="body reveal">My engineering does not stop at a prototype. At the Nigerian Airspace Management Agency I took part in installing and maintaining VSAT systems and worked on VHF radios, Instrument Landing Systems, VOR and voice communication equipment.</p>
      <p class="body reveal">The same discipline goes into my own builds: embedded devices with their own power, sensing, connectivity and enclosures, tested until they run unattended.</p>
      <a class="link reveal" href="about.html">My professional journey {UPRIGHT}</a>
    </div>
    <div class="split__media duo">
      <div class="frame clip"><img src="img/field-vsat.jpg" alt="Amos Abiodun working on the electronics box of a satellite dish" loading="lazy" data-speed="-0.04"></div>
      <div class="frame clip"><img src="img/field-vcs.jpg" alt="Amos Abiodun beside a voice communication system equipment rack" loading="lazy" data-speed="0.04"></div>
    </div>
  </div>
</section>

<section class="section section--alt band"><div class="wrap">
  {eyebrow("06", "Speaking")}
  <h2 class="h-xl reveal">Ideas are powerful. <span class="hl">Sharing them</span> creates impact.</h2>
  <div class="band__row">
    <p class="lead mute reveal">I moderate panels, speak at technology and skill-acquisition events, and pitch engineering projects.</p>
    <a class="btn reveal" href="speaking.html"><span class="ico">{ARROW}</span>Invite me to speak</a>
  </div>
</div></section>

{cta_section()}
''' + foot()

def page_projects():
    more = [("build-rfid.jpg", "ESP32 build with an RFID reader, keypad and display"), ("build-drone.jpg", "Drone and controller on the workbench"),
            ("build-sbc.jpg", "Single-board computer with a battery pack in an enclosure"), ("build-meter.jpg", "Energy meter prototype with a GSM link")]
    grid = "".join(f'<a class="gal__item reveal" href="gallery.html" style="--d:{i}"><img src="img/{f}" alt="{c}" loading="lazy"><span class="gal__cap"><small>Bench build</small>{c}</span></a>' for i, (f, c) in enumerate(more))
    others = [
        dict(title="AgroCool+", brand="AgroCool+", tagline="Multi-compartment smart freezer", link="https://github.com/Abiodun-Amos/AgroCool_Plus", label="View the code",
             desc="An ESP32 freezer controller that holds a set temperature in each compartment so fruits and vegetables stay fresh longer, with phone monitoring and manual on/off. Pitched at the Nigeria Energy Forum, Lagos (2026)."),
        dict(img="more-emeter.jpg", title="Smart Prepaid Energy Meter", desc="Real-time monitoring and remote prepaid credit management, with live readings and relay control.",
             link="https://emeter.onrender.com/", label="Live dashboard"),
        dict(img="more-energy.jpg", title="SmartEnergyPro", desc="A smart home energy controller: an ESP32 with relay modules switches two lamps and two sockets, and the dashboard shows real-time load, temperature and energy used.",
             thumbs=[("build-energy-box.jpg", "The SmartEnergyPro box with two lamp holders and two switched sockets"), ("build-energy-inside.jpg", "Inside: an ESP32 wired to relay modules and sensors"),
                     ("build-energy-lamps.jpg", "Testing: both lamps on"), ("build-energy-sockets.jpg", "Testing: both sockets powered")]),
        dict(img="more-weather.jpg", title="Smart Weather Reporting System", desc="An Arduino circuit with sensors and an LCD, designed and simulated in Tinkercad."),
        dict(img="more-collect.jpg", title="CollectAI", desc="A group collection tracker that takes spoken or typed commands and shows how many members have paid."),
    ]
    def pcard(i, o):
        t = html.escape(o["title"])
        img = f'<button class="pcard__img" data-full="img/{o["img"]}" data-caption="{t}" aria-label="View {t} full size"><img src="img/{o["img"]}" alt="{t} screen" loading="lazy"></button>' if o.get("img") else f'<a class="pcard__img pcard__img--text" href="{o["link"]}" target="_blank" rel="noopener"><b>{o["brand"]}</b><span>{o["tagline"]}</span></a>'
        th = "".join(f'<button class="pcard__thumb" data-full="img/{f}" data-caption="{html.escape(c)}" aria-label="{html.escape(c)}"><img src="img/{f}" alt="{html.escape(c)}" loading="lazy"></button>' for f, c in o.get("thumbs", []))
        th = f'<div class="pcard__thumbs">{th}</div>' if th else ""
        ln = f'<a class="link" href="{o["link"]}" target="_blank" rel="noopener">{o["label"]} {UPRIGHT}</a>' if o.get("link") else ""
        return f'<article class="pcard reveal" style="--d:{i%2}">{img}{th}<h3>{o["title"]}</h3><p>{o["desc"]}</p>{ln}</article>'
    cards = "".join(pcard(i, o) for i, o in enumerate(others))
    webs = [
        dict(title="Loft Essence", brand="Loft Essence", tagline="Print It. Brand It. Own It.", link="https://loftessence.vercel.app/", label="Visit site",
             desc="Website for a custom printing and branding business in Ibadan, with services, a shop, gallery, FAQ, quote requests and WhatsApp ordering."),
        dict(img="web-prixima.jpg", title="Prixima", link="https://prixima-project.vercel.app/", label="Visit site",
             desc="Agency website built with Bootstrap 5: hero slider, services, portfolio, team, reviews, blog and a contact form."),
        dict(img="web-bootcamp.jpg", title="Frontend Bootcamp", link="https://frontend-bootcamp.vercel.app/", label="Visit site",
             desc="Course landing page for a web development bootcamp, with what you'll learn, questions, instructors and a newsletter sign-up."),
        dict(img="web-edgeledger.jpg", title="EdgeLedger", link="https://edgeledger-three.vercel.app/", label="Visit site",
             desc="Landing page with a full-width city hero, navigation and a call to action."),
        dict(img="web-hotel.jpg", title="Hotel website", link="https://hotel-website-psi.vercel.app/", label="Visit site",
             desc="Hotel landing page with a photo hero and Home, About and Contact sections."),
    ]
    webcards = "".join(pcard(i, o) for i, o in enumerate(webs))
    return head("Projects by Amos Abiodun", "Case studies in IoT, machine learning, computer vision and data science by Amos Abiodun.", "projects.html") + phead(
        "Work", ("01", "Projects"), ["Selected", "projects"],
        "Three case studies with live systems you can open, more hardware and software projects, websites I have built, and builds from the workbench. I have built more than 20 projects; these are the ones I can show.") + f'''
<section class="section wrap" style="padding-top:0">
  <div class="filters" data-target=".work__item" role="group" aria-label="Filter projects">
    <button aria-pressed="true" data-filter="all">All</button>
    <button aria-pressed="false" data-filter="ai">AI and Machine Learning</button>
    <button aria-pressed="false" data-filter="iot">IoT and Embedded</button>
    <button aria-pressed="false" data-filter="data">Data Science</button>
  </div>
  {work_items(PROJECTS)}
</section>
<section class="section wrap" style="padding-top:0">
  {eyebrow("02", "More projects")}
  <h2 class="h-lg reveal" style="margin-bottom:clamp(32px,5vw,60px)">Also built.</h2>
  <div class="pcards">{cards}</div>
</section>
<section class="section wrap" style="padding-top:0">
  {eyebrow("03", "Web design")}
  <div class="next" style="margin-bottom:clamp(32px,5vw,60px)">
    <h2 class="h-lg reveal">Websites.</h2>
    <a class="link reveal" href="{GITHUB}" target="_blank" rel="noopener">GitHub {UPRIGHT}</a>
  </div>
  <div class="pcards">{webcards}</div>
</section>
<section class="section section--alt"><div class="wrap">
  {eyebrow("04", "From the workbench")}
  <div class="next" style="margin-bottom:clamp(32px,5vw,60px)">
    <h2 class="h-lg reveal">Hardware builds.</h2>
    <a class="link reveal" href="gallery.html">Open the gallery {UPRIGHT}</a>
  </div>
  <div class="gal" style="columns:4 220px">{grid}</div>
</div></section>
{cta_section()}
{lightbox()}
''' + foot()

def page_case(p, nxt):
    built = "".join(f"<p>{t}</p>" for t in p["built"])
    prob = "".join(f"<p>{t}</p>" for t in p["problem"])
    pts = "".join(f"<li>{t}</li>" for t in p["points"])
    shots = "".join(f'<button class="gal__item reveal" data-full="img/{f}" data-caption="{html.escape(c)}" style="--d:{i%2}"><img src="img/{f}" alt="{html.escape(c)}" loading="lazy"><span class="gal__cap"><small>{lab}</small>{c}</span></button>' for i, (f, lab, c) in enumerate(p["shots"]))
    words = p["title"].split(" ")
    half = math.ceil(len(words) / 2)
    return head(p["title"], p["short"], "projects.html") + phead(
        p["n"], (p["n"], "Case study"), [" ".join(words[:half]), " ".join(words[half:])], p["short"]) + f'''
<section class="wrap">
  <dl class="case__meta reveal">
    <div><dt>Category</dt><dd>{p["catlabel"]}</dd></div>
    <div><dt>Year</dt><dd>{p["year"]}</dd></div>
    <div><dt>My role</dt><dd>{p["role"]}</dd></div>
    <div><dt>Status</dt><dd>Live</dd></div>
  </dl>
</section>
<section class="section wrap" style="padding-bottom:0"><div class="case__hero clip"><img src="img/{p["img"]}" alt="{p["alt"]}"></div></section>
<section class="section wrap">
  <div class="case__grid">
    <h2 class="reveal">The problem</h2><div class="case__txt reveal">{prob}</div>
    <h2 class="reveal">What I built</h2><div class="case__txt reveal">{built}</div>
    <h2 class="reveal">What it does</h2><div class="case__txt reveal"><ul class="ticks">{pts}</ul></div>
    <h2 class="reveal">Tools and technologies</h2><div class="case__txt reveal">{tags(p["tools"])}</div>
    <h2 class="reveal">See it running</h2><div class="case__txt reveal"><a class="btn" href="{p["live"]}" target="_blank" rel="noopener"><span class="ico">{UPRIGHT}</span>{p["livelabel"]}</a><p class="note">{p["note"]}</p></div>
  </div>
</section>
<section class="section wrap" style="padding-top:0">
  {eyebrow("+", "Inside the build")}
  <div class="gal gal--shots">{shots}</div>
</section>
{lightbox()}
<section class="section section--alt"><div class="wrap">
  {eyebrow("→", "Next project")}
  <div class="next"><a class="big reveal" href="{nxt["slug"]}.html">{nxt["title"]} {UPRIGHT}</a><a class="link reveal" href="projects.html">All projects {UPRIGHT}</a></div>
</div></section>
''' + foot()

def page_expertise():
    return head("Expertise of Amos Abiodun", "Electrical and electronics engineering, embedded systems and IoT, AI and machine learning, data science, public speaking and STEM instruction.", "expertise.html") + phead(
        "Skills", ("02", "Expertise"), ["Areas of", "expertise"],
        "Six areas I work in. Select any one to see the skills behind it and the work it produced.") + f'''
<section class="section wrap" style="padding-top:0">{xp_rows(expand=True)}</section>
<section class="section section--alt"><div class="wrap">
  {eyebrow("→", "How I work")}
  <div class="statement">
    <h2 class="h-lg reveal">Research, build, test, teach.</h2>
    <p class="statement__a reveal">Every project starts with the problem and the people who have it. I prototype early in hardware or code, measure it against real data, and write down what I learn so the next person can <span class="hl">build on it</span>.</p>
    <p class="statement__b reveal" style="--d:1">The same habit carries into my talks and training sessions. If I cannot explain a system plainly, I do not understand it well enough yet.</p>
  </div>
</div></section>
{cta_section()}
''' + foot()

TIMELINE = [
    ("2026 to now", "Lead STEM Instructor", "Talent Code Africa, at Lead British International School, Ibadan",
     "I lead the STEM and robotics programme for more than 200 students across ten year groups, primary Year 1 to 6 and secondary Year 7, 8, 10 and 11. I plan the curriculum, write the project guides, and run the practical sessions with Arduino starter kits and LEGO WeDo 2.0."),
    ("2026", "Machine Learning Engineer (contract)", "Freelance, paid client project",
     "Built and deployed a decision tree model that predicts congestion on telecom network data with accuracy above 85%, and a web app that maps congestion risk by location and recommends an action for each."),
    ("2026", "B.Eng. Electrical/Electronics Engineering, Second Class Upper (2:1)", "Olabisi Onabanjo University, Ibogun Campus",
     "Final-year project: an AI facial recognition attendance system. In June 2026 my team took first position at the university's Inter-Faculty Competition for Research Innovations, and I pitched at the Nigeria Energy Forum student energy pitch challenge."),
    ("2025 to 2026", "STEM and Robotics Instructor (contract)", "FebDec Technologies",
     "Designed and ran a 12-week robotics and hardware engineering training programme for 33 students with a co-trainer, covering microcontroller architectures, sensor integration and circuit design. Led STEM outreach to secondary schools with live demonstrations."),
    ("2025 to 2026", "General Secretary", "NIEEESA, Olabisi Onabanjo University chapter",
     "Chief administrative officer of the departmental student association. Planned and ran NIEEESA Week, including a technical symposium and skill-acquisition sessions, and moderated its panel discussions."),
    ("2025", "SIWES Intern", "Nigerian Airspace Management Agency (NAMA), Ibadan Airport",
     "Took part in installing and maintaining VSAT systems, and worked with aviation equipment including VHF radios, Instrument Landing Systems, VOR and voice communication equipment. Learned how redundancy and safety shape engineering in aviation."),
    ("2024", "Facilitator", "Build-A-Thon Holiday Camp, National Centre for Artificial Intelligence and Robotics (NCAIR)",
     "Trained students in foundational robotics and AI concepts with hands-on electronics and programming on single-board computers, and mentored a team through their AI tasks."),
    ("2024", "First place, 1st of 23, TRAIL OOU x DSN data science competition", "Data Science Nigeria, TRAIL and exploreCSR, on Zindi",
     "Built the top-ranked model for predicting which customers will default on a loan. Also completed TRAIL (The Route to Artificial Intelligence Learning) training in research methodology, data literacy, Excel, Power BI and Python for data science."),
    ("2020", "Senior Secondary School Certificate", "Loyola College, Ibadan",
     "Assistant Health Prefect. Cleared O'level results in a single sitting."),
]
AWARDS = [
    ("2026", "First position, Inter-Faculty Competition for Research Innovations", "Directorate of Research, Olabisi Onabanjo University. Team award, 17 June 2026."),
    ("2026", "Institutional representative, Student Energy Pitch Challenge", "Nigeria Energy Forum, Lagos. 30 June 2026."),
    ("2026", "Institutional representative, BUESA Competition", "Bells University Engineering Students' Association technical exhibition."),
    ("2026", "Certificate, Introduction to Safeguarding and Child Protection", "Lagos State Domestic and Sexual Violence Agency (DSVA) and Office of Education Quality Assurance (OEQA). 15 September 2026."),
    ("2025", "Elected General Secretary, NIEEESA", "Olabisi Onabanjo University chapter. Election held 11 December 2025."),
    ("2024", "First place, 1st of 23, TRAIL OOU x DSN data science competition", "Predicting which customers will default on a loan, on Zindi. Organised by Data Science Nigeria, TRAIL and exploreCSR. 3 May 2024."),
    ("2024", "Certificate of participation, TRAIL", "The Route to Artificial Intelligence Learning, Olabisi Onabanjo University."),
    ("2020", "Beneficiary, LOCOBA Class '98 exam fee funding", "One of 15 students selected on merit by the Loyola College Old Boys Association."),
]
CERTS = [
    ("cert-nef.jpg", "Nigeria Energy Forum 2026", "Certificate of participation, Day 1, 30 June 2026", "Nigeria Energy Forum 2026 certificate of participation awarded to Abiodun Amos"),
    ("award-research.jpg", "First position, Research Innovations", "OOU Directorate of Research, 17 June 2026", "Amos holding the first position trophy and cheque at the OOU Inter-Faculty Competition for Research Innovations"),
    ("cert-zindi.jpg", "First place, 1st of 23", "TRAIL OOU x DSN data science competition on Zindi, 3 May 2024", "Zindi certificate: first place out of 23 in the TRAIL OOU x DSN Data Science Training, predicting customers who will default on a loan"),
    ("cert-safeguarding.jpg", "Safeguarding and Child Protection", "Lagos State DSVA and OEQA, 15 September 2026", "Certificate of achievement for completing Introduction to Safeguarding and Child Protection"),
    ("cert-gensec.jpg", "General Secretary, NIEEESA", "Certificate of return, election of 11 December 2025", "Certificate of return to office as General Secretary of NIEEESA, Olabisi Onabanjo University"),
]

def page_about():
    tl = "".join(f'''<li class="reveal"><time>{y}</time><div><h3>{t}</h3><p class="org">{o}</p><p>{d}</p></div></li>''' for y, t, o, d in TIMELINE)
    aw = "".join(f'<li class="reveal"><time>{y}</time><b>{t}</b><span>{d}</span></li>' for y, t, d in AWARDS)
    certs = "".join(f'<button class="cert reveal" data-full="img/{f}" data-caption="{html.escape(a)}" style="--d:{i}"><img src="img/{f}" alt="{html.escape(a)}" loading="lazy"><div><b>{t}</b><span>{s}</span></div></button>' for i, (f, t, s, a) in enumerate(CERTS))
    return head("About Amos Abiodun", "The professional journey of Amos Abiodun: engineering education, industrial training, projects, awards and certificates.", "about.html") + phead(
        "About", ("03", "About"), ["Engineer at the core.", "Versatile by design."],
        "I am an Electrical/Electronics engineer working across embedded systems and IoT, machine learning and data science. I build systems end to end, from the circuit to the model to the dashboard, and I speak about that work in public.") + f'''
<section class="section wrap" style="padding-top:0">
  <div class="split split--bio">
    <div class="split__media"><div class="frame clip" style="aspect-ratio:4/5"><img src="img/amos-vest.jpg" alt="Amos Abiodun smiling in a safety vest, arms folded" data-speed="-0.03"></div></div>
    <div class="split__text">
      {eyebrow("→", "Biography")}
      <h2 class="h-md reveal">I am Amos Olaoluwa Abiodun, an Electrical/Electronics engineer based in Ibadan, Nigeria.</h2>
      <p class="body reveal">My engineering work sits where hardware meets intelligent software: embedded systems, the Internet of Things, and machine learning. I have built an AI attendance system that recognises faces, an IoT system that predicts fruit spoilage, a multi-compartment smart freezer, and a model that forecasts congestion on telecom networks.</p>
      <p class="body reveal">I trained on aviation communication and navigation systems at the Nigerian Airspace Management Agency, and in 2026 my team took first position at my university's Inter-Faculty Competition for Research Innovations.</p>
      <p class="body reveal">I also speak and moderate at technology events, and as a STEM Instructor I have trained more than 300 students in robotics and electronics.</p>
      <p class="body reveal">I speak English and Yoruba.</p>
      <div class="cta__row reveal"><a class="btn" href="projects.html"><span class="ico">{ARROW}</span>See my projects</a><a class="btn btn--ghost" href="{CV}" download>Download my CV</a><a class="link" href="{LINKEDIN}">LinkedIn {UPRIGHT}</a></div>
    </div>
  </div>
</section>
<section class="section section--alt"><div class="wrap">{eyebrow("→", "In numbers")}{STATS}</div></section>
<section class="section wrap">
  {eyebrow("→", "Professional journey")}
  <h2 class="h-lg reveal" style="margin-bottom:clamp(40px,6vw,80px)">The path so far.</h2>
  <ol class="tl"><span class="tl__fill" aria-hidden="true"></span>{tl}</ol>
</section>
<section class="section section--alt" id="credentials"><div class="wrap">
  {eyebrow("→", "Achievements and credentials")}
  <h2 class="h-lg reveal" style="margin-bottom:clamp(32px,5vw,60px)">Awards, competitions and certificates.</h2>
  <ul class="cred">{aw}</ul>
  <div class="certs">{certs}</div>
</div></section>
{cta_section()}
{lightbox()}
''' + foot()

TALKS = [
    ("01", "NIEEESA Week technical symposium", "Moderated panel discussions on emerging trends in technology and engineering. Olabisi Onabanjo University."),
    ("02", "Tech skill-acquisition events", "Spoke to engineering students about building practical skills alongside their degree."),
    ("03", "Student Energy Pitch Challenge, Nigeria Energy Forum", "Represented Olabisi Onabanjo University, pitching AgroCool+, a multi-compartment smart freezer that keeps fruits and vegetables fresh for longer. Lagos, June 2026."),
    ("04", "Inter-Faculty Competition for Research Innovations", "Presented research for the Electrical/Electronics Engineering department. First position. June 2026."),
    ("05", "STEM outreach to secondary schools", "Live demonstrations of electrical components and robotics for secondary school students."),
]
TOPICS = ["Getting started in robotics with Arduino", "IoT and machine learning for everyday problems", "Teaching STEM hands-on", "Building a tech portfolio as an engineering student", "AI and computer vision, explained simply"]

def page_speaking():
    talks = "".join(f'<li class="reveal"><i>{n}</i><b>{t}</b><span>{d}</span></li>' for n, t, d in TALKS)
    topics = "".join(f"<li>{t}</li>" for t in TOPICS)
    return head("Speaking by Amos Abiodun", "Amos Abiodun moderates panels, speaks at technology events and pitches engineering projects. Invite him to speak.", "speaking.html") + phead(
        "Talks", ("04", "Speaking"), ["Ideas are powerful.", 'Sharing them <span class="hl" style="display:inline">creates impact.</span>'],
        "I moderate panels, speak at technology and skill-acquisition events, pitch projects, and run STEM workshops. I have moderated more than five events.") + f'''
<section class="section section--tight wrap" style="padding-top:0">
  <div class="pair">
    <div class="frame clip"><img src="img/speak-podium.jpg" alt="Amos Abiodun speaking with a microphone beside a podium at Olabisi Onabanjo University" data-speed="-0.03"></div>
    <div class="frame clip"><img src="img/speak-mic.jpg" alt="Amos Abiodun smiling while speaking into a microphone at a podium" data-speed="0.03"></div>
  </div>
</section>
<section class="section section--alt"><div class="wrap">
  {eyebrow("→", "Where I have spoken")}
  <h2 class="h-lg reveal" style="margin-bottom:clamp(32px,5vw,60px)">Panels, pitches and workshops.</h2>
  <ul class="talks">{talks}</ul>
</div></section>
<section class="section wrap">
  <div class="split">
    <div class="split__text">
      {eyebrow("→", "Topics")}
      <h2 class="h-lg reveal">What I can speak about.</h2>
      <p class="body reveal">I keep talks practical, with demonstrations where the venue allows. I can speak to students, schools, parents or professionals, and I can moderate panels.</p>
      <a class="btn reveal" href="contact.html"><span class="ico">{ARROW}</span>Invite me to speak</a>
    </div>
    <div class="split__media"><ul class="ticks reveal">{topics}</ul></div>
  </div>
</section>
{cta_section()}
''' + foot()

GALLERY = [
    # (file in dist/img, filter categories, label, caption). To add a photo: put it in dist/img and add a line here.
    ("build-energy-box.jpg", "builds", "Builds", "SmartEnergyPro: two lamp holders and two switched sockets, one labelled Fan, in a single enclosure."),
    ("cert-zindi.jpg", "awards", "Awards", "First place, 1st of 23, TRAIL OOU x DSN Data Science Training on Zindi: predicting customers who will default on a loan, 3 May 2024."),
    ("train-build.jpg", "training", "STEM instruction", "Demonstrating a build step with a glue gun, with the step-by-step guide on the board behind."),
    ("build-energy-inside.jpg", "builds", "Builds", "Inside SmartEnergyPro: an ESP32 wired to relay modules and sensors."),
    ("code-jupyter.jpg", "code", "Code", "Working with NumPy arrays in a Jupyter notebook."),
    ("build-esp32.jpg", "builds", "Builds", "An ESP32-WROOM-32D development board powered up inside a project enclosure."),
    ("cert-safeguarding.jpg", "awards", "Certificates", "Introduction to Safeguarding and Child Protection, Lagos State DSVA and OEQA, 15 September 2026."),
    ("build-energy-lamps.jpg", "builds", "Builds", "Testing SmartEnergyPro: both lamps on."),
    ("code-pictoblox.jpg", "code training", "Code", "A paddle-and-ball game with a score, built with blocks in PictoBlox."),
    ("shot-fruit-fritzing.jpg", "builds", "Builds", "The Smart Fruit Monitor circuit drawn in Fritzing: ESP32, gas sensor, temperature and humidity sensor, camera module and two batteries."),
    ("build-energy-sockets.jpg", "builds", "Builds", "Testing SmartEnergyPro: both sockets powered."),
    ("cert-gensec.jpg", "awards", "Leadership", "Certificate of return: elected General Secretary of NIEEESA, Olabisi Onabanjo University, 11 December 2025."),
    ("build-nodemcu.jpg", "builds", "Builds", "A NodeMCU V3 (ESP8266) board connected for programming in the Arduino IDE."),
    ("field-vsat.jpg", "field", "Field", "Working on the electronics of a satellite dish (VSAT) installation."),
    ("award-research.jpg", "awards", "Awards", "First position at the Inter-Faculty Competition for Research Innovations, OOU Directorate of Research, 17 June 2026."),
    ("build-meter.jpg", "builds", "Builds", "An energy meter prototype showing energy, power, voltage and current, with a GSM link."),
    ("field-vcs.jpg", "field", "Field", "Beside a voice communication system equipment rack."),
    ("build-rfid.jpg", "builds", "Builds", "An ESP32 build with an RFID reader, keypad and display, programmed in the Arduino IDE."),
    ("speak-mic.jpg", "speaking", "Speaking", "Speaking at a campus event."),
    ("amos-outdoor.jpg", "portraits", "Portrait", "Amos Abiodun."),
    ("build-assembly.jpg", "builds", "Builds", "Assembling a microcontroller device in its enclosure."),
    ("field-cables.jpg", "field", "Field", "Handling antenna cables on site."),
    ("build-sbc.jpg", "builds", "Builds", "A single-board computer with a battery pack and voltage regulator inside a project enclosure."),
    ("build-camera.jpg", "builds", "Builds", "A camera unit with a cooling fan in its enclosure."),
    ("speak-podium.jpg", "speaking", "Speaking", "At the podium, Olabisi Onabanjo University."),
    ("build-drone.jpg", "builds", "Builds", "A drone and its controller on the workbench, with an Arduino board and jumper wires."),
    ("amos-vest.jpg", "portraits field", "Portrait", "On site in a safety vest."),
    ("event-febdec.jpg", "training", "STEM instruction", "With robotics kits and test equipment at a FebDec Technologies event."),
    ("train-arduino.jpg", "training", "STEM instruction", "Explaining the Arduino Uno board in a training session."),
    ("build-ultrasonic.jpg", "builds robotics", "Robotics", "Arduino and ultrasonic sensor models on a cardboard road layout."),
    ("kit-lift.jpg", "robotics", "Robotics", "A LEGO WeDo 2.0 lift vehicle beside an Arduino ultrasonic sensor circuit."),
    ("train-lab.jpg", "training", "STEM instruction", "Leading an Arduino session in a computer lab."),
    ("kit-program.jpg", "robotics", "Robotics", "A LEGO WeDo 2.0 model with the block program that drives it."),
    ("field-site.jpg", "field", "Field", "Field work on site."),
    ("kit-sensor-car.jpg", "robotics", "Robotics", "A LEGO WeDo 2.0 car fitted with a motion sensor."),
    ("cert-nef.jpg", "awards", "Awards", "Nigeria Energy Forum 2026, certificate of participation."),
    ("kit-car.jpg", "robotics", "Robotics", "A motorised LEGO WeDo 2.0 car beside its parts tray."),
    ("kit-belt.jpg", "robotics", "Robotics", "A LEGO WeDo 2.0 build with a belt drive."),
    ("lab-setup.jpg", "training", "STEM instruction", "A computer lab set up for a session."),
    ("kit-vehicle.jpg", "robotics", "Robotics", "A LEGO WeDo 2.0 vehicle, close up."),
    ("amos-campus.jpg", "portraits", "Portrait", "On campus at Olabisi Onabanjo University."),
]

def page_gallery():
    items = "".join(f'<button class="gal__item reveal" data-cat="{c}" data-full="img/{f}" data-caption="{html.escape(cap)}" style="--d:{i%3}"><img src="img/{f}" alt="{html.escape(cap)}" loading="lazy"><span class="gal__cap"><small>{lab}</small>{cap}</span></button>' for i, (f, c, lab, cap) in enumerate(GALLERY))
    return head("Gallery of Amos Abiodun", "Photos of builds, field work, speaking, awards and STEM instruction by Amos Abiodun.", "gallery.html") + phead(
        "Gallery", ("05", "Gallery"), ["Work, in", "pictures"],
        "Builds from the workbench, field sites, stages and training sessions. Select a photo to view it full size.") + f'''
<section class="section wrap" style="padding-top:0">
  <div class="filters" data-target=".gal__item" role="group" aria-label="Filter photos">
    <button aria-pressed="true" data-filter="all">All</button>
    <button aria-pressed="false" data-filter="builds">Builds</button>
    <button aria-pressed="false" data-filter="field">Field</button>
    <button aria-pressed="false" data-filter="robotics">Robotics</button>
    <button aria-pressed="false" data-filter="speaking">Speaking</button>
    <button aria-pressed="false" data-filter="training">STEM instruction</button>
    <button aria-pressed="false" data-filter="code">Code</button>
    <button aria-pressed="false" data-filter="awards">Awards and certificates</button>
    <button aria-pressed="false" data-filter="portraits">Portraits</button>
  </div>
  <div class="gal">{items}</div>
</section>
{cta_section()}
{lightbox()}
''' + foot()

def page_contact():
    return head("Contact Amos Abiodun", "Contact Amos Abiodun by email, phone or WhatsApp about engineering projects, STEM instruction and speaking.", "contact.html") + phead(
        "Hello", ("06", "Contact"), ["Have an idea?", '<span class="hl" style="display:inline">Let\'s build</span> it.'],
        "Whether you're exploring an engineering project, seeking a STEM instructor, planning a technology initiative, or looking for a speaker, I'd love to hear from you.") + f'''
<section class="section wrap" style="padding-top:0">
  <div class="contact">
    <div class="contact__info">
      {eyebrow("→", "Reach me directly")}
      <span class="pill reveal">Available for work</span>
      <ul class="ways">
        <li class="reveal"><a href="mailto:{EMAIL}"><small>Email</small><b>{EMAIL}</b>{UPRIGHT}</a></li>
        <li class="reveal"><a href="{WA}"><small>WhatsApp</small><b>Chat with me on WhatsApp</b>{UPRIGHT}</a></li>
        <li class="reveal"><a href="tel:{PHONE_TEL}"><small>Phone</small><b>{PHONE_SHOW}</b>{UPRIGHT}</a></li>
        <li class="reveal"><a href="{CV}" download><small>CV</small><b>Download my CV (PDF)</b>{DL}</a></li>
        <li class="reveal"><a href="{LINKEDIN}"><small>LinkedIn</small><b>linkedin.com/in/abiodun-amos</b>{UPRIGHT}</a></li>
        <li class="reveal"><a href="{GITHUB}"><small>GitHub</small><b>github.com/Abiodun-Amos</b>{UPRIGHT}</a></li>
      </ul>
      <figure class="hello reveal">
        <img src="img/amos-portrait-2.webp" alt="Amos Abiodun smiling in a shirt and tie" width="958" height="1300" loading="lazy">
        <figcaption><b>Amos Abiodun</b>Based in Ibadan, Nigeria. Open to work on site and remotely.</figcaption>
      </figure>
    </div>
    <div class="contact__form">
      {eyebrow("→", "Write a message")}
      <form id="contact-form" class="reveal">
        <label class="field" for="cf-name"><span>Your name</span><input id="cf-name" name="name" type="text" autocomplete="name" required></label>
        <label class="field" for="cf-email"><span>Your email</span><input id="cf-email" name="email" type="email" autocomplete="email"></label>
        <label class="field" for="cf-topic"><span>What is this about?</span><select id="cf-topic" name="topic"><option>Engineering project</option><option>Machine learning</option><option>Data science</option><option>Software design</option><option>STEM instruction</option><option>Speaking invitation</option><option>Job opportunity</option><option>Something else</option></select></label>
        <label class="field" for="cf-message"><span>Your message</span><textarea id="cf-message" name="message" required></textarea></label>
        <button class="btn" type="submit"><span class="ico">{ARROW}</span>Prepare my message</button>
      </form>
      <div class="sendbox" id="sendbox" hidden>
        <p>Your message is ready. Choose how to send it.</p>
        <pre id="send-preview"></pre>
        <div class="cta__row">
          <a class="btn" id="send-wa" href="{WA}" target="_blank" rel="noopener"><span class="ico">{UPRIGHT}</span>Send on WhatsApp</a>
          <a class="btn btn--ghost" id="send-gmail" href="https://mail.google.com/mail/?view=cm&fs=1&to={EMAIL}" target="_blank" rel="noopener">Send with Gmail</a>
          <a class="btn btn--ghost" id="send-mail" href="mailto:{EMAIL}" target="_blank" rel="noopener">Open my mail app</a>
          <button class="btn btn--ghost" id="send-copy" type="button">Copy message</button>
        </div>
        <p class="note">No mail app on this device? Use Gmail, or copy the message and send it to {EMAIL}.</p>
      </div>
    </div>
  </div>
</section>
''' + foot()

def page_404():
    return head("Page not found: Amos Abiodun", "This page does not exist on the Amos Abiodun portfolio.", "") + phead(
        "404", ("404", "Page not found"), ["This page", "is not here."],
        "The link may be old or mistyped. The home page and the projects page are a good place to start again.") + f'''
<section class="section wrap" style="padding-top:0"><div class="cta__row"><a class="btn" href="/index.html"><span class="ico">{ARROW}</span>Go to the home page</a><a class="btn btn--ghost" href="/projects.html">See projects</a></div></section>
''' + foot()

PERSON = {"@type": "Person", "@id": SITE_URL + "/#amos", "name": "Amos Abiodun", "alternateName": ["Amos Olaoluwa Abiodun", "Abiodun Amos", "Engr. Amos Abiodun"],
          "givenName": "Amos", "additionalName": "Olaoluwa", "familyName": "Abiodun", "url": SITE_URL + "/", "image": SITE_URL + "/img/amos-portrait.png",
          "jobTitle": "Electrical/Electronics Engineer", "description": "Electrical/Electronics engineer in Ibadan, Nigeria, working across embedded systems, IoT, machine learning and data science.",
          "email": "mailto:" + EMAIL, "telephone": PHONE_TEL,
          "address": {"@type": "PostalAddress", "addressLocality": "Ibadan", "addressRegion": "Oyo", "addressCountry": "NG"},
          "knowsAbout": ["Electrical and Electronics Engineering", "Embedded Systems", "Internet of Things", "Machine Learning", "Data Science", "Robotics", "Public Speaking"],
          "sameAs": [LINKEDIN, GITHUB]}
def seo(name):
    url = SITE_URL + "/" + ("" if name == "index.html" else name)
    out = f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">'
    if name == "404.html":
        return '<meta name="robots" content="noindex">'
    graph = [PERSON, {"@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": "Amos Abiodun", "alternateName": "Amos Abiodun Portfolio", "inLanguage": "en", "publisher": {"@id": SITE_URL + "/#amos"}}]
    if name in ("index.html", "about.html"):
        graph.append({"@type": "ProfilePage", "url": url, "mainEntity": {"@id": SITE_URL + "/#amos"}})
    return out + '\n<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"

pages = {"index.html": page_home(), "projects.html": page_projects(), "expertise.html": page_expertise(),
         "about.html": page_about(), "speaking.html": page_speaking(), "gallery.html": page_gallery(), "contact.html": page_contact()}
for i, p in enumerate(PROJECTS):
    pages[p["slug"] + ".html"] = page_case(p, PROJECTS[(i + 1) % len(PROJECTS)])
pages["404.html"] = page_404()
for name, body in pages.items():
    body = body.replace("<!--SEO-->", seo(name))
    if name == "404.html":
        body = body.replace('<meta name="robots" content="index, follow">\n', "").replace('href="css/', 'href="/css/').replace('src="js/', 'src="/js/').replace('src="img/', 'src="/img/').replace('href="favicon', 'href="/favicon').replace('href="img/', 'href="/img/')
        for h, _ in NAV: body = body.replace(f'href="{h}"', f'href="/{h}"')
        body = body.replace('href="index.html"', 'href="/index.html"').replace(f'href="{CV}"', f'href="/{CV}"')
    (OUT / name).write_text(body, encoding="utf-8")
    print(name, len(body) // 1024, "KB")

today = datetime.date.today().isoformat()
urls = "".join(f"  <url><loc>{SITE_URL}/{'' if n == 'index.html' else n}</loc><lastmod>{today}</lastmod></url>\n" for n in pages if n != "404.html")
(OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
