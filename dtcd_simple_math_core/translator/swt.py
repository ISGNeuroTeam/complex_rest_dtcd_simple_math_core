# -*- coding: utf-8 -*-
"""This module describes logic of the layer between graph and data_collector
"""

import logging

from typing import List, Dict, Tuple

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

    def check_swt_exists(self, dc: DataCollector) -> Tuple[bool, str]:
        exists: bool = True
        reason: str = 'Default reason'
        counter = 0
        while True:
            try:
                dc.read_swt(last_row=True)
                return True, 'swt table exists'
            except OTLReadfileError:
                return False, 'does not exist'
            except (OTLSubsearchFailed, OTLJobWithStatusNewHasNoCacheID, OTLJobWithStatusFailedHasNoCacheID) as e:
                if counter > 5:
                    self.log.exception('we tried to connect to spark 5 times in a row and failed, '
                                       'it seems it is not fine.')
                    raise
                counter += 1
                continue

    def create_swt(self, dc: DataCollector) -> None:
        counter = 0
        while True:
            try:
                dc.create_fresh_swt(OTL_CREATE_FRESH_SWT)
                break
            except (OTLSubsearchFailed, OTLJobWithStatusNewHasNoCacheID, OTLJobWithStatusFailedHasNoCacheID) as e:
                if counter > 5:
                    self.log.exception('we tried to connect to spark 5 times in a row and failed, '
                                       'it seems it is not fine.')
                    raise
                counter += 1
                continue
            except OTLReadfileError:  # this should happen actually, because we are here
                raise

            except Exception as e:
                raise ('unregistered exception: %s', e.args[0])

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
        # check if swt table is created
        exists, reason = self.check_swt_exists(data_collector)
        if not exists and reason == 'does not exist':
            # if not > create
            self.create_swt(data_collector)

        while True:
            try:
                self.log.debug('swt-calc | trying..')
                result = data_collector.calc_swt(eval_names=graph_eval_names)
                break

            except (OTLJobWithStatusNewHasNoCacheID, OTLJobWithStatusFailedHasNoCacheID):  # here we need to try again
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
            except (OTLSubsearchFailed, OTLReadfileError):
                raise
            except Exception as e:  # pylint: disable=broad-except, invalid-name
                self.log.exception('unregistered exception: %s', e)
                raise

        self.log.debug('result=%s', result)

        return result
