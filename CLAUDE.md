# CLAUDE.md — working rules for this repo

Project: Maybe It's You onboarding prototype (PatternBreak for Christine and Dana). Read README.md for architecture.

## Source of truth
- Edit `src/template.html` and `src/assets/*`. Never edit `index.html` by hand; it is generated.
- After any change: `python3 src/build.py`. It fails on unresolved placeholders. Commit the rebuilt `index.html` with the template.
- Full-file replacements over patches when handing work back.

## Hard constraints
- Raw WebGL1 + vanilla JS/CSS. No frameworks, no libraries, no CDN, no external requests. The deliverable stays a single self-contained HTML.
- Frame is iPhone 17: 402 x 874, Dynamic Island. Content must fit the frame with no scrolling.
- No photography anywhere (client rule). Pattern, texture, colour and type only. The existing imagery is procedural/pattern art and is allowed.
- Client-approved copy is verbatim. Do not rewrite, "improve", or re-punctuate it. It contains its own em dash ("saying—and"); keep it. See `docs/client-copy-and-rules.md`.
- Do not use em dashes in any copy or UI text YOU write (studio rule). Use commas, periods, or colons.
- Do not add generic UX labels ("Continue", "Next", "Get Started"). Buttons carry the voice.
- Questions in the flow are never numbered or labelled as a quiz/assessment.

## Motion rules the client has signed off on
- Smooth 60 fps easing. No stop-motion stepping.
- The plate pieces slide in from off-screen; they do not fade. MAYBE and the quail fade (requested). IT'S YOU keeps its original arc: `translateX(160%) rotate(6deg)`, 1.15 s, `var(--ease)`. Do not speed it up or change its path.
- The cream well is a perfect circle that morphs into the drip; the pink drip emerges from under it in the drip direction only, never at the top-left.
- The Well… button copy plays "Well…", a beat, then "that's annoying." as one phrase.
- The disc arrow is masked inside the circle and passes through end to end. The rim glint and pulse halo stay on every burgundy disc.
- Bottom shade is user-tunable (`--shade`, slider). Default 0.55.

## Design tokens (see docs/design-language.md)
paper #F1E6CE, forest #1E4A37, dusty rose #E2A89A, wine #7C2836 (action), gold #BF9739 / #E6C880 (reward), ink #2A231D.
Type: Newsreader for body and page-2 copy, IBM Plex Mono for labels, the client's lockups as images for display type.

## Testing
See README "Testing". Use `window.__t0` for page time, `window.__go()` for the transition, DPR 1 for sweeps. Validate JS with `node --check` on the extracted script before shipping.

## Style of communication with the studio
Terse and decisive. Root-cause fixes without touching unrelated code. Say what changed and why in a few lines.
