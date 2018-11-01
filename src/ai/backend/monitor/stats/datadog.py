import datadog

from ai.backend.common.monitor import AbstractStatsMonitor


class DatadogStatsMonitor(AbstractStatsMonitor):

    def __init__(self):
        self.statsd = None

    def init(self, config, **kwargs):
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


def add_plugin_args(parser):
    parser.add('--datadog-api-key', env_var='DATADOG_API_KEY',
               type=str, default=None,
               help='The API key for Datadog monitoring agent.')
    parser.add('--datadog-app-key', env_var='DATADOG_APP_KEY',
               type=str, default=None,
               help='The application key for Datadog monitoring agent.')


def get_plugin(config, **kwargs):
    stats_monitor = DatadogStatsMonitor()
    stats_monitor.init(config, **kwargs)
    return stats_monitor
