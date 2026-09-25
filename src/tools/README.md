# Asset prep tools

Each script reads `reference/originals/…` and writes into `src/assets/…`. Run from the package root.
They are only needed if an original changes; the shipped assets are already in place.

    python3 src/tools/pieces.py         # plate pieces -> pieces/p1..p8.webp
    python3 src/tools/drip_profile.py   # well silhouette -> geometry/drip.json
    python3 src/tools/fills.py          # cream.webp / rose.webp drip fills
    python3 src/tools/button_prep.py    # both buttons, disc geometry, word layers
    python3 src/tools/type_prep.py      # splash lockup pieces, page-2 headline
    python3 src/build.py                # then rebuild index.html

Requires Pillow and numpy (`pip install pillow numpy`).
Fonts came from npm: @fontsource-variable/newsreader, @fontsource-variable/fraunces, @fontsource/ibm-plex-mono.
