"""Draw the book's README artwork. Run from the repo root:
python assets/make_assets.py
"""

from pathlib import Path

from nqlab import art

OUT = Path(__file__).resolve().parent

SECTIONS = [
    ("record", "The research record", "Every idea tested, kept whether it worked or not"),
    ("process", "How an idea gets tested", "Written down first, tested second"),
    ("splits", "Three periods, fixed in advance", "Build, check once, final verdict"),
    ("data", "The shared library", "One loader, one set of cleaning rules"),
    ("book", "Starting a new hypothesis", "One idea, one repo"),
    ("rules", "House rules", "What keeps the results honest"),
]


def main():
    for name, t in art.THEMES.items():
        status = (f'Ideas tested: <tspan font-weight="700">1</tspan>'
                  f'<tspan dx="14" fill="{t["sub"]}">·</tspan><tspan dx="14">Edges found: </tspan>'
                  f'<tspan fill="{t["accent"]}" font-weight="700">0 so far</tspan>')
        art.write(OUT, "banner", name, art.banner(
            t, "nq-research", "The NQ Lab book: every hypothesis, in one place", status,
            "H-001 · −0.014R · rejected"))
        art.write(OUT, "splits", name, art.splits(t))
        for num, (slug, title, sub) in enumerate(SECTIONS, 1):
            art.write(OUT, f"section-{slug}", name, art.section(t, num, slug, title, sub))
    print("ok")


if __name__ == "__main__":
    main()
