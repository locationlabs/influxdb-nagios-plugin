"""
Query construction tests.
"""
from argparse import Namespace

from hamcrest import assert_that, is_, equal_to

from influxdbnagiosplugin.query import QueryBuilder


def test_query():
    args = Namespace(
        age="30s",
        where=None,
        hostname="hostname",
        measurement="cpu_usage_idle",
    )
    query = QueryBuilder.from_args(args).query
    assert_that(query, is_(equal_to(
        "SELECT time, value FROM cpu_usage_idle WHERE time > now() - 30s AND host = 'hostname'"
    )))


def test_query_wherec_lause():
    args = Namespace(
        age="30s",
        where=["path=/"],
        hostname="hostname",
        measurement="disk_free",
    )
    query = QueryBuilder.from_args(args).query
    assert_that(query, is_(equal_to(
        "SELECT time, value FROM disk_free WHERE time > now() - 30s AND host = 'hostname' AND path = '/'"
    )))
