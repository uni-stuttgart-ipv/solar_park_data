from __future__ import annotations

import datetime as dt
import os
import pathlib
from dataclasses import dataclass

import pyarrow as pa
import pyarrow.csv as pacsv
from influxdb_client_3 import InfluxDBClient3

from .meta import needs_influx

MEASUREMENT = "panel_parameters"


@dataclass
class Query:
    start: dt.datetime | str | None = None
    end: dt.datetime | str | None = None
    freq: str = "10m"

    def to_influxql(self) -> str:
        clauses = []
        start = self.start
        end = self.end
        if isinstance(start, dt.datetime):
            start = start.isoformat()
        if isinstance(end, dt.datetime):
            end = end.isoformat()
 
        if start is not None:
            clauses.append(f"time >= '{start}'")
        if end is not None:
            clauses.append(f"time <= '{end}'")

        query = f"SELECT mean(*) FROM {MEASUREMENT}"
        if clauses:
            query += f" WHERE {' AND '.join(clauses)}"

        return f"{query} GROUP BY time({self.freq}), * fill(none)"


class Client:
    def __init__(self, influx_client: InfluxDBClient3 | None = None) -> None:
        self.influx_client = influx_client

    @needs_influx
    def query(self, query: Query) -> pa.Table:
        q = query.to_influxql()
        return self.influx_client.query(q, language="influxql")

    def download_as_csv(
        self,
        table: pa.Table,
        outdir: os.PathLike | str = ".",
        fmt: str = "%Y-%m-%dT%H-%M-%S",
    ) -> pathlib.Path:
        outdir = pathlib.Path(outdir)
        timestamps = table["time"].to_pylist()
        if timestamps:
            start, end = min(timestamps), max(timestamps)
        else:
            start = end = dt.datetime.now(dt.timezone.utc)

        filename = f"wsn_data_{start.strftime(fmt)}-{end.strftime(fmt)}.csv"
        path = outdir.joinpath(filename)
        pacsv.write_csv(table, path)
        return path