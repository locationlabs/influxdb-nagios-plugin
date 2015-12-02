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


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()

    # Nagios encourages verbosity controls for debugging
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
    )

    # Specify the thequery arguments
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

    # Specify the connection arguments
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

    # Specify the error and warning ranges
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

