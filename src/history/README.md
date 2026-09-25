# History

`template-v4.html` / `index-v4.html` is the iteration immediately before the current one. Differences from the current template:
- IT'S YOU entered faster from further out (`translateX(200%)`, 0.9 s); the client asked for the original arc back (160%, 1.15 s).
- Bottom shade was a fixed strength (~.74); the client found it too dark, so it is now `--shade` with a slider (default .55).
- The page-2 corner rose was small and tucked (`scale .53`, offset .46); the client outlined a larger region, now `scale .62`, `x .30 y .44`.

Build it the same way: `python3 src/build.py --template src/history/template-v4.html --out src/history/index-v4.html`
