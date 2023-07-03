# -*- coding: utf-8 -*-
"""This module describes logic of the layer between graph and data_collector
"""

import logging

from typing import List, Dict

from ..settings import plugin_name, OTL_CREATE_FRESH_SWT
from .data_collector import DataCollector
from .errors import OTLReadfileError, OTLJobWithStatusNewHasNoCacheID, OTLSubsearchFailed, \
    OTLJobWithStatusFailedHasNoCacheID


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
        self.log.debug('Input swt_name=%s', swt_name)
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
        self.log.debug('reading %s swt table | last_row=%s', self.swt_name, last_row)

        result = data_collector.read_swt(last_row=last_row)
        self.log.debug('result=%s', result)

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
        self.log.debug('calculating %s swt table with %s', self.swt_name, graph_eval_names)
        result = []
        counter = 0
        while True:
            try:
                self.log.debug('swt-calc | trying..')
                result = data_collector.calc_swt(eval_names=graph_eval_names)
                break
            except OTLReadfileError:  # here we have to save swt table first
                self.log.debug('swt-calc | OTLReadFileError caught, '
                               'trying to create fresh swt table')
                data_collector.create_fresh_swt(OTL_CREATE_FRESH_SWT)
            except OTLJobWithStatusNewHasNoCacheID:  # here we need to try again
                # and make a counter and exit after like 5 tries
                self.log.exception('swt-calc | OTLJobWithStatusNewHasNoCacheID caught >>> '
                                   'We seem to fail finding swt table because of spark '
                                   '| %s try', counter + 1)
                if counter > 5:
                    self.log.exception('We failed to find swt table because of spark for '
                                       '5 attempts in a row')
                    raise
                counter += 1
                continue
            except OTLSubsearchFailed:
                self.log.debug('swt-calc | OTLSubsearchFailed caught, '
                               'trying to check if swt table exists...')
                # pylint: disable=pointless-string-statement
                '''Subsearch may fail because of subsearch error,
                or because there was a readFile error.

                Need to check if swt exists and readFile can read it.

                If not - then we create swt table.
                If yes - than its a subsearch error and we raise.
                '''
                try:
                    self.log.debug('swt-calc-subsearchFailed | try read_swt...')
                    data_collector.read_swt(last_row=False)
                    self.log.debug('swt-calc-subsearchFailed | swt table exists...')
                except OTLReadfileError:
                    self.log.debug('swt-calc-subsearchFailed | OTLReadfileError caught >>> '
                                   'there is no swt table, creating...')
                    data_collector.create_fresh_swt(OTL_CREATE_FRESH_SWT)
                    self.log.debug('swt-calc-subsearchFailed | OTLReadfileError caught >>> '
                                   'swt table was created...')
                    continue
                except OTLSubsearchFailed:
                    self.log.debug('swt-calc-subsearchFailed | OTLSubsearchFailed caught >>> '
                                   'there is no swt table, creating...')
                    self.log.exception('Subsearch failure. Check logs')
                    raise
                except OTLJobWithStatusFailedHasNoCacheID:
                    self.log.debug('swt-calc-subsearchFailed | OTLJobWithStatusFailedHasNoCacheID caught >>> '
                                   'there is no swt table, creating...')
                    self.log.exception('Subsearch failure. Check logs')
                    raise
            except Exception as e:  # pylint: disable=broad-except, invalid-name
                self.log.exception('unregistered exception: %s', e)
                raise

        self.log.debug('result=%s', result)

        return result
