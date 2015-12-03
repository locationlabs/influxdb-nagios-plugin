# influxdb-nagios-plugin

InfluxDB Nagios Plugin

Uses the excellent [nagiosplugin](https://pythonhosted.org/nagiosplugin/) project to create
measurement-based Nagios checks using [InfluxDB](https://influxdb.com/).

[![Build Status](https://travis-ci.org/locationlabs/influxdb-nagios-plugin.png)](https://travis-ci.org/locationlabs/influxdb-nagios-plugin)

## Queries

The plugin issues InfluxDB queries of the form:

    SELECT time, value FROM <measurement> WHERE time > now() - <age> AND host = '<hostname>'

It then validates that there are a sufficient number of measurements in the time range and
that the mean of these measurements are within acceptable bounds.

This model works well with [Telegraf](https://github.com/influxdb/telegraf) in which healthy
hosts will emit specific measurements regularly. Many of the plugin's defaults are optimized
for this use case.


## Installation

Use pip:

    pip install influxdbnagiosplugin


## Usage

The basic usage specifies arguments used to construct and execute an InfluxDB query and then
validate the resulting measurements are in range:

    check-measurement \
      --measurement <measurement> \
      --hostname <monitored_hostname> \
      --age <age> \
      --influxdb-hostname <hostname> \
      --influxdb-port <port> \
      --influxdb-username <username> \
      --influxdb-password <password> \
      --influxdb-database <database>
      --count-error-range <error_range> \
      --count-warning-range <warning_range> \
      --mean-error-range <error_range> \
      --mean-warning-range <warning_range>

Most of these arguments have sane default values. Users will minimally need to specify the
`measurement`, target `hostname`, and connection information to reach an InfluxDB instance
or cluster.
