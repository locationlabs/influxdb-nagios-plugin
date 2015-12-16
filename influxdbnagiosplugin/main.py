"""
Command line entry point.
"""
from click import argument, group, option
from influxdb import InfluxDBClient
from nagiosplugin import (
    Check,
    guarded,
    ScalarContext,
)

from influxdbnagiosplugin.query import ExplicitQueryBuilder, SingleMeasurementQueryBuilder
from influxdbnagiosplugin.resources import COUNT, MEAN, Measurements
from influxdbnagiosplugin.summaries import MeasurementValuesSummary


@group(chain=True)
@option("-v", "--verbose", count=True)
@option("--hostname", default="localhost", help="InfluxDB hostname")
@option("--port", default=8086, help="InfluxDB port")
@option("--username", default="influxdb", help="InfluxDB usernanme")
@option("--password", default="secret", help="InfluxDB password")
@option("--database", default="telegraf", help="InfluxDB database name")
@option("--count-error-range", default="1:", help="Range of measurement counts that are NOT considered an error")  # noqa
@option("--count-warning-range", default="2:", help="Range of measurement counts that are NOT considered a warning")  # noqa
@option("--mean-error-range", default="", help="Range of measurement means that are NOT considered an error")  # noqa
@option("--mean-warning-range", default="", help="Range of measurement counts that are NOT considered a warning")  # noqa
@option("--timeout", default=5, help="Timeout in seconds for connecting to InfluxDB")
def main(**kwargs):
    """
    Command line entry point. Defines common arguments.
    """
    pass


@main.resultcallback()
@guarded
def check(processors, **args):
    """
    Invoke the InfluxDB check using the Nagios plugin framework.

    Reads the query from the processors chain.
    """
    query = processors[0]()

    client = InfluxDBClient(
        host=args["hostname"],
        port=args["port"],
        username=args["username"],
        password=args["password"],
        database=args["database"],
        timeout=args["timeout"],
    )

    check = Check(
        Measurements(
            query=query,
            client=client,
        ),
        ScalarContext(COUNT, args["count_warning_range"], args["count_error_range"]),
        ScalarContext(MEAN, args["mean_warning_range"], args["mean_error_range"]),
        MeasurementValuesSummary(
            query=query,
        )
    )
    check.main(args["verbose"])


@main.command()
@argument("query")
def query(query):
    """
    Run an explicit query.
    """
    return ExplicitQueryBuilder(query)


@main.command()
@argument("measurement")
@argument("hostname")
@option("--age", default="30s")
@option("--where", multiple=True, help="Extra where conditions to include.")
def single(measurement, hostname, age, where):
    """
    Run a query for a single measurement.
    """
    return SingleMeasurementQueryBuilder.for_hostname_and_age(
        measurement=measurement,
        hostname=hostname,
        age=age,
        where=where,
    )
