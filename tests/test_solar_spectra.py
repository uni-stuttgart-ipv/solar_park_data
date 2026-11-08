import datetime as dt
import os

import solar_park_data as spd

from . import AWS_TOKEN_KEY, INFLUXDB_TOKEN_KEY


def influx_token() -> str:
    token = os.environ.get(INFLUXDB_TOKEN_KEY)
    if token is None:
        raise RuntimeError(
            f"InfluxDB token not found. Set with key {INFLUXDB_TOKEN_KEY}"
        )

    return token


def aws_token() -> str:
    token = os.environ.get(AWS_TOKEN_KEY)
    if token is None:
        raise RuntimeError(f"AWS token not found. Set with key {AWS_TOKEN_KEY}")

    return token


def test_list_range():
    influx = spd.influxdb.client(influx_token())
    client = spd.solar_spectra.Client(influx)

    start = dt.datetime.now() - dt.timedelta(days=1)
    end = dt.datetime.now()
    client.list_range(start=start, end=end)
