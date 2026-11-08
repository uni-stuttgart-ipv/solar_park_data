from influxdb_client_3 import InfluxDBClient3

ORG = "Institute of Photovoltaics"
HOST = "https://eu-central-1-1.aws.cloud2.influxdata.com"
DB_PROD = "solar_park_data"


def client(token: str, db: str = DB_PROD) -> InfluxDBClient3:
    """Create a new influx client.

    Args:
        token (str): API token.
        db (str, optional): Database key. Defaults to solar_park_data.

    Returns:
        InfluxDBClient3: Influx client.
    """
    return InfluxDBClient3(host=HOST, token=token, database=db, org=ORG)
