"""
Command line entry point.
"""
from argparse import ArgumentParser
from nagiosplugin import (
    Check,
    guarded,
    ScalarContext,
)

from influxdbnagiosplugin.resources import COUNT, MEAN, Measurements
from influxdbnagiosplugin.summaries import MeasurementValuesSummary


def add_nagios_args(parser):
    """
    Specify arguments encouraged by Nagios.
    """
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
    )


def add_query_args(parser):
    """
    Specify arguments used to construct InfluxDB query.
    """
    parser.add_argument(
        "--hostname",
        required=True,
        help="Monitored hostname",
    )
    parser.add_argument(
        "--measurement",
        required=True,
        help="InfluxDB measurement name",
    )
    parser.add_argument(
        "--age",
        default="30s",
        help="InfluxDB measurement age",
    )


def add_influxdb_args(parser):
    """
    Add arguments to connect to InfluxDB.
    """
    parser.add_argument(
        "--influxdb-hostname",
        default="localhost",
        help="InfluxDB hostname",
    )
    parser.add_argument(
        "--influxdb-port",
        default=8086,
        help="InfluxDB port",
    )
    parser.add_argument(
        "--influxdb-username",
        default="influxdb",
        help="InfluxDB usernanme",
    )
    parser.add_argument(
        "--influxdb-password",
        default="secret",
        help="InfluxDB password",
    )
    parser.add_argument(
        "--influxdb-database",
        default="telegraf",
        help="InfluxDB database name",
    )


def add_range_args(parser):
    """
    Add arguments for measurement range validation.
    """
    parser.add_argument(
        "--count-error-range",
        default="1:",
        help="Range of measurement counts that are NOT considered an error",
    )
    parser.add_argument(
        "--count-warning-range",
        default="2:",
        help="Range of measurement counts that are NOT considered a warning",
    )
    parser.add_argument(
        "--mean-error-range",
        default="",
        help="Range of measurement means that are NOT considered an error",
    )
    parser.add_argument(
        "--mean-warning-range",
        default="",
        help="Range of measurement counts that are NOT considered a warning",
    )


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()

    add_nagios_args(parser)
    add_query_args(parser)
    add_influxdb_args(parser)
    add_range_args(parser)

    args = parser.parse_args()
    return args


@guarded
def main():
    args = parse_args()

    check = Check(
        Measurements(
            hostname=args.hostname,
            measurement=args.measurement,
            age=args.age,
            influxdb_hostname=args.influxdb_hostname,
            influxdb_port=args.influxdb_port,
            influxdb_username=args.influxdb_username,
            influxdb_password=args.influxdb_password,
            influxdb_database=args.influxdb_database,
        ),
        ScalarContext(COUNT, args.count_warning_range, args.count_error_range),
        ScalarContext(MEAN, args.mean_warning_range, args.mean_error_range),
        MeasurementValuesSummary(
            measurement=args.measurement,
        )
    )
    check.main(args.verbose)
