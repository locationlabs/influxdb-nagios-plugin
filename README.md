# influxdb-nagios-plugin

InfluxDB Nagios Plugin

Uses the excellent [nagiosplugin](https://pythonhosted.org/nagiosplugin/) project to create
measurement-based Nagios checks using [InfluxDB](https://influxdb.com/).

[![Build Status](https://travis-ci.org/locationlabs/influxdb-nagios-plugin.png)](https://travis-ci.org/locationlabs/influxdb-nagios-plugin)

## Queries

The plugin issues InfluxDB queries in a few differnt forms based on command line input.

The most common of these (and the query that the tool is built-around) is define by the
`single` sub-command; it will issue a query of the form:

    SELECT time, value FROM <measurement> WHERE time > now() - <age> AND host = '<hostname>'

The plugin then validates that there are a sufficient number of results and that the mean of
these measurements are within acceptable bounds.

This model works well with [Telegraf](https://github.com/influxdb/telegraf) in which healthy
hosts will emit specific measurements regularly. Many of the plugin's defaults are optimized
for this use case.


## Installation

Use pip:

    pip install influxdbnagiosplugin


## Usage

The basic usage for the `single` sub-command is:

    check-measurement \
      --hostname <influxdb-hostname> \
      --username <influxdb-username> \
      --password <influxdb-password> \
	  single <measurement> <monitored_hostname>

A number of other arguments are supported.
