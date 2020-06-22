import datadog

from typing import (
    Any,
    Mapping,
    Union,
)

from ai.backend.common.monitor import AbstractStatsMonitor
from ai.backend.common.plugin.monitor import AbstractStatReporterPlugin


class DatadogStatsMonitor(AbstractStatReporterPlugin):

    def __init__(self, plugin_config: Mapping[str, Any], local_config: Mapping[str, Any]) -> None:
        super().__init__(plugin_config, local_config)
        self.statsd = None

    async def init(self) -> None:
        datadog.initialize(api_key=self.plugin_config['datadog_api_key'],
                           app_key=self.plugin_config['datadog_app_key'])
        self.statsd = datadog.statsd
        self.statsd.__enter__()

    async def cleanup(self) -> None:
        self.statsd.__exit__(None, None, None)

    async def update_plugin_config(self, new_plugin_config: Mapping[str, Any]) -> None:
        self.plugin_config = self.new_plugin_config
        if self.statsd:
            await self.statsd.cleanup()
            await self.statsd.init()

    async def report_stats(self, report_type: str, metric: Union[float, int], *args):
        if report_type == 'increment':
            self.statsd.increment(metric)
        elif report_type == 'gauge':
            value = args[0]
            self.statsd.gauge(metric, value)
        else:
            raise ValueError(f'Not supported report type: {report_type}')
