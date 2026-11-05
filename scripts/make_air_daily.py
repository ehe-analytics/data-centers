"""Turn data/raw/kunak_hourly_agg.json into data/air_daily.json using DEQ's data-quality rules.
Run from the repo root:  python3 scripts/make_air_daily.py
Rules: data before each site's valid_from dropped (DEQ stabilization); PM2.5 before pm_valid_from dropped (voided first week);
sites with a `last` date stop there (Heritage Farm Museum's sensor went flat after May 28); daily mean needs >= 18 hours (DEQ rule).
"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
H = json.loads((root / "data/raw/kunak_hourly_agg.json").read_text())
meta = json.loads((root / "data/sites_meta.json").read_text())["sites"]
rows = []
for s in meta:
    h = H[str(s["loc"])]
    vf = s["valid_from"]; pf = s.get("pm_valid_from") or vf; last = s["last"]
    for d in sorted({k.split("|")[1] for k in h}):
        if d < vf or d > last:
            continue
        def mean(e):
            x = h.get(e + "|" + d)
            return round(x[1], 2) if x and x[0] >= 18 else None
        def mx(e):
            x = h.get(e + "|" + d)
            return round(x[2], 2) if x else None
        r = {"loc": s["loc"], "site": s["tag"], "county": s["county"], "day": d,
             "pm": mean("1266") if d >= pf else None, "pmx": mx("1266") if d >= pf else None,
             "no": mean("1253"), "nox": mx("1253"), "co": mean("1263"), "cox": mx("1263")}
        if all(r[k] is None for k in ("pm", "pmx", "no", "nox", "co", "cox")):
            continue
        rows.append(r)
(root / "data/air_daily.json").write_text(json.dumps(rows, separators=(",", ":")))
print("wrote data/air_daily.json", len(rows), "rows")
