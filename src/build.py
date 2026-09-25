#!/usr/bin/env python3
"""
Build index.html from src/template.html by inlining every asset as base64.

    python3 src/build.py                      # -> ./index.html
    python3 src/build.py --template src/history/template-v4.html --out src/history/index-v4.html

Never hand-edit index.html. Edit src/template.html (or an asset), then rebuild.
Placeholders in the template (all must resolve; the script fails if any remain):

  Fonts      __NRN__ __NRI__ (Newsreader n/i)  __PLEX__ __PLEX6__ (IBM Plex Mono 500/600)
  Type       __QUAIL__ __MAYBE__ __ITSYOU__ (splash lockup pieces)  __H2__ (page-2 headline lockup)
  Buttons    __BTN__ (Well… button, text+arrow removed)  __BTN2__ (I'd check)  __ARROW__
  Plate      __P2__ __P3__ __P4__ __P5__ __P7__ __P8__ (raster pieces)  __CREAM__ __ROSE__ (drip fills)
  Geometry   __DRIP__ (drip profile JSON)  __CX__ __CY__ __D__ __SD__ (Well… disc)  __CX2__ __CY2__ __D2__ __SD2__ (I'd check disc)
  Words      __WORDS__ (three <img class="word"> layers positioned from words.json)
"""
import argparse, base64, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = ROOT / "src" / "assets"

def b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode()

def disc_vars(c: dict) -> dict:
    """Disc geometry in percent of the button image (cx, cy, r are fractions of width/height)."""
    return {
        "cx": f"{c['cx']*100:.3f}",
        "cy": f"{c['cy']*100:.3f}",
        "d":  f"{c['r']*2*100*0.90:.3f}",   # arrow mask: just inside the gold rim
        "sd": f"{c['r']*2*100*1.16:.3f}",   # shine ring: covers the gold rim
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default=str(ROOT / "src" / "template.html"))
    ap.add_argument("--out", default=str(ROOT / "index.html"))
    a = ap.parse_args()

    s = pathlib.Path(a.template).read_text(encoding="utf-8")
    g = A / "geometry"
    c1 = disc_vars(json.loads((g / "circle.json").read_text()))
    c2 = disc_vars(json.loads((g / "circle2.json").read_text()))
    words = json.loads((g / "words.json").read_text())

    # word layers for the Well… button (positions are fractions of the button image)
    word_html = "\n     ".join(
        f'<img class="word w{i}" style="left:{w["x"]*100:.3f}%;top:{w["y"]*100:.3f}%;width:{w["w"]*100:.3f}%" '
        f'src="data:image/webp;base64,{b64(A/"words"/f"word{i}.webp")}" alt="">'
        for i, w in enumerate(words)
    )
    s = s.replace("__WORDS__", word_html)

    rep = {
        "__CX__": c1["cx"], "__CY__": c1["cy"], "__D__": c1["d"], "__SD__": c1["sd"],
        "__CX2__": c2["cx"], "__CY2__": c2["cy"], "__D2__": c2["d"], "__SD2__": c2["sd"],
        "__DRIP__": (g / "drip.json").read_text().strip(),
        "__NRN__": b64(A/"fonts"/"newsreader-normal.woff2"),
        "__NRI__": b64(A/"fonts"/"newsreader-italic.woff2"),
        "__PLEX__": b64(A/"fonts"/"plex-mono-500.woff2"),
        "__PLEX6__": b64(A/"fonts"/"plex-mono-600.woff2"),
        "__QUAIL__": b64(A/"type"/"quail.webp"),
        "__MAYBE__": b64(A/"type"/"maybe.webp"),
        "__ITSYOU__": b64(A/"type"/"itsyou.webp"),
        "__H2__": b64(A/"type"/"headline-p2.webp"),
        "__ARROW__": b64(A/"arrow.webp"),
        "__CREAM__": b64(A/"fills"/"cream.webp"),
        "__ROSE__": b64(A/"fills"/"rose.webp"),
        "__BTN2__": b64(A/"buttons"/"button-idcheck.webp"),
        "__BTN__": b64(A/"buttons"/"button-well.webp"),
    }
    for i in (2, 3, 4, 5, 7, 8):
        rep[f"__P{i}__"] = b64(A/"pieces"/f"p{i}.webp")

    # longest keys first so __CX2__ never collides with __CX__ etc.
    for k in sorted(rep, key=len, reverse=True):
        s = s.replace(k, rep[k])

    left = sorted(set(re.findall(r"__[A-Z0-9]+__", s)))
    if left:
        sys.exit(f"unresolved placeholders: {left}")

    out = pathlib.Path(a.out)
    out.write_text(s, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size/1024/1024:.2f} MB)")

if __name__ == "__main__":
    main()
