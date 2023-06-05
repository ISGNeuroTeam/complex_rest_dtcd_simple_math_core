import logging


from ..settings import plugin_name
from .data_collector import DataCollector


class SourceWideTable:
    log = logging.getLogger(plugin_name)

    def __init__(self, swt_name: str, ) -> None:
        self.log.debug(f'Input {swt_name=}')
        self.swt_name = swt_name

    def read(self, last_row: bool = False) -> list:
        data_collector = DataCollector(self.swt_name)
        return data_collector.read_swt(last_row=last_row)

    def calc(self, graph_eval_names: str) -> list:
        data_collector = DataCollector(self.swt_name)
        return data_collector.calc_swt(eval_names=graph_eval_names)
