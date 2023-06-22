# -*- coding: utf-8 -*-
"""This module describes logic of the layer between graph and data_collector
"""

import logging

from typing import List, Dict

from ..settings import plugin_name
from .data_collector import DataCollector


class SourceWideTable:
    """
    Class to describe how swt works

    Args:
        :: log: local instance of plugin logger
        :: swt_name: name of the swt table to work with
    """
    log = logging.getLogger(plugin_name)
    swt_name: str

    def __init__(self, swt_name: str) -> None:
        self.log.debug(f'Input {swt_name=}')
        self.swt_name = swt_name

    def read(self, last_row: bool = False) -> list:
        """Here we create a data collector and make it read swt table

        Args:
            :: last_row: flag to point out if we need only last row of the table
                         or the whole table

        Returns:
              we get either the whole table, or last row
              # TODO [? or empty table if it does not exist]
        """
        data_collector: DataCollector = DataCollector(self.swt_name)
        return data_collector.read_swt(last_row=last_row)

    def calc(self, graph_eval_names: List[Dict]) -> list:
        """Here we create a data collector and make it calc swt table

        Args:
            :: graph_eval_names: the list of all nodes and properties names
                                 to be used for creating all eval expressions

        Returns:
              we get either the whole recalculated table
              # TODO [? or empty table if it does not exist]
        """
        data_collector: DataCollector = DataCollector(self.swt_name)
        return data_collector.calc_swt(eval_names=graph_eval_names)
