"""
InfluxDB query building.
"""
from abc import ABCMeta, abstractmethod
from logging import getLogger

from six import add_metaclass


DEFAULT_FIELDS = [
    "time",
    "value",
]


def maybe_quote(value):
    """
    Quote a value for InfluxDB if necessary.
    """
    if value[0] == "'" and value[-1] == "'":
        return value
    return "'{}'".format(value)


def kv_condition(key, value):
    """
    Generate a key value equality condition.

    Ensure that the value is properly quoted.
    """
    return "{} = {}".format(key, maybe_quote(value))


def age_condition(age):
    return "time > now() - {}".format(age)


def host_condition(hostname):
    return kv_condition("host", hostname)


def kv_conditions(conditions):
    return [
        kv_condition(*condition.split("=", 1))
        for condition in conditions or []
    ]


class Query(object):
    """
    Query wrapper.
    """
    def __init__(self, query, measurements=None):
        self.query = query
        self.measurements = measurements or []
        self.logger = getLogger('nagiosplugin')

    def __str__(self):
        return self.query

    def get_results(self, client):
        self.logger.debug("Querying InfluxDB at {}:{} with query: \"{}\"".format(
            client._host,
            client._port,
            self.query,
        ))
        results = client.query(self.query)
        self.logger.info("Received result set: {}".format(results))
        return list(results.get_points())


@add_metaclass(ABCMeta)
class QueryBuilder(object):
    """
    Abstract callable that builds queries.
    """
    @abstractmethod
    def __call__(self):
        pass


class ExplicitQueryBuilder(QueryBuilder):
    """
    Return the provided query.
    """
    def __init__(self, query):
        self.query = query

    def __call__(self):
        return Query(
            query=self.query,
        )


class SingleMeasurementQueryBuilder(QueryBuilder):
    """
    Build a simple InfluxDB query of the form:

        SELECT <fields> FROM <measurement> WHERE <conditions>
    """
    def __init__(self,
                 fields=None,
                 measurement=None,
                 conditions=None):
        self.fields = fields or ["time", "value"]
        self.measurement = measurement
        self.conditions = conditions or []

    def __call__(self):
        return Query(
            query="SELECT {} FROM {} WHERE {}".format(
                ", ".join(self.fields),
                self.measurement,
                " AND ".join(self.conditions),
            ),
            measurements=[
                self.measurement,
            ],
        )

    @classmethod
    def for_hostname_and_age(cls, measurement, age, hostname, where):
        return cls(
            fields=DEFAULT_FIELDS,
            measurement=measurement,
            conditions=[
                age_condition(age),
                host_condition(hostname),
            ] + kv_conditions(where),
        )
