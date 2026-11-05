# data-centers

A small, one-time snapshot dashboard on air quality and noise near data centers. Built speculatively, pulled November 5, 2026, not set up to refresh.

Open `docs/index.html` in a browser (it needs internet only to load d3 from a CDN). To host it, turn on GitHub Pages for the `docs/` folder.

## What is in it

- **Air sensors:** Virginia DEQ's Data Center Air Monitoring Project (Kunak AIR sensors, PM2.5, NO2, CO) for 14 locations in Loudoun and Prince William counties, Feb 24 to Nov 1, 2026, summarized to Eastern Standard Time days.
- **Background:** EPA Air Quality System daily summaries for the regulatory monitors: PM2.5 at Broad Run HS (Loudoun), NO2 at Broad Run HS and James S. Long Park (Prince William). EPA has no CO monitor in either county. The sensor at Broad Run HS is collocated with the EPA monitor.
- **Weather:** observed daily rain and wind at Dulles International Airport (station IAD), from the Iowa Environmental Mesonet.
- **Noise:** 18 published measurements compiled from Bray and Dominici (arXiv 2610.03975) and the sources it cites, with each source's verifiability tier.

## Layout

    data/air_daily.json              daily mean and highest-hour PM2.5, NO2, CO per sensor location
    data/air_sites.json              whole-record summary per location (hourly-based means and peaks)
    data/epa_background_daily.json   EPA regulatory monitor daily values
    data/weather_dulles_daily.json   Dulles daily rain and wind
    data/noise.json                  noise measurements table (28 rows)
    data/sites_meta.json             location metadata and the data-quality rules applied
    data/raw/kunak_hourly_agg.json   per-location, per-day [hours, mean, max] straight from the Kunak feed
    data/epa_aqs_raw_extract.json    EPA AQS rows as pulled
    page/page.html                   the dashboard page (HTML, CSS and JS)
    scripts/                         pull and build scripts
    docs/index.html                  standalone page with data inlined (generated)

## Rebuilding

    python3 scripts/make_air_daily.py   # data/raw/kunak_hourly_agg.json -> data/air_daily.json
    python3 scripts/build_page.py       # data/ + page/page.html -> docs/index.html

## Refreshing the data

Not planned. If it is wanted later:

- Kunak: `scripts/pull_kunak.js`, run in the browser console on DEQ's page (kunakcloud.com/websites/VirginiaDEQ.html). New locations must be added to `data/sites_meta.json`. The feed is a public widget, not a documented API, so DEQ's air quality monitoring staff are the right contact for a supported route.
- EPA: `scripts/pull_epa_aqs.js` uses EPA's public test credentials from the AQS API documentation. Register your own email and key for anything ongoing.
- Weather: `scripts/pull_weather.md`.
- `data/air_sites.json` came from the Kunak widget's per-location summaries and is not rebuilt by these scripts.

## Data-quality rules applied

- DEQ's stabilization period (before March 3) and voided first-week PM2.5 (before March 9) are dropped for the five original locations.
- A daily mean needs at least 18 valid hours (DEQ's rule).
- Heritage Farm Museum is cut off after May 28: its PM2.5 went flat near zero before DEQ removed the sensor on June 18.
- Sensors are low-cost and non-regulatory. NO2 sensor agreement with the regulatory monitor is weak, and the sensors read lower than the regulatory monitor during the July 16-18 PM2.5 event.
- EPA values for recent months may not be fully validated.
- Noise levels are not comparable across rows. Positions, weightings and instruments differ and many are not stated. Tier labels per row are partly inferred from source type.
