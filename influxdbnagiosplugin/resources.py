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
                 extra_where_clauses,
                 influxdb_hostname,
                 influxdb_port,
                 influxdb_username,
                 influxdb_password,
                 influxdb_database):
        self.hostname = hostname
        self.measurement = measurement
        self.age = age
        self.extra_where_clauses = extra_where_clauses or []
        self.influxdb_hostname = influxdb_hostname
        self.influxdb_port = influxdb_port
        self.influxdb_username = influxdb_username
        self.influxdb_password = influxdb_password
        self.influxdb_database = influxdb_database
        self.logger = getLogger('nagiosplugin')

    @property
    def fields(self):
        """
        Generate the InfluxDB query fields.
        """
        return ["time", "value"]

    @property
    def clauses(self):
        return [
            "time > now() - {}".format(self.age),
            "host = '{}'".format(self.hostname)
        ] + self.extra_where_clauses

    @property
    def query(self):
        """
        Create the InfluxDB query.
        """
        return "SELECT {} FROM {} WHERE {}".format(
            ", ".join(self.fields),
            self.measurement,
            " AND ".join(self.clauses),
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
        measurements = [
            {
                field: measurement[field]
                for field in self.fields
            }
            for measurement in self.get_measurements()
        ]
        values = [measurement["value"] for mesaurement in measurements]

        count = len(measurements)
        total = float(sum(values))
        mean = 0 if count == 0 else total / count

        yield Metric(COUNT, count, context=COUNT)
        yield Metric(MEAN, mean, context=MEAN)
        # null context; values are not validated individually
        yield Metric(VALUES, values, context="null")
