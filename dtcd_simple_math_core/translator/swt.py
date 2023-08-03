# -*- coding: utf-8 -*-
"""This module describes logic of the layer between graph and data_collector
"""

import logging
import re

from typing import List, Dict, Tuple

from ..settings import plugin_name, OTL_CREATE_FRESH_SWT, FILTER_DATALAKENODE_COLUMNS, RE_DATALAKENODE
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
        :: datalakenode_columns: list of columns that will be imported from wide table
                                 and must not be deleted from target swt table
    """
    log = logging.getLogger(plugin_name)
    swt_name: str
    data_collector: DataCollector
    latest_tick_value: str
    datalakenode_columns: List[str]

    def __init__(self, swt_name: str) -> None:
        self.log.debug('Input swt_name=%s', swt_name)
        self.swt_name = swt_name
        self.data_collector = DataCollector(name=swt_name)
        self.latest_tick_value = ''
        self.datalakenode_columns = []

    def initialize(self):
        # we need to check if swt table exists
        # we need to get _t value of the latest tick of swt in order to use
        # for later imports from other swt table

        exists, reason = self.check_swt_exists(self.data_collector)
        if not exists and reason == 'does not exist':
            # if not > create
            self.create_swt(self.data_collector)

        if FILTER_DATALAKENODE_COLUMNS:
            # get a list of `datalakenodes` saved in 'self.swt_name`.tmp file
            # 'datalakenodes' are columns from *.tmp swt table that have name matching
            # GRAPH_GLOBALS['re_datalakenode']
            counter = 0
            try:
                temp_dc = DataCollector(name=self.swt_name + '.tmp')
                datalakenode_data = temp_dc.read_swt(last_row=True)
                self.datalakenode_columns = self.get_datalakenodes(datalakenode_data)
            except OTLReadfileError:
                self.datalakenode_columns = []
            except (OTLSubsearchFailed, OTLJobWithStatusNewHasNoCacheID,
                    OTLJobWithStatusFailedHasNoCacheID):
                if counter > 15:
                    self.log.exception('we tried to connect to spark 5 times in a row and failed, '
                                       'it seems it is not fine.')
                    raise
                counter += 1

    @staticmethod
    def get_datalakenodes(dln_data: List) -> List:
        if len(dln_data) == 0:
            return []
        result = [match for match in dln_data[0].keys() if re.match(RE_DATALAKENODE, match)]
        return result

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

    def calc(self, graph_eval_names: List[Dict], imported_columns: List[str]) -> list:
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
        saved_columns = self.datalakenode_columns + imported_columns

        while True:
            try:
                self.log.debug('swt-calc | trying..')
                result = data_collector.calc_swt(eval_names=graph_eval_names,
                                                 saved_columns_names=saved_columns)
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
