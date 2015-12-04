"""
Query construction tests.
"""
from hamcrest import assert_that, is_, equal_to

from influxdbnagiosplugin.query import ExplicitQueryBuilder, SingleMeasurementQueryBuilder


def test_explicit_query():
    query = ExplicitQueryBuilder("SHOW MEASUREMENTS")
    assert_that(query().query, is_(equal_to(
        "SHOW MEASUREMENTS"
    )))


def test_single_measurement_query():
    query = SingleMeasurementQueryBuilder.for_hostname_and_age(
        measurement="disk_free",
        hostname="hostname",
        age="30s",
        where=[],
    )
    assert_that(query().query, is_(equal_to(
        "SELECT time, value FROM disk_free"
        " WHERE time > now() - 30s"
        " AND host = 'hostname'"
    )))


def test_single_measurement_query_where_clause():
    query = SingleMeasurementQueryBuilder.for_hostname_and_age(
        measurement="disk_free",
        hostname="hostname",
        age="30s",
        where=["path=/"],
    )
    assert_that(query().query, is_(equal_to(
        "SELECT time, value FROM disk_free"
        " WHERE time > now() - 30s"
        " AND host = 'hostname'"
        " AND path = '/'"
    )))


def test_single_measurement_query_where_clause_quoted():
    query = SingleMeasurementQueryBuilder.for_hostname_and_age(
        measurement="disk_free",
        hostname="hostname",
        age="30s",
        where=["path='/'"],
    )
    assert_that(query().query, is_(equal_to(
        "SELECT time, value FROM disk_free"
        " WHERE time > now() - 30s"
        " AND host = 'hostname'"
        " AND path = '/'"
    )))
