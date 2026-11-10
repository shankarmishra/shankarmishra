"""Render the animated SVG cards for the profile README.
GitHub strips scripts and CSS from READMEs, and SVGs shown through <img> cannot load
web fonts, so each card carries its own CSS keyframes + SMIL and uses system fonts.
Run: python scripts/render_cards.py        (STATIC=1 renders end states for screenshots)
"""
import json, os, html
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cards")
STATIC = os.environ.get("STATIC") == "1"
BG, CARD, LINE = "#0a0f1c", "#0d1322", "#1c2740"
INK, MUTE, GREEN, BLUE = "#e8eefc", "#8a97b5", "#17E8A0", "#4f8cff"
SANS = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SERIF = "Georgia,'Times New Roman',serif"
e = html.escape

CSS_BASE = f"""
<style>
text{{font-family:{SANS}}}
.m{{font-family:{MONO}}} .s{{font-family:{SERIF}}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes pulse{{0%,100%{{opacity:.25}}50%{{opacity:.9}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes swing{{0%{{opacity:0;transform:translateY(22px) rotate(-2deg)}}70%{{transform:translateY(-4px) rotate(.4deg)}}100%{{opacity:1;transform:none}}}}
.up{{animation:up .8s cubic-bezier(.2,.7,.2,1) both}}
.bar{{transform-box:fill-box;transform-origin:bottom;animation:grow .9s cubic-bezier(.2,.7,.2,1) both}}
.ring{{animation:pulse 2.8s ease-in-out infinite}}
.cur{{animation:blink 1s steps(1) infinite}}
.tile{{animation:swing .9s cubic-bezier(.2,.8,.2,1) both}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>"""
if STATIC:
    CSS_BASE = CSS_BASE.replace("both}", "both;animation-duration:0s}")


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f"<defs>{defs}</defs>{CSS_BASE}{body}</svg>")


def write(name, s):
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), "w", encoding="utf8").write(s)


def shine(id_, w, dur=4.5):
    """Moving highlight; background-clip:text does not exist in SVG, so animate a gradient."""
    a = "" if STATIC else (f'<animateTransform attributeName="gradientTransform" type="translate" '
                           f'from="-1 0" to="1 0" dur="{dur}s" repeatCount="indefinite"/>')
    return (f'<linearGradient id="{id_}" x1="0" x2="1" y1="0" y2="0" gradientUnits="objectBoundingBox">'
            f'<stop offset="0" stop-color="{INK}"/><stop offset=".42" stop-color="{INK}"/>'
            f'<stop offset=".5" stop-color="{GREEN}"/><stop offset=".58" stop-color="{INK}"/>'
            f'<stop offset="1" stop-color="{INK}"/>{a}</linearGradient>')


def d(i, base=0.0):
    return "" if STATIC else f' style="animation-delay:{base + i * 0.12:.2f}s"'


# ---------------------------------------------------------------- hero
def hero():
    chips = ["Python", "Flask / FastAPI", "LLM apps", "PostgreSQL", "AWS"]
    cx, chip_svg = 40, ""
    for i, c in enumerate(chips):
        wd = 18 + len(c) * 8.2
        chip_svg += (f'<g class="up"{d(i, 1.4)}><rect x="{cx}" y="188" width="{wd:.0f}" height="30" rx="15" '
                     f'fill="{CARD}" stroke="{LINE}"/><text x="{cx + wd / 2:.0f}" y="208" text-anchor="middle" '
                     f'font-size="13" fill="{MUTE}" class="m">{e(c)}</text></g>')
        cx += wd + 10
    body = f"""
<rect width="880" height="250" rx="18" fill="{BG}"/>
<rect x=".5" y=".5" width="879" height="249" rx="17.5" fill="none" stroke="{LINE}"/>
<circle cx="800" cy="40" r="120" fill="{GREEN}" opacity=".05"/><circle cx="840" cy="210" r="90" fill="{BLUE}" opacity=".06"/>
<g class="up"{d(0)}><circle cx="46" cy="46" r="5" fill="{GREEN}" class="ring"/>
<text x="60" y="51" font-size="13" fill="{GREEN}" class="m" letter-spacing="1.5">OPEN TO WORK</text></g>
<g class="up"{d(1)}><text x="40" y="112" font-size="54" class="s" fill="{INK}">Shankar</text>
<text x="264" y="112" font-size="54" class="s" fill="url(#sh)" font-style="italic">Mishra</text></g>
<g class="up"{d(2)}><text x="40" y="152" font-size="19" fill="{MUTE}">Python developer who puts LLM features into production.</text>
<text x="40" y="174" font-size="14" fill="{MUTE}" class="m">Mumbai first. Noida, other cities and remote also fine.<tspan class="cur" fill="{GREEN}"> _</tspan></text></g>
{chip_svg}"""
    write("hero.svg", svg(880, 250, body, shine("sh", 200)))


