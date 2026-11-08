# %%
import datetime as dt
import os

import solar_park_data as spd

# %%
influx_token = os.environ.get("INFLUXDB_TOKEN")
if influx_token is None:
    raise RuntimeError("influxdb token not set")
s3_access_key = os.environ.get("S3_ACCESS_KEY")
if s3_access_key is None:
    raise RuntimeError("s3 access key not set")
s3_secret_key = os.environ.get("S3_SECRET_KEY")
if s3_secret_key is None:
    raise RuntimeError("s3 secret key not set")

influx = spd.influxdb.client(influx_token)
s3 = spd.aws.s3_client(s3_access_key, s3_secret_key)
spectra = spd.solar_spectra.Client(influx_client=influx, s3_client=s3)

# %%
now = dt.datetime.now()
start = now - dt.timedelta(days=1)
recent = spectra.query(spd.solar_spectra.Query(start, now))
# %%
spectra.download_table(recent)
# %%
