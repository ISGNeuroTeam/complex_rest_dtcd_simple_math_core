# -*- coding: utf-8 -*-
"""This module describes logic of the layer between graph and data_collector
"""

import logging

from typing import List, Dict, Tuple

from ..settings import plugin_name, OTL_CREATE_FRESH_SWT
from .data_collector import DataCollector
from .errors import OTLReadfileError, OTLJobWithStatusNewHasNoCacheID, OTLSubsearchFailed, \
    OTLJobWithStatusFailedHasNoCacheID, OTLServiceUnavailable


class SourceWideTable:
    """
    Class to describe how swt works

    Args:
        :: log: local instance of plugin logger
        :: swt_name: name of the swt table to work with
        :: data_collector instance of current swt table
        :: latest_tick_value: value of the _t parameter of the latest tick
    """
    log = logging.getLogger(plugin_name)
    swt_name: str
    data_collector: DataCollector
    latest_tick_value: str

    def __init__(self, swt_name: str) -> None:
        self.log.debug('Input swt_name=%s', swt_name)
        self.swt_name = swt_name
        self.data_collector = DataCollector(name=swt_name)
        self.latest_tick_value = ''

    def initialize(self):
        # we need to check if swt table exists
        # we need to get _t value of the latest tick of swt in order to use
        # for later imports from other swt table

        exists, reason = self.check_swt_exists(self.data_collector)
        if not exists and reason == 'does not exist':
            # if not > create
            self.create_swt(self.data_collector)

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

    def import_data(self, names) -> Dict:
        result = self.data_collector.read_multiple_swts(names, self.latest_tick_value)
        return result

    def check_swt_exists(self, data_collector: DataCollector) -> Tuple[bool, str]:
        """Function to check if swt table with given name exists or not and why

        Args:
            :: data_collector: instance of the DataCollector work with otl service

        Returns:
            :: tuple of flag whether table exists
               and a string, containing the reason of why it does not exist
            """
        counter = 0
        while True:
            try:
                result = data_collector.read_swt(last_row=True)
                self.latest_tick_value = result[0]['_t']
                return True, 'swt table exists'
            except OTLReadfileError:
                return False, 'does not exist'
            except ConnectionError:
                raise
            except (OTLSubsearchFailed, OTLJobWithStatusNewHasNoCacheID,
                    OTLJobWithStatusFailedHasNoCacheID):
                if counter > 5:
                    self.log.exception('we tried to connect to spark 5 times in a row and failed, '
                                       'it seems it is not fine.')
                    raise
                counter += 1
                continue

    def create_swt(self, data_collector: DataCollector) -> None:
        """Function to create swt table

        Args:
            :: data_collector: DataCollector instance to work with otl service
            """

        counter = 0
        while True:
            try:
                result = data_collector.create_fresh_swt(OTL_CREATE_FRESH_SWT)
                self.latest_tick_value = result[0]['_t']
                break
            except (OTLSubsearchFailed, OTLJobWithStatusNewHasNoCacheID,
                    OTLJobWithStatusFailedHasNoCacheID):
                if counter > 5:
                    self.log.exception('we tried to connect to spark 5 times in a row and failed, '
                                       'it seems it is not fine.')
                    raise
                counter += 1
                continue
            except OTLReadfileError:  # this should happen actually, because we are here
                raise

            except OTLServiceUnavailable:
                raise

            except Exception as exception:
                raise Exception(f'unregistered exception: {exception.args[0]}') from exception

    def calc(self, graph_eval_names: List[Dict]) -> list:
        """Here we create a data collector and make it calc swt table

        Args:
            :: graph_eval_names: the list of all nodes and properties names
                                 to be used for creating all eval expressions

        Returns:
              we get the whole recalculated table
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

            except (OTLJobWithStatusNewHasNoCacheID, OTLJobWithStatusFailedHasNoCacheID):
                # here we need to try again
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
