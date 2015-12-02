"""
Nagios Plugin summaries.
"""
from nagiosplugin import Summary


class MeasurementValuesSummary(Summary):
    """
    Customize the success result to show all measurement values.
    """
    def __init__(self, measurement):
        self.measurement = measurement

    def ok(self, results):
        return "{} is {}".format(
            self.measurement,
            # XXX select by name
            results[2].metric.value,
        )
