from __future__ import annotations

import datetime as dt
import os
import pathlib
from dataclasses import dataclass

import pyarrow as pa
from influxdb_client_3 import InfluxDBClient3

from .meta import needs_s3, needs_influx

S3_BUCKET = "solar-park-spectra"


@dataclass
class Query:
    start: dt.datetime | str | None = None
    end: dt.datetime | str | None = None
    spectrometer: str | None = None

    def to_sql_where(self) -> str | None:
        if self.start is None and self.end is None and self.spectrometer is None:
            return None

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
        if self.spectrometer is not None:
            clauses.append(f"spectrometer = '{self.spectrometer}'")

        return " AND ".join(clauses)


class Client:
    def __init__(
        self, influx_client: InfluxDBClient3 | None = None, s3_client=None
    ) -> None:
        self.influx_client = influx_client
        self.s3_client = s3_client

    @needs_influx
    def query(self, query: Query) -> pa.Table:
        q = f"SELECT * FROM solar_spectra WHERE {query.to_sql_where()}"
        return self.influx_client.query(q)

    @needs_s3
    def download_table(
        self,
        table: pa.Table,
        outdir: os.PathLike | str = ".",
        fmt: str = "%Y-%m-%dT%H-%M-%S",
    ):
        """Download files decribed in the table.

        Args:
            table (pa.Table): Table with columns `time`, `spectrometer`, `s3_bucket`, and `s3_object_key`.
            outdir (os.PathLike | str, optional): Output directory. Defaults to ".".
            fmt (str, optional): Format string for time in filename. Defaults to "%Y-%m-%dT%H-%M-%S".
        """
        outdir = pathlib.Path(outdir)
        for record in table.to_pylist():
            time = record["time"].strftime(fmt)
            filename = f"{record['spectrometer']}-{time}.csv"
            path = outdir.joinpath(filename)
            self.s3_client.download_file(
                record["s3_bucket"], record["s3_object_key"], path
            )
