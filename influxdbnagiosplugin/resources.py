"""
Nagios Plugin resource(s).
"""
from logging import getLogger

from influxdb import InfluxDBClient
from nagiosplugin import (
    CheckError,
    Metric,
    Resource,
)


COUNT = "count"
MEAN = "mean"
VALUES = "values"


class Measurements(Resource):
    """
    Count and mean metrics for a simple InfluxDB measurement query.
    """
    def __init__(self,
                 hostname,
                 measurement,
                 age,
                 influxdb_hostname,
                 influxdb_port,
                 influxdb_username,
                 influxdb_password,
                 influxdb_database):
        self.hostname = hostname
        self.measurement = measurement
        self.age = age
        self.influxdb_hostname = influxdb_hostname
        self.influxdb_port = influxdb_port
        self.influxdb_username = influxdb_username
        self.influxdb_password = influxdb_password
        self.influxdb_database = influxdb_database
        self.logger = getLogger('nagiosplugin')

    @property
    def query(self):
        """
        Create the InfluxDB query.
        """
        return "SELECT time, value FROM {} WHERE time > now() - {} AND host = '{}'".format(
            self.measurement,
            self.age,
            self.hostname,
        )

    def get_measurements(self):
        """
        Fetch measurements from InfluxDB.
        """
        self.logger.debug("Querying InfluxDB at {}:{} with query: \"{}\"".format(
            self.influxdb_hostname,
            self.influxdb_port,
            self.query,
        ))
        try:
            client = InfluxDBClient(
                self.influxdb_hostname,
                self.influxdb_port,
                self.influxdb_username,
                self.influxdb_password,
                self.influxdb_database,
            )
            results = client.query(self.query)
            self.logger.info("Received result set: {}".format(results))
            return list(results.get_points())
        except Exception as error:
            self.logger.info("Failed to query InfluxDB: {}".format(
                error,
            ))
            raise CheckError(error)

    def probe(self):
        """
        Query InfluxDB; yield the count and mean of the measurements.
        """
        measurements = self.get_measurements()
        values = [measurement["value"] for measurement in measurements]

        count = len(measurements)
        total = float(sum(values))
        mean = 0 if count == 0 else total / count

        yield Metric(COUNT, count, context=COUNT)
        yield Metric(MEAN, mean, context=MEAN)
        # null context; values are not validated individually
        yield Metric(VALUES, values, context="null")
