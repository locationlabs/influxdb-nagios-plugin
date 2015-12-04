"""
Nagios Plugin resource(s).
"""
from logging import getLogger

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
                 query,
                 client):
        self.query = query
        self.client = client
        self.logger = getLogger('nagiosplugin')

    def get_results(self):
        """
        Fetch results from InfluxDB.
        """
        try:
            return self.query.get_results(self.client)
        except Exception as error:
            self.logger.info("Failed to query InfluxDB: {}".format(
                error,
            ))
            raise CheckError(error)

    def probe(self):
        """
        Query InfluxDB; yield the count and mean of the measurements.
        """
        def get_value(result):
            # measurement results should have a 'value' field
            if "value" in result:
                return result["value"]
            # otherwise, 'name' is a good guess
            return result["name"]

        values = [
            get_value(result) for result in self.get_results()
        ]

        count = len(values)
        yield Metric(COUNT, count, context=COUNT)

        try:
            total = float(sum(values))
            mean = 0 if count == 0 else total / count
            yield Metric(MEAN, mean, context=MEAN)
        except TypeError:
            # non numeric queries won't have a mean
            pass

        # null context; values are not validated individually
        yield Metric(VALUES, values, context="null")
