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
    def __init__(self, measurement):
        self.measurement = measurement

    def ok(self, results):
        result = filter(is_values, results)[0]
        return "{} is {}".format(
            self.measurement,
            result.metric.value,
        )
