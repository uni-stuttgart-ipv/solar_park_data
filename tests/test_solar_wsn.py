import datetime as dt
import os

import solar_park_data as spd

from . import INFLUXDB_TOKEN_KEY


def influx_token() -> str:
    token = os.environ.get(INFLUXDB_TOKEN_KEY)
    if token is None:
        raise RuntimeError(
            f"InfluxDB token not found. Set with key {INFLUXDB_TOKEN_KEY}"
        )

    return token


def test_query_recent_data():
    influx = spd.influxdb.client(influx_token())
    client = spd.solar_wsn.Client(influx)

    start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)
    end = dt.datetime.now(dt.timezone.utc)
    client.query(spd.solar_wsn.Query(start=start, end=end))
