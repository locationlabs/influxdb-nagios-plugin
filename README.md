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

In 0.10.x, Telegraf changed their model from having point measurements (time, value) to
to collections (time, value, value2).  That is, previously there would be mulitple series such as
`cpu_usage_nice` and `cpu_usage_system`, each containing only (time, value) pairs.  In new
model, the series cpu would contain (time, `usage_nice`, `usage_system`).

## Installation

Use pip:

    pip install influxdbnagiosplugin


## Usage

	Usage: check-measurement [OPTIONS] COMMAND1 [ARGS]...

	Command line entry point. Defines common arguments.

	Options:
	  -v, --verbose
	  --hostname TEXT             InfluxDB hostname
	  --port INTEGER              InfluxDB port
	  --username TEXT             InfluxDB usernanme
	  --password TEXT             InfluxDB password
	  --database TEXT             InfluxDB database name
	  --count-error-range TEXT    Range of measurement counts that are NOT
								  considered an error
	  --count-warning-range TEXT  Range of measurement counts that are NOT
								  considered a warning
	  --mean-error-range TEXT     Range of measurement means that are NOT
								  considered an error
	  --mean-warning-range TEXT   Range of measurement counts that are NOT
								  considered a warning
	  --timeout INTEGER           Timeout in seconds for connecting to InfluxDB
	  --help                      Show this message and exit.

	Commands:
	  query   Run an explicit query.
	  single  Run a query for a single measurement.

	check-measurement [OPTIONS] single [OPTIONS] MEASUREMENT HOSTNAME

	  Run a query for a single measurement.

	Options:
	  --age TEXT
	  --where TEXT  Extra where conditions to include.
	  --field TEXT
	  --help        Show this message and exit.


	Usage: check-measurement query [OPTIONS] QUERY

	  Run an explicit query.

	Options:
	  --help  Show this message and exit.
