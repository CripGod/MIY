# Maybe It's You — onboarding prototype (handoff)

A two-screen, WebGL-driven onboarding prototype for the Maybe It's You dating app (client: Christine and Dana; studio: PatternBreak). Splash screen with a paper-cutout plate that assembles and drips, then a transition into the payment ("I'd check") screen. One self-contained `index.html`, no external requests, sized to iPhone 17.

Read `CLAUDE.md` first for the working rules. Read `docs/client-copy-and-rules.md` before writing any copy.

---

## Files

    index.html                    built deliverable (self-contained, ~1.6 MB). Generated. Do not hand-edit.
    src/template.html             THE SOURCE. HTML + CSS + raw WebGL/JS with __PLACEHOLDERS__ for assets.
    src/build.py                  template + assets -> index.html   (python3 src/build.py)
    src/assets/                   everything the build inlines (WebP, WOFF2, JSON)
    src/tools/                    scripts that derive assets from the originals (see src/tools/README.md)
    src/history/                  template-v4 (+ built index-v4) = the iteration before this one
    docs/design-language.md       palette, type, surfaces, components, principles
    docs/client-copy-and-rules.md approved copy (verbatim) and the client's hard rules
    docs/iteration-log.md         what changed, why, and current tuning values
    reference/originals/          the client's/AI-generated source art (plate pieces, buttons, lockups)
    reference/mockups/            client references the screens are matched against
    reference/design-language-board.html   the design-language page shown to the client

## Build and run

    python3 src/build.py          # writes ./index.html, fails loudly on any unresolved placeholder
    open index.html               # any modern browser; WebGL1 required

Dev controls under the phone: **Replay** (restarts both timelines) and **Shade** (bottom-gradient strength, sets `--shade` live).
Console hooks: `window.__t0` (ms timestamp when the timeline started; undefined until all textures are loaded) and `window.__go()` (fires the splash -> payment transition).

Verified reproducible: `src/build.py` on the shipped template reproduces the shipped `index.html` byte for byte, and `src/tools/*` regenerate every asset from `reference/originals/` to the same bytes.

---

## Architecture

### Frame
iPhone 17: 402 x 874 pt, 19.5:9, Dynamic Island. `.phone` is `aspect-ratio: 402/874`, radius 56, `overflow:hidden`, cream background (`#f1e6ce`) so the empty stage is paper.

