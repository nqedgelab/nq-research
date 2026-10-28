"""SVG artwork shared by the book and the hypothesis repos.

Every drawing takes a theme from THEMES, so each image comes in a dark and
a light version for GitHub's <picture> switching.
"""

import math
from pathlib import Path

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(bg1="#0f172a", bg2="#1e293b", fg="#f1f5f9", sub="#94a3b8", grid="#334155",
                 accent="#60a5fa", accent2="#818cf8", muted="#475569", bad="#f87171", good="#4ade80"),
    "light": dict(bg1="#f8fafc", bg2="#e2e8f0", fg="#0f172a", sub="#475569", grid="#cbd5e1",
                  accent="#2563eb", accent2="#6366f1", muted="#94a3b8", bad="#dc2626", good="#16a34a"),
}

# Line icons on a 24x24 grid
ICONS = {
    "record": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v2h6V3M8.5 10h7M8.5 14h7M8.5 18h4"/>',
    "process": '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="9" y="15" width="6" height="6" rx="1"/><path d="M9 6h6M6 9v3h12V9M12 12v3"/>',
    "splits": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M10 10v11M15 10v11"/>',
    "data": '<ellipse cx="12" cy="5.5" rx="8" ry="2.5"/><path d="M4 5.5v13c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5v-13M4 12c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5"/>',
    "map": '<path d="M3 6.5a1.5 1.5 0 0 1 1.5-1.5H9l2 2.5h8.5A1.5 1.5 0 0 1 21 9v9.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"/>',
    "rules": '<path d="M12 3l7.5 3v5.5c0 4.5-3.2 8.2-7.5 9.5-4.3-1.3-7.5-5-7.5-9.5V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "claim": '<path d="M4 5h16v11H10l-6 4z"/><path d="M8 9h8M8 12h5"/>',
    "result": '<path d="M3 21h18"/><path d="M4 16l5-5 4 3 7-8"/><path d="M16 6h4v4"/>',
    "lessons": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "book": '<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H11v17H5.5A1.5 1.5 0 0 1 4 18.5zM20 4.5A1.5 1.5 0 0 0 18.5 3H13v17h5.5a1.5 1.5 0 0 0 1.5-1.5z"/>',
}


def write(folder, name, theme, text):
    Path(folder, f"{name}-{theme}.svg").write_text(text, encoding="utf-8")


def gaussian(x0, x1, base, h, mu, sig, n=200):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append(f"{x:.1f},{base - h * math.exp(-((x - mu) ** 2) / (2 * sig ** 2)):.1f}")
    return "M" + " L".join(pts)


