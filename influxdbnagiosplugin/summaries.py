"""
Nagios Plugin summaries.
"""
from nagiosplugin import Summary

from influxdbnagiosplugin.resources import VALUES


def is_values(result):
    return result.metric.name == VALUES


class MeasurementValuesSummary(Summary):
    """
    Customize the success result to show all measurement values.
    """
    def __init__(self, query):
        self.query = query

    def ok(self, results):
        result = filter(is_values, results)[0]
        return "{} is {}".format(
            self.query.measurements[0] if self.query.measurements else "result",
            result.metric.value,
        )
