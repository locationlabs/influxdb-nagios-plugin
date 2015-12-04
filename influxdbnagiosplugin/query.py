"""
InfluxDB query building.
"""


class QueryBuilder(object):
    """
    Construct an InfluxDB query.
    """
    def __init__(self,
                 hostname,
                 measurement,
                 age,
                 extra_where_clauses):
        self.hostname = hostname
        self.measurement = measurement
        self.age = age
        self.extra_where_clauses = extra_where_clauses or []

    @property
    def fields(self):
        """
        Generate the InfluxDB query fields.
        """
        return ["time", "value"]

    @property
    def clauses(self):
        return [
            "time > now() - {}".format(self.age),
            "host = '{}'".format(self.hostname)
        ] + [
            "{} = '{}'".format(
                clause.split('=', 1)[0],
                clause.split('=', 1)[1],
            )
            for clause in self.extra_where_clauses
        ]

    @property
    def query(self):
        """
        Create the InfluxDB query.
        """
        return "SELECT {} FROM {} WHERE {}".format(
            ", ".join(self.fields),
            self.measurement,
            " AND ".join(self.clauses),
        )

    @classmethod
    def from_args(cls, args):
        return cls(
            hostname=args.hostname,
            measurement=args.measurement,
            age=args.age,
            extra_where_clauses=args.where,
        )