### Layers (z-order inside `.phone`)
1. `canvas.plate` (z1): raw WebGL, the paper plate and the two drips
2. `.content` (z4): splash DOM (shade gradient, quail, MAYBE, IT'S YOU, body copy, Well… button)
3. `.pay` (z5): payment DOM (headline lockup, sub line, 7-item list, price, I'd check button, fine print)
4. status bar (z25), Dynamic Island (z30)

### WebGL engine (template.html, the `<script>` block)
Two programs, WebGL1, premultiplied alpha blending, textures from data URIs.

**PQ, raster pieces.** One shared 30x50 subdivided quad. Each plate piece is drawn as a full-image quad in "cover" fit: `uHalf = ((941/1672)/canvasAspect, 1)`, so x spans `[-1.22, 1.22]` and y `[-1, 1]` in clip space. Uniforms: `uT` (translate), `uRot`, `uScale`, `uAmp/uTime/uPhase` (the continuous soft squiggle, vertex displacement).

**PD, drips.** A polar fan: centre vertex + 180 rim vertices. Attributes per rim vertex: `aAng` (screen angle), `aR` (the well's real silhouette radius at that angle, from `drip.json`). Uniforms: `uR0` (starting circle radius), `uMorph` 0->1, `uLag` (bottom of the shape morphs last = gravity), `uScale`, `uOff`, `uWob` (continuous wobble), `uDripDir/uDripAmt` (extra radius in the drip direction only; this is how the pink stays hidden at the top and drips out below), `uFlat/uUseFlat` (a flat-colour pass = the paper shadow). Position is `center + off + dir(θ)·r` with `dir = (cosθ/aspect, sinθ)`, which is why the start state is a **perfect circle on screen**. UVs are planar from clip position, so fills are sampled by canvas position and the shape reveals them like a mask (textures never stretch when the shape scales).

Draw order per frame: PIECES (back to front) -> rose drip (shadow, then paper) -> cream drip (shadow, then paper) -> in the payment phase, `p3` again on top as the corner rose.

### Choreography (edit these arrays, not the loop)
`PIECES[]`: `k` texture, `from` off-screen start pose `{x,y,r}`, `d` delay, `dur`, `amp` squiggle after landing, `depth` parallax, `ph` phase, `o` exit pose for the transition (`d` stagger, `x,y,r`).
`DRIPS[]`: `k` fill, `a` when the circle pops in, `d`/`dur` morph, `r0` circle radius, `scale`, `off`, `rise` (circle sits high then sinks), `wob`, `lag`, `depth`, `dripDir`, `dripAmt`.
DOM timing lives in CSS custom properties on `:root`: `--tQ --tM --tI --tC --tB --tW` (quail, MAYBE, IT'S YOU, copy, button, words). Payment entrance delays are on the `.pay.on …` rules.

Timeline gating: nothing runs until all textures are loaded (`.content.hold` pauses the CSS animations; `t0` is set at that moment).

### Transition (splash -> payment)
`startTransition()` (bound to the Well… button; also `window.__go()`): sets `phase='pay'`, adds `.leave` to `.content` (CSS exits: type up and out, copy left, button down, shade fades), adds `.pay` to `.phone` (status text goes ink), adds `.on` to `.pay` after 1250 ms (entrance animations). In WebGL: pieces ease to their `o` poses over 1.15 s, the pink drip shrinks to nothing over 0.7 s, the cream drip scales x3.6 over 1.35 s (the flood), then `p3` slides in over the cream from the top-right corner (from tt 0.8, 1.3 s) to pose `x .30 y .44 scale .62` as the corner accent.

### Buttons (`.btn` system)
Both buttons are image assets. Per-button geometry is passed as CSS custom properties on the element: `--cx --cy` (disc centre, % of image), `--d` (arrow mask diameter), `--sd` (shine ring diameter), `--mask` (the button image, used to mask the grain). Layers inside: `.cbg` image, `.fiber` + `.grain` paper texture (multiply, masked), `.mask > img` the arrow clipped to the disc and passing through end to end, `.halo` a pulse ring, `.shine` the rim glint. States: hover (lift, faster arrow/glint), `.down`/`:active` (sinks, tighter shadow). The Well… button's copy is three separate word layers (`.word.w0/w1/w2`) that wipe in: "Well…", a beat, then the rest.

### Other
Pointer parallax (pieces shift by `depth`), `prefers-reduced-motion` (settled state, no motion), Replay (clones `.content` and `.pay`, resets `t0` and `phase`).

---

## Asset pipeline (what each thing is)
| asset | from | how |
|---|---|---|
| `pieces/p2..p8.webp` | 8 plate pieces (AI-generated, client supplied) | resized 840w. Stack order that reproduces the client's reference: 8,7,4,5,6,3,2 then the well |
| `geometry/drip.json` | piece-1 (cream well) alpha | ray-marched silhouette in screen-polar coords around the centroid |
| `fills/cream.webp`, `rose.webp` | piece-1, pieces 3+6 | full-sheet fills for the two drips |
| `buttons/button-well.webp` | button-well-v2.png | baked arrow inpainted out of the disc, wine text lifted out; disc measured by hand (.873,.475,.0675) |
| `words/word0-2.webp`, `geometry/words.json` | same | the three word layers and their positions |
| `buttons/button-idcheck.webp`, `geometry/circle2.json` | button-idcheck.png | disc auto-detected (arrives empty) |
| `type/quail,maybe,itsyou.webp` | type-lockup-splash.png | white knocked out, split by the three clean bands |
| `type/headline-p2.webp` | type-lockup-p2-headline.png | used whole (lines overlap at the "y") |
| `arrow.webp` | arrow.png | the cream arrow that passes through the discs |
| fonts | fontsource | Newsreader (body/page-2), Fraunces (legacy), IBM Plex Mono 500/600 (labels) |

Imagery is placeholder-grade (AI-generated). It clears the client's "no photography" rule because it is pattern and texture, not photos.

---

## Testing
Headless capture is slow because WebGL runs on SwiftShader. What works:

    from playwright.sync_api import sync_playwright
    # launch args: --use-gl=swiftshader --enable-webgl --ignore-gpu-blocklist
    pg.goto(url, wait_until="commit")                         # do NOT wait for "load"
    pg.wait_for_function("window.__t0!==undefined")           # timeline actually started
    t = pg.evaluate("performance.now()-window.__t0")/1000     # page time of each screenshot
    pg.evaluate("window.__go()")                              # fire the transition

Capture at DPR 1 for timing sweeps (each 2x/3x screenshot costs seconds). Read `performance.now()-window.__t0` around every screenshot rather than trusting wall-clock sleeps.

### Repo checks
    scripts/check.sh              # build must reproduce the committed index.html byte for byte, then node --check on the page script
    scripts/check.sh --smoke      # also runs scripts/smoke.py: headless load, wait for __t0, fire __go(), fail on page errors
    python3 scripts/smoke.py --shots out/   # same, plus splash.png and payment.png at DPR 1

`.github/workflows/check.yml` runs both on every push and pull request and uploads the screenshots. In Claude Code on the web, `.claude/hooks/session-start.sh` installs Pillow, numpy and Playwright (matching the container's Chromium) so the asset tools and the smoke test run without setup.

## Known constraints / production notes
- Single file with everything inlined: ~1.6 MB. For production, serve the WebP/WOFF2 as separate files so they cache; the build script is the only thing that changes.
- The rose corner piece is wide and shallow; pushing it deeper down the right edge also pushes it further left across the top (see iteration-log).
- Status time is a mock. Reduced-motion users get the settled screens.

## Where this goes next
Screen 3 (Meet Felix) and the disguised-question flow, on the same engine: new `PIECES` exit/enter poses per screen, a `.meet` DOM block, and a second transition. Copy for those screens is in `docs/client-copy-and-rules.md`.
