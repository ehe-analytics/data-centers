"""Build docs/index.html (standalone page, data inlined) from data/ and page/page.html.
Run from the repo root:  python3 scripts/build_page.py
"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = root / "data"
page = (root / "page" / "page.html").read_text()
data = {
    "air_daily": json.loads((d / "air_daily.json").read_text()),
    "air_sites": json.loads((d / "air_sites.json").read_text()),
    "noise": json.loads((d / "noise.json").read_text()),
    "background": json.loads((d / "epa_background_daily.json").read_text()),
    "weather": json.loads((d / "weather_dulles_daily.json").read_text()),
}
head = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Data Center Air and Noise</title>
<style>
:root{--color-fg:#1d2330;--color-fg-muted:#5b6475;--color-bg:#f6f7f9;--color-panel:#fff;--color-border-line:#dde1e8;
--cds-gap-sm:.5rem;--cds-gap-lg:1.5rem;--cds-pad-xs:.25rem;--cds-pad-sm:.5rem;--cds-pad-lg:1.25rem;--cds-radius:6px;
--cds-font-size-caption:.8rem;--cds-font-size-heading:1.05rem;--cds-font-size-title:1.9rem;--cds-font-weight-medium:600;
--cds-surface-popover:#fff;--cds-border:#c9ced8;--cds-shadow-popover:0 2px 8px rgba(0,0,0,.15);
--cds-chart-grid:#e6e9ee;--cds-chart-axis:#9aa3b2;--cds-chart-muted:#8a93a6;--cds-chart-reference:#b0482f;
--font-anthropic-sans:system-ui,-apple-system,"Segoe UI",sans-serif;--font-anthropic-serif:Georgia,"Times New Roman",serif;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--color-fg:#e6e9ef;--color-fg-muted:#9aa3b2;--color-bg:#14171d;--color-panel:#1c2028;--color-border-line:#2c323d;--cds-surface-popover:#242933;--cds-border:#3a4150;--cds-chart-grid:#272c36;--cds-chart-axis:#5a6372;--cds-chart-muted:#7a8397;--cds-chart-reference:#e08a6f;color-scheme:dark}}
body{margin:0;background:var(--color-bg);color:var(--color-fg);font-family:var(--font-anthropic-sans)}
#dash-root{padding:max(16px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) 3rem max(16px,env(safe-area-inset-left))}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
</head><body>
<div id="dash-root">
"""
shim = """<script>
window.__DATA=%s;
(function(){
const draws=new Map();
const dark=matchMedia('(prefers-color-scheme: dark)').matches;
window.dash={colors:dark?['#6cb4ff','#f2a65a','#5fd0b0','#d58cf0','#f06a6a','#c8c66a','#8aa0ff','#b0b6c4']:['#1f6feb','#d9822b','#17a37f','#a14cc7','#d64545','#8c8a1e','#4a5fd6','#6b7280'],
 data:id=>({status:window.__DATA[id]?'ok':'missing',data:window.__DATA[id]||[]}),
 draw(name,fn){ if(fn){draws.set(name,fn);} const f=draws.get(name); if(f)document.querySelectorAll('[data-draw="'+name+'"]').forEach(el=>f(el)); },
 params:()=>({}),setParams(){},setLink(){},refresh(){}};
const all=()=>[...draws.keys()].forEach(n=>dash.draw(n));
addEventListener('DOMContentLoaded',all);let t;addEventListener('resize',()=>{clearTimeout(t);t=setTimeout(all,120)});
})();
</script>
""" % json.dumps(data, separators=(",", ":"))
body = page.replace('<meta name="dash-one-writer">', "")
marker = "<script>\n(function(){\nconst root"
i = body.index(marker)
html = head + body[:i] + shim + body[i:] + "\n</div>\n</body></html>\n"
(root / "docs").mkdir(exist_ok=True)
(root / "docs" / "index.html").write_text(html)
print("wrote docs/index.html", len(html), "bytes")