def banner(t, title, subtitle, status, corner=""):
    """Wide header. `status` is SVG text content and may contain <tspan>s."""
    W, H, cx, base = 1200, 300, 880, 232
    grid = "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="{H-40}" stroke="{t["grid"]}" opacity="0.5"/>'
                   for x in range(600, 1180, 60))
    curve = gaussian(620, 1140, base, 140, cx - 6, 62)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <style>
    .pulse {{ animation: pulse 3s ease-in-out infinite; }}
    @keyframes pulse {{ 50% {{ opacity: 0.35; }} }}
    .blink {{ animation: blink 1.2s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .pulse, .blink {{ animation: none; }} }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
    </linearGradient>
    <linearGradient id="under" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.28"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>
  {grid}
  <path d="{curve} L1140,{base} L620,{base} Z" fill="url(#under)"/>
  <path d="{curve}" fill="none" stroke="{t["fg"]}" stroke-width="4" stroke-linecap="round"/>
  <line x1="600" y1="{base}" x2="1160" y2="{base}" stroke="{t["sub"]}" stroke-width="2" opacity="0.6"/>
  <line class="pulse" x1="{cx}" y1="62" x2="{cx}" y2="{base + 16}" stroke="{t["accent"]}" stroke-width="3"/>
  <text x="{cx}" y="{base + 40}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="600" fill="{t["accent"]}">0R</text>
  <text x="1140" y="74" text-anchor="end" font-family="{MONO}" font-size="14" fill="{t["sub"]}">{corner}</text>
  <text x="60" y="118" font-family="{FONT}" font-size="58" font-weight="800" fill="{t["fg"]}">{title}</text>
  <text x="62" y="160" font-family="{FONT}" font-size="22" fill="{t["sub"]}">{subtitle}</text>
  <text x="62" y="222" font-family="{FONT}" font-size="20" fill="{t["fg"]}">{status}<tspan class="blink" fill="{t["accent"]}"> ▍</tspan></text>
</svg>
'''


def section(t, num, slug, title, sub):
    W, H = 1200, 120
    grid = "".join(f'<line x1="{x}" y1="18" x2="{x}" y2="{H-18}" stroke="{t["grid"]}" opacity="0.45"/>'
                   for x in range(900, 1180, 40))
    curve = gaussian(900, 1160, 92, 56, 1046, 34, 120)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/>
    </linearGradient>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
  <rect width="8" height="{H}" fill="{t["accent"]}" clip-path="url(#card)"/>
  {grid}
  <line x1="900" y1="92" x2="1160" y2="92" stroke="{t["sub"]}" stroke-width="1.5" opacity="0.6"/>
  <path d="{curve}" fill="none" stroke="{t["fg"]}" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
  <line x1="1030" y1="26" x2="1030" y2="98" stroke="{t["accent"]}" stroke-width="2"/>
  <rect x="36" y="26" width="68" height="68" rx="14" fill="{t["accent"]}" fill-opacity="0.12" stroke="{t["accent"]}" stroke-opacity="0.45"/>
  <g transform="translate(50 40) scale(1.667)" fill="none" stroke="{t["accent"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[slug]}</g>
  <text x="128" y="60" font-family="{FONT}" font-size="34" font-weight="700" fill="{t["fg"]}">{title}</text>
  <text x="129" y="89" font-family="{FONT}" font-size="18" fill="{t["sub"]}"><tspan font-family="{MONO}" fill="{t["accent"]}" font-weight="600">{num:02d}</tspan>  ·  {sub}</text>
</svg>
'''


def splits(t, sessions=(1807, 517, 396)):
    W, H, x0, x1 = 1200, 190, 40, 1160
    parts = [("In sample", "2015 – 2021", "Ideas are built here", t["accent"]),
             ("Validation", "2022 – 2023", "Checked once per idea", t["accent2"]),
             ("Holdout", "2024 – Jul 2025", "Final verdict only", t["muted"])]
    gap = 8
    usable = (x1 - x0) - gap * (len(parts) - 1)
    out, x = [], x0
    for (name, years, role, color), size in zip(parts, sessions):
        w = usable * size / sum(sessions)
        if name == "Holdout":
            out.append(f'<g transform="translate({x + w - 34:.1f} 54)" fill="none" stroke="{t["fg"]}" stroke-width="1.8" stroke-linecap="round">'
                       f'<rect x="0" y="9" width="16" height="12" rx="2"/><path d="M3.5 9V6a4.5 4.5 0 0 1 9 0v3"/></g>')
        out.append(f'<rect x="{x:.1f}" y="40" width="{w:.1f}" height="56" rx="10" fill="{color}" fill-opacity="0.9"/>')
        out.append(f'<text x="{x + 16:.1f}" y="74" font-family="{FONT}" font-size="20" font-weight="700" fill="#ffffff">{name}</text>')
        out.append(f'<text x="{x + 2:.1f}" y="126" font-family="{MONO}" font-size="15" fill="{t["fg"]}" font-weight="600">{years}</text>')
        out.append(f'<text x="{x + 2:.1f}" y="150" font-family="{FONT}" font-size="15" fill="{t["sub"]}">{size:,} sessions</text>')
        out.append(f'<text x="{x + 2:.1f}" y="172" font-family="{FONT}" font-size="15" fill="{t["sub"]}">{role}</text>')
        x += w + gap
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" rx="14" fill="{t["bg1"]}"/>
  <text x="40" y="26" font-family="{FONT}" font-size="14" fill="{t["sub"]}">Time →</text>
  {"".join(out)}
</svg>
'''


def equity(t, rows, title, subtitle, verdict):
    """Cumulative R chart. `rows` is a list of (session 'YYYY-MM-DD', r)."""
    W, H = 1200, 360
    L, R, T, B = 80, 1160, 70, 300
    cum, xs = [0.0], [rows[0][0]]
    for day, r in rows:
        cum.append(cum[-1] + r)
        xs.append(day)
    n = len(cum) - 1
    lo, hi = math.floor(min(cum) / 20) * 20, math.ceil(max(cum) / 20) * 20

    def px(i):
        return L + (R - L) * i / n

    def py(v):
        return B - (B - T) * (v - lo) / (hi - lo)

    line = "M" + " L".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(cum))
    yticks = "".join(
        f'<line x1="{L}" y1="{py(v):.1f}" x2="{R}" y2="{py(v):.1f}" stroke="{t["grid"]}" opacity="0.6"/>'
        f'<text x="{L - 12}" y="{py(v) + 5:.1f}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["sub"]}">{v:+d}R</text>'
        for v in range(lo, hi + 1, 20))
    xticks, seen = [], set()
    for i, day in enumerate(xs[1:], 1):
        year = day[:4]
        if year not in seen:
            seen.add(year)
            xticks.append(f'<line x1="{px(i):.1f}" y1="{B}" x2="{px(i):.1f}" y2="{B + 6}" stroke="{t["sub"]}"/>'
                          f'<text x="{px(i) + 4:.1f}" y="{B + 24}" font-family="{MONO}" font-size="13" fill="{t["sub"]}">{year}</text>')
    end = cum[-1]
    color = t["good"] if end > 0 else t["bad"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" rx="14" fill="{t["bg1"]}"/>
  <text x="{L}" y="36" font-family="{FONT}" font-size="20" font-weight="700" fill="{t["fg"]}">{title}</text>
  <text x="{L}" y="58" font-family="{FONT}" font-size="14" fill="{t["sub"]}">{subtitle}</text>
  {yticks}
  <line x1="{L}" y1="{py(0):.1f}" x2="{R}" y2="{py(0):.1f}" stroke="{t["fg"]}" stroke-width="1.5" opacity="0.7"/>
  {"".join(xticks)}
  <path d="{line}" fill="none" stroke="{t["accent"]}" stroke-width="2.2" stroke-linejoin="round"/>
  <circle cx="{px(n):.1f}" cy="{py(end):.1f}" r="5" fill="{t["accent"]}"/>
  <text x="{R}" y="36" text-anchor="end" font-family="{MONO}" font-size="20" font-weight="700" fill="{color}">{end:+.1f}R</text>
  <text x="{R}" y="58" text-anchor="end" font-family="{FONT}" font-size="14" fill="{t["sub"]}">{verdict}</text>
</svg>
'''
