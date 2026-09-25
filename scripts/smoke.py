#!/usr/bin/env python3
"""Headless smoke test for index.html (README "Testing").

Loads the built page with software WebGL, waits for the timeline to start
(window.__t0), fires the splash -> payment transition (window.__go()) and
fails on any page error. Optionally writes screenshots.

    python3 scripts/smoke.py                 # pass/fail only
    python3 scripts/smoke.py --shots out/    # also capture splash + payment at DPR 1

Requires the Python `playwright` package and a Chromium it can find
(`pip install playwright` then `playwright install chromium`, or the browser
already present in the Claude Code web container).
"""
import argparse, pathlib, sys, time
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARGS = ["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", default=str(ROOT / "index.html"))
    ap.add_argument("--shots", help="directory to write splash.png and payment.png into")
    ap.add_argument("--timeout", type=float, default=240, help="seconds to wait for the timeline to start")
    a = ap.parse_args()

    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=ARGS)
        page = browser.new_page(viewport={"width": 480, "height": 960}, device_scale_factor=1)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)

        t = time.time()
        page.goto(pathlib.Path(a.page).resolve().as_uri(), wait_until="commit")   # do not wait for "load"
        page.wait_for_function("window.__t0!==undefined", timeout=a.timeout * 1000)
        print(f"timeline started ({time.time() - t:.1f}s wall)")

        def page_time():
            return page.evaluate("performance.now()-window.__t0") / 1000

        page.wait_for_timeout(1500)
        if a.shots:
            d = pathlib.Path(a.shots); d.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(d / "splash.png")); print(f"splash.png at page time {page_time():.2f}s")
        page.evaluate("window.__go()")
        page.wait_for_timeout(4500)
        assert page.evaluate("document.getElementById('pay').classList.contains('on')"), "payment screen never switched on"
        if a.shots:
            page.screenshot(path=str(d / "payment.png")); print(f"payment.png at page time {page_time():.2f}s")
        browser.close()

    if errors:
        print("FAIL: page errors"); print("\n".join(errors)); sys.exit(1)
    print("OK: no page errors, transition fired")

if __name__ == "__main__":
    main()
