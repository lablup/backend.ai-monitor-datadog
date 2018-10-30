import datadog

from .base import AbstractStatsMonitor


class DatadogStatsMonitor(AbstractStatsMonitor):

    def __init__(self):
        self.statsd = None

    def init(self, config):
        datadog.initialize(api_key=config.datadog_api_key,
                           app_key=config.datadog_app_key)
        self.statsd = datadog.statsd

    def report_stats(self, report_type, metric, *args):
        if report_type == 'increment':
            self.statsd.increment(metric)
        elif report_type == 'gauge':
            value = args[0]
            self.statsd.gauge(metric, value)
        else:
            raise ValueError(f'Not supported report type: {report_type}')

    def __enter__(self):
        self.statsd.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.statsd.__exit__(type, value, traceback)


def get_plugin(config):
    stats_monitor = DatadogStatsMonitor()
    stats_monitor.init(config)
    return stats_monitor
