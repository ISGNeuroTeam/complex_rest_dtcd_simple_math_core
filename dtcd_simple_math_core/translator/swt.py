# -*- coding: utf-8 -*-
"""This module describes logic of the layer between graph and data_collector
"""

import logging

from typing import List, Dict

from ..settings import plugin_name, OTL_CREATE_FRESH_SWT
from .data_collector import DataCollector
from .errors import OTLReadfileError, OTLJobWithStatusNewHasNoCacheID, OTLSubsearchFailed


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
        self.log.debug(f'reading {self.swt_name} swt table | {last_row=}')

        result = data_collector.read_swt(last_row=last_row)
        self.log.debug(f'{result=}')

        return result

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
        self.log.debug(f'calculating {self.swt_name} swt table with {graph_eval_names=}')
        result = []
        counter = 0
        while True:
            try:
                result = data_collector.calc_swt(eval_names=graph_eval_names)
                break
            except OTLReadfileError:  # here we have to save swt table first
                data_collector.create_fresh_swt(OTL_CREATE_FRESH_SWT)
            except OTLJobWithStatusNewHasNoCacheID:  # here we need to try again
                # and make a counter and exit after like 5 tries
                if counter > 5:
                    self.log.exception(f'We seem to fail finding swt table because of spark 5 failures in a row')
                    raise
                counter += 1
                continue
            except OTLSubsearchFailed:
                """Subsearch may fail because of subsearch error or because there was a readFile error
                Need to check if swt exists and readFile can read it. 
                If not - then we create swt table.
                If yes - than its a subsearch error and we raise 
                """
                try:
                    data_collector.read_swt(last_row=False)
                    self.log.exception(f'Subsearch failure. Checking if {self.swt_name} swt table exists...')
                except OTLReadfileError:
                    data_collector.create_fresh_swt(OTL_CREATE_FRESH_SWT)
                    self.log.exception(f'swt table was created...')
                    continue
                except OTLSubsearchFailed:
                    self.log.exception(f'Subsearch failure. Check logs')
                    raise
            except Exception as e:
                self.log.exception(f'unregistered exception: {e}')
                raise

        self.log.debug(f'{result}')

        return result
