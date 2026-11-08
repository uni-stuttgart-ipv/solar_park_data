# %%
import datetime as dt
import os

import solar_park_data as spd

# %%
influx_token = os.environ.get("INFLUXDB_TOKEN")
if influx_token is None:
    raise RuntimeError("influxdb token not set")

influx = spd.influxdb.client(influx_token)
wsn = spd.solar_wsn.Client(influx_client=influx)

# %%
now = dt.datetime.now(dt.timezone.utc)
start = now - dt.timedelta(days=7)
recent = wsn.query(spd.solar_wsn.Query(start, now))
# %%
recent_df = recent.to_pandas()
print(recent_df.columns.tolist())
# %%
csv_path = wsn.download_as_csv(recent)
# %%