# ---------------------------------------------------------------- tiles
def tile(name, num, label, sub, color, idx):
    steps, dt, t0 = 18, 0.05, 0.5 + idx * 0.25
    digits = []
    for i in range(steps + 1):
        v = round(num * (i / steps) ** 2) if not STATIC else num
        txt = f"{v:,}"
        if STATIC and i < steps:
            continue
        vis = ""
        if not STATIC:
            vis = f'<set attributeName="visibility" to="visible" begin="{t0 + i * dt:.2f}s" fill="freeze"/>'
            if i < steps:
                vis += f'<set attributeName="visibility" to="hidden" begin="{t0 + (i + 1) * dt:.2f}s" fill="freeze"/>'
        init = "visible" if STATIC else "hidden"
        digits.append(f'<text x="28" y="98" font-size="52" font-weight="700" fill="{INK}" '
                      f'visibility="{init}" class="s">{txt}{vis}</text>')
    sh = "" if STATIC else (f'<rect x="-120" y="0" width="70" height="190" fill="url(#g{idx})" opacity=".18" '
                            f'transform="skewX(-20)"><animate attributeName="x" from="-120" to="360" dur="3.6s" '
                            f'begin="{t0 + 1}s;{t0 + 1 + 8}s" repeatCount="indefinite"/></rect>')
    defs = (f'<linearGradient id="g{idx}"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="c{idx}"><rect width="280" height="190" rx="16"/></clipPath>')
    body = f"""<g class="tile"{d(idx, 0.0)}>
<rect width="280" height="190" rx="16" fill="{CARD}"/><rect x=".5" y=".5" width="279" height="189" rx="15.5" fill="none" stroke="{LINE}"/>
<g clip-path="url(#c{idx})">{sh}</g>
<circle cx="236" cy="44" r="22" fill="none" stroke="{color}" stroke-width="2" class="ring"/>
<circle cx="236" cy="44" r="6" fill="{color}"/>
<text x="28" y="46" font-size="12" letter-spacing="2" fill="{color}" class="m">{e(name)}</text>
{''.join(digits)}
<text x="28" y="132" font-size="17" fill="{INK}">{e(label)}</text>
<text x="28" y="156" font-size="13" fill="{MUTE}">{e(sub)}</text></g>"""
    write(f"tile-{idx + 1}.svg", svg(280, 190, body, defs))


# ---------------------------------------------------------------- activity
def activity():
    p = os.path.join(ROOT, "data", "contributions.json")
    months = OrderedDict()
    total = 0
    try:
        cal = json.load(open(p))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total = cal["totalContributions"]
        for wk in cal["weeks"]:
            for day in wk["contributionDays"]:
                months[day["date"][:7]] = months.get(day["date"][:7], 0) + day["contributionCount"]
    except Exception:
        months = OrderedDict((f"2026-{m:02d}", 0) for m in range(1, 13))
    keys = list(months)[-12:]
    vals = [months[k] for k in keys]
    mx = max(vals) or 1
    best = vals.index(max(vals))
    # current streak (days with >0, counting back from the last day)
    streak = 0
    try:
        days = [x["contributionCount"] for wk in cal["weeks"] for x in wk["contributionDays"]]
        for c in reversed(days):
            if c == 0 and streak == 0:
                continue  # today may not have commits yet
            if c == 0:
                break
            streak += 1
    except Exception:
        pass
    mn = "JFMAMJJASOND"
    bars, w = "", 880
    x0, bw, gap, base, top = 56, 40, 28, 190, 84
    for i, (k, v) in enumerate(zip(keys, vals)):
        hh = max(3, (v / mx) * (base - top))
        col = BLUE if i == best else "#24324f"
        bars += (f'<g><rect class="bar" x="{x0 + i * (bw + gap)}" y="{base - hh:.0f}" width="{bw}" height="{hh:.0f}" '
                 f'rx="6" fill="{col}"{d(i, .3)}/>'
                 f'<text x="{x0 + i * (bw + gap) + bw / 2}" y="{base + 20}" text-anchor="middle" font-size="12" fill="{MUTE}" class="m">'
                 f'{mn[int(k[5:]) - 1]}</text>')
        if i == best:
            bars += (f'<text x="{x0 + i * (bw + gap) + bw / 2}" y="{base - hh - 8:.0f}" text-anchor="middle" '
                     f'font-size="13" fill="{INK}" font-weight="700" class="m">{v}</text>')
        bars += "</g>"
    body = f"""<rect width="{w}" height="250" rx="18" fill="{BG}"/><rect x=".5" y=".5" width="{w - 1}" height="249" rx="17.5" fill="none" stroke="{LINE}"/>
<text x="40" y="40" font-size="12" letter-spacing="2" fill="{GREEN}" class="m">ACTIVITY, LAST 12 MONTHS</text>
<text x="{w - 40}" y="40" text-anchor="end" font-size="13" fill="{MUTE}" class="m">{total} contributions · {streak} day streak</text>
{bars}"""
    write("activity.svg", svg(w, 250, body))


