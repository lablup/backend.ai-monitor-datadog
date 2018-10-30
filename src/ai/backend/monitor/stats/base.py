from abc import ABC, abstractmethod


class AbstractStatsMonitor(ABC):

    @abstractmethod
    def init(self, config):
        raise NotImplementedError

    @abstractmethod
    def report_stats(self, report_type, metric, *args):
        raise NotImplementedError

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
