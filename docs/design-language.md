# Maybe It's You - UI Kit Specification
### A brief for UI Kit Maker

Build an elegant, complete UI component kit for a mobile app called **Maybe It's You**. Everything below is the target. Follow it closely, and when in doubt, choose the more editorial, more confident, more restrained option.

---

## 1. What this is

Maybe It's You is a dating app that refuses to look like a dating app. A sharp, funny, perceptive concierge named **Felix** guides the user. The interface should feel editorial and graphic, warm and light, sophisticated and a little irreverent. All of the personality comes from color, pattern, texture, and type. A full screen should hold attention with zero photography.

Reference feeling: the visual DNA of a beautifully designed old supper club or a hand-painted marquee, reinterpreted as a modern digital system. Extract the color, pattern, texture, typography, and wit. Never depict the actual room.

---

## 2. Hard rules

1. **No photography.** No photos of people, faces, rooms, furniture, lamps, food, or lifestyle imagery. None, anywhere.
2. **Light ground, never black.** Warm cream paper is the canvas. Forest green and wine are fields and accents, not the base. Avoid black-on-black moodiness.
3. **Texture on everything.** Flat color reads cheap. Add grain, depth, layering, and finish.
4. **Maximal detail, generous negative space.** It should feel expensive because it is not crowded.
5. **Surprise without randomness.** Rotate a defined set of surfaces and color-ways so each section feels like a new room. A system, not chaos.
6. **Behaves like Felix.** Evidence before cleverness (flourishes are earned). Intermittent reinforcement (not every screen shouts). Ouch, then laugh, then oh shit (payoffs escalate). The interface keeps rewarding curiosity.

---

## 3. Color tokens

| Token | Hex | Use |
|---|---|---|
| `paper` | #F1E6CE | Primary ground (the canvas) |
| `paper-deep` | #E6D6B6 | Secondary ground, card fills |
| `forest` | #1E4A37 | Field color, primary chips, text on paper |
| `forest-deep` | #123021 | Reveal grounds, deepest shade |
| `forest-light` | #2C5F47 | Stripe tone, hover |
| `rose` | #E2A89A | Chapter field, warm bubbles, secondary chips |
| `rose-deep` | #CD8A7C | Rose shading, veining |
| `rose-light` | #EEC3B9 | Rose highlights |
| `wine` | #7C2836 | Primary action color, headlines on light |
| `wine-deep` | #5C1C28 | Pressed states, borders |
| `wine-light` | #95323F | Hover on wine |
| `gold` | #BF9739 | Reward, accents, outlines, icons |
| `gold-light` | #E6C880 | Foil highlight, arrows on wine |
| `gold-deep` | #8F6F26 | Foil shadow |
| `ink` | #2A231D | Body text on light |
| `ink-soft` | #71634F | Secondary text, captions |

Rules of thumb: **wine = the action color. gold = the reward.** Forest and rose are the fields that change per chapter. Text is ink or forest on paper, and paper on dark fields.

---

## 4. Typography

Three roles. Big contrast between display and body is essential.

- **Display / marquee.** A bold, high-contrast serif with old-signage confidence and individuality. Set very large, tight tracking, usually stacked on two lines. One big line per screen, treated like a headline on a marquee. Suggested: Fraunces 700-900, or a strong Didone display (Playfair Display, Abril Fatface). Do not use a font that literally says "vintage."
- **Editorial serif / Felix voice.** A warm, readable serif at book weight, with italics for emphasis and for Felix's warm asides. Body copy, questions, and Felix speech. Suggested: Fraunces 400-500, or an old-style text serif.
- **Mono label.** Uppercase monospace, wide letterspacing, small. Eyebrows, system labels, progress counts, chip text. Suggested: IBM Plex Mono 500.

Scale guide: display 40-72, section headline 28-40, body 15-18, label 9-11.

---

## 5. Shape, spacing, finish

- **Radii.** Pills fully rounded (999). Cards 12-16. Arch panels use a large top radius (a doorway shape) with a small bottom radius. (Note: this project is intentionally soft and arched, not square.)
- **Spacing.** Base unit 4. Screen side margins 22-28.
- **Elevation.** Soft, warm, low-and-wide shadows built from deep brown alpha, never hard black.
- **Grain.** A fine fractal-noise overlay at roughly 5-9 percent, multiply, on paper and on colored fields, to read as aged paper and finished surfaces.

---

## 6. Surface and pattern library

Each surface is procedural (CSS or SVG). No image files.

- **Awning stripe.** Vertical two-tone stripes (forest and cream, or tonal forest). Left-edge spines, headers, dividers.
- **Rose marble.** A soft veined rose field: gradient clouds plus faint gold veins.
- **Gold crackle (kintsugi).** Thin gold veins branching over a dark field. Reserved for reveal and reward screens.
- **Gold leaf / foil.** Metallic gradient, dark gold to light gold to mid. Celebratory buttons and accents.
- **Aged paper.** Cream plus grain. The default ground.
- **Ornament.** A small symmetrical gold flourish (diamond, rule, dots). Dividers, footers, framing.
- **Arch / doorway panel.** A tall rounded-top container. Hero framing.

