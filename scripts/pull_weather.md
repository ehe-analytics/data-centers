# Weather pull

Observed daily weather for Dulles International Airport (station IAD) from the Iowa Environmental Mesonet:

    https://mesonet.agron.iastate.edu/cgi-bin/request/daily.py?network=VA_ASOS&stations=IAD&year1=2026&month1=2&day1=24&year2=2026&month2=11&day2=1&format=csv

Columns kept in `data/weather_dulles_daily.json`: `precip_in`, `avg_wind_speed_kts` (as `wind_kts`), `avg_wind_drct` (as `wind_dir`), `max_wind_gust_kts` (as `gust_kts`). Stations HEF (Manassas) and JYO (Leesburg) are also available if a closer station is wanted.
