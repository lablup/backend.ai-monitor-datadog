from .datadog import DatadogStatsMonitor


def install_plugin(app):
    stats_monitor = DatadogStatsMonitor()
    stats_monitor.init(app['config'])
    app['stats_monitor'] = stats_monitor