# ---------------------------------------------------------------- repo cards
REPOS = [
    ("mini-rag-qa", "Ask questions about your own PDF. Answers come only from the document; a relevance gate skips the LLM when nothing close enough is found.", ["FastAPI", "FAISS", "Groq"], GREEN),
    ("AIVOA", "CRM agent for pharma reps. A form and an LLM chat both go through one LangGraph agent that owns five tools.", ["LangGraph", "FastAPI", "PostgreSQL"], BLUE),
    ("box-selection-system", "Picks the cheapest box an order really fits in, using a 3D packing check that explains every rejection. 78 tests, CI.", ["Django REST", "pytest", "CI"], GREEN),
    ("openhinglish", "Deterministic, explainable Roman-Hinglish text normalization. CPU only, no model download.", ["Python", "MIT"], BLUE),
]


def wrap(t, n):
    out, line = [], ""
    for w_ in t.split():
        if len(line) + len(w_) + 1 > n:
            out.append(line)
            line = w_
        else:
            line = (line + " " + w_).strip()
    return out + [line]


def repos():
    for i, (name, desc, tags, col) in enumerate(REPOS):
        lines = wrap(desc, 58)[:3]
        tx = "".join(f'<text x="28" y="{74 + j * 20}" font-size="13.5" fill="{MUTE}">{e(l)}</text>' for j, l in enumerate(lines))
        cx, tg = 28, ""
        for t in tags:
            wd = 16 + len(t) * 7.6
            tg += (f'<rect x="{cx}" y="136" width="{wd:.0f}" height="24" rx="12" fill="none" stroke="{LINE}"/>'
                   f'<text x="{cx + wd / 2:.0f}" y="152" text-anchor="middle" font-size="11.5" fill="{INK}" class="m">{e(t)}</text>')
            cx += wd + 8
        body = f"""<g class="tile"{d(i % 2, .1)}>
<rect width="430" height="176" rx="16" fill="{CARD}"/><rect x=".5" y=".5" width="429" height="175" rx="15.5" fill="none" stroke="{LINE}"/>
<rect x="0" y="22" width="4" height="28" rx="2" fill="{col}"/>
<text x="28" y="42" font-size="17" font-weight="700" fill="{INK}" class="m">{e(name)}</text>
<text x="402" y="42" text-anchor="end" font-size="16" fill="{col}" class="ring">↗</text>
{tx}{tg}</g>"""
        write(f"repo-{i + 1}.svg", svg(430, 176, body))


if __name__ == "__main__":
    hero()
    tile("BRAHMAI / BACKEND", 79, "Flask API routes", "teacher review, scanner, safety controls", GREEN, 0)
    tile("BRAHMAI / TESTS", 1144, "pytest tests", "135 files, plus 45 Playwright E2E", BLUE, 1)
    tile("BOX SELECTION / CI", 78, "tests, with CI", "Django REST, Python 3.11 and 3.12", GREEN, 2)
    activity()
    repos()
    print("cards written to", OUT)
