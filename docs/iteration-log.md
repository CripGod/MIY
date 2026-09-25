# Iteration log

How this build got here, the decisions that were made, and the numbers that currently tune it. Newest at the bottom.

## Path to the current engine
1. **Flat plate** (an AI-generated texture collage) used as a background image, copy in the cream well. Proved the direction but was a fixed raster.
2. **Plate rebuilt from the client's eight pieces** (Archive_34) by compositing them. Stack order that reproduces the client's reference: forest(8), bottom stripes(7), gold seigaiha(4), black crackle(5), left rose(6), top rose(3), top-left stripes(2), then the cream well(1) on top. This made the plate a recipe instead of a picture.
3. **First animated version**: CSS entrance, stop-motion steps, no fades. Client then asked for smooth 60 fps and no stepping.
4. **WebGL engine**: pieces as textured quads with a continuous squiggle; the cream well became a procedural drip that morphs from a perfect circle (with gravity lag on the tail); the pink under it became its own drip emerging from beneath. Paper shadows under both. Client copy on the button lifted into word layers.
5. **Page 2 and the transition**: cream drip floods the screen, pieces exit, the top-right rose returns over the cream as the corner accent, payment content builds in.

## Decisions worth knowing
- **Why drips are polar fans, not raster**: the client asked for the well to morph from a perfect circle into a drip. A polar radius profile interpolates cleanly from a constant (circle) to the well's real silhouette; screen-polar coordinates keep the circle circular on a 19.5:9 canvas.
- **Why the pink extends only in the drip direction** (`uDripDir/uDripAmt`): a uniformly larger pink showed a pink rim at the top-left, which the client rejected. Directional extra keeps the pink hidden above and drips it out below and to the left.
- **Why both drips share the same wobble**: different amplitudes produced pink slivers flashing at the top edge.
- **Why the corner rose is drawn a second time on top** in the payment phase: the cream drip draws over all pieces during the flood, so the rose has to come back above it.
- **Why the Well… disc was measured by hand**: automatic detection kept catching the wine text and the gold rim. `circle.json` is the hand measurement.
- **Why the page-2 headline lockup is used whole**: the two lines overlap at the "y" descender; any horizontal split nicks glyphs.
- **Why the rose corner is where it is**: the piece is wide and shallow, so a uniform scale trades reach across the top against depth down the right. Scale .62 with the piece bleeding off the top and right is the balance the client accepted.

## Current tuning (template.html)
Splash timeline (CSS `:root`): `--tQ 2.45s` quail, `--tM 2.6s` MAYBE fade, `--tI 3.55s` IT'S YOU (1.15 s arc from `translateX(160%) rotate(6deg)`), `--tC 3.95s` copy, `--tB 4.3s` button, `--tW 5.05s` "Well…" then `+0.9s` "that's annoying."
Plate (JS `PIECES`): delays 0 / .14 / .26 / .38 / .55 / .66 s, durations ~1 s, squiggle amp .004–.013 on gold, top rose, top-left stripes.
Drips (`DRIPS`): circle pops at .62 s; pink morph .82 s for 1.15 s; cream morph 1.02 s for 1.25 s; `r0 .34`, `rise .22`, `lag .55`, `wob .007`; pink `scale .985`, `dripDir (-.41,-.91)`, `dripAmt .125`.
Shade: `--shade .55` (slider 0–100).
Buttons: arrow pass 1.05 s (0.55 s on hover), glint 1.7 s (1.2 s on hover), halo pulse 2.4 s, grain .34 + fiber .16 multiply.
Transition: exits 1.15 s, cream flood x3.6 over 1.35 s, pink collapse .7 s, rose corner from tt .8 s over 1.3 s to `x .30 y .44 scale .62`, `.pay.on` at 1250 ms.
Payment entrance: headline 1.4 s @ .1 s, sub 1.2 s @ .65 s, items 1.15 s from .6 s every .18 s, price @ 2.6 s, button @ 3.1 s, fine print @ 3.85 s.
Page-2 type: lockup 82% width; sub 22 px Newsreader 400; list titles 14.4 px 700; descriptions 12.2 px; $89 at 50 px; tagline Plex Mono 600 12 px; fine print 9.5 px.

## Open items
- Names/prices to confirm with the client: "Maybe It's You" vs "It's Something"; $89 vs $65.
- The corner rose's reach vs depth trade-off (see above) if the client wants it deeper.
- Imagery is placeholder-grade. Real pattern/texture plates (not photos) would replace `reference/originals` and flow through `src/tools`.
- Next screens: Meet Felix, the disguised-question flow, Felix interruptions (copy in `docs/client-copy-and-rules.md`).
- Production: split assets out of the single file for caching.