---

## 7. The component kit

Build every component below. Show each in all variants and states.

### Buttons
- **Primary.** Full-width wine pill, cream italic-serif label, small gold arrow. The label carries voice, never generic. States: default, hover (wine-light, slight lift), pressed, disabled (muted).
- **Secondary.** Gold-outline pill, transparent fill, forest or ink label.
- **Tertiary / ghost.** Hairline outline, quiet sans label.
- **Icon button.** Circular wine button with a gold arrow, for advance / next.
- **Text link.** Wine, underline on hover.

### Inputs and forms
- **Text field.** Cream inset with grain, thin ink border, serif input, mono label above, wine focus ring. States: default, focus, filled, error (wine), disabled.
- **Text area.** Same, taller (for Felix chat replies and free text).
- **Select / dropdown.** Same field style, gold chevron.

### Selection
- **Option card (radio).** Cream rounded card, thin wine circle on the left, serif label. States: default, hover (subtle rose tint), selected (filled wine radio, wine border), disabled. This is the question answer component.
- **Checkbox.** Wine check.
- **Toggle / switch.** Pill track, cream knob, wine when on.

### Chips, tags, pills
- **Autopilot chip.** Solid forest pill (primary) and solid rose pill (secondary), uppercase mono.
- **Badge chip.** Gold-outline pill, collectible feel (for named badges like "The Slow Fade").
- **Status tag.** Small mono pill.

### Progress and steppers
- **Progress bar.** Slim track, wine fill, mono "X / N". Never label it "Question N".
- **Dot stepper.** Small dots, gold active.
- **Countdown ring.** Thin gold ring depleting, for timed questions.

### Cards and containers
- **Content card.** Cream, grain, soft shadow, 12-16 radius.
- **Value row.** Gold line icon in a gold-ring circle, serif title, small serif subtext (the payment list rows).
- **Badge card.** Icon medallion, name, and a wry one-line description.
- **Arch panel.** Doorway container for hero moments.
- **Reveal panel.** Dark field (forest or wine) with gold crackle, for the Autopilot reading.

### Felix and conversation
- **Speech bubble.** Cream bubble, tail lower-left, serif text. **Warm variant:** rose bubble, wine italic text, for Felix's emphatic lines.
- **Coaching card.** Bordered card, mono label ("Felix, just to you"), italic-serif message. For the voice call.
- **Typing indicator.** Three dots.

### Media and reveal
- **Locked media card.** Portrait card, gold lock icon, mono caption ("unlocks after one call"). Purely graphic, no image behind it.
- **Reveal frame.** A paper or marble framed placeholder where a real image will later live. Never a stock photo.

### Navigation and chrome
- **Top bar.** Minimal, small gold monogram centered, optional back control.
- **Status bar mock.** 9:41 plus glyphs, for full-screen mockups.
- **Bottom sheet / overlay.** Cream sheet rising over a dimmed field, arch or rounded top.
- **Modal / dialog.** Centered card.

### Feedback
- **Toast / snackbar.** Small wine or gold card.
- **Inline note / warning.** Mono, with wine emphasis (used for the accountability rule).
- **Empty state.** An ornament plus a single Felix line. Never a generic illustration.

### Voice and audio
- **Waveform.** Animated gold-to-wine bars.
- **Call header.** Name, "voice only, no numbers exchanged", and a timer.

### Motifs and decoration
- **Quail.** A small, elegant line-drawn bird, used at most once per screen as a wink. Never a mascot on every element.
- **Ornamental divider.** A gold flourish rule.
- **Footer signature.** "Curiosity in. [quail] People out." with the wordmark.

### Iconography
- Style: fine gold line icons, stroke 1.4-1.6, rounded joins, often inside a gold-ring circle on dark or set in ink on paper. Subjects: autopilot / compass, badge / star, target, camera, eye, signal, lock, clock, calendar, pin. Keep them elegant and consistent, never literal or cute.

---

## 8. Interactive states

Apply to every interactive component: default, hover, pressed, focus (wine ring), selected, disabled (desaturate and lower opacity), loading.

---

## 9. Motion

- **Screen to screen.** Graphic transitions, not fades: a stripe sweeps, an arch opens, a panel flips, a pattern morphs. Motion is an event.
- **Micro-rewards.** Reveals (Felix lines, badges, the Autopilot) animate in with a small flourish. The payoff screens get the biggest one.
- **Rhythm.** Calm screens, then a loud one. Intermittent, not constant.

---

## 10. Do and don't

**Do:** warm light grounds, saturated fields, texture on every surface, strong type contrast, a voice in every label, one motif wink per screen, real negative space.

**Don't:** photographs, black or near-black base, generic UX labels ("Continue", "Next", "Get Started"), flat untextured color, the quail on every element, anything that reads as therapy, wellness, or clinical.

---

## 11. How to deliver

- Output an organized component sheet on a cream `paper` ground with grain.
- One section per group above, each component shown in all variants and states, labeled with its token names.
- Put the color and type token reference at the top of the sheet.
- Build it graphic and procedural, with zero photography.
- Use portrait phone frames (9 by 19.5) for any full-screen examples.
