from .datadog import DatadogStatsMonitor


def get_plugin(app):
    stats_monitor = DatadogStatsMonitor()
    stats_monitor.init(app['config'])
    return stats_monitor
