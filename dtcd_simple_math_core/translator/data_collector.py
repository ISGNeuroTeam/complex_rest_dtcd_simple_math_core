# -*- coding: utf-8 -*-
"""This module is for connecting to OTL service
and to actual data in ExternalData folder through OTL service
"""
import logging
from typing import List, Dict

from ot_simple_connector.connector import Connector  # pylint: disable=import-error
from ..settings import plugin_name, CONNECTOR_CONFIG
from .query import Query
from .errors import OTLReadfileError, OTLJobWithStatusNewHasNoCacheID, \
    OTLSubsearchFailed, OTLJobWithStatusFailedHasNoCacheID, LackingPathNameError, \
    OTLServiceUnavailable
from requests.exceptions import ConnectionError


class DataCollector:
    """Level of abstraction between SWT and actual data in ExternalData folder.
    It creates expressions and uses otl connector to exchange data with spark service.
    If in future otl connector or spark service usage changes -
    it must be changed here only, not in swt or graph layer.

    Args:
        :: log: local instance of plugin logger
        :: name: name of the swt table to work with
        :: connector: local instance of the OTL connector
    """
    log = logging.getLogger(plugin_name)
    connector: Connector

    def __init__(self, name):
        self.name = name
        self.connector = Connector(**CONNECTOR_CONFIG)

    def read_swt(self, last_row: bool) -> list:
        """This function creates an otl query to read a swt table
        and makes connection through otl connector

        Args:
              :: last_row: if we need only last row of the table, but not the whole table
                           we set last_row to True, otherwise - False

        Return:
              We get dataset of swt table [or its last row] if swt table exists
        """
        self.log.debug('reading swt table %s', self.name)
        expression = Query(name=self.name).get_read_expression(last_row=last_row)

        result = self.job_create(expression=expression, cache_ttl=5)
        return list(result)

    def calc_swt(self, eval_names: List[Dict], saved_columns_names: List[str]) -> list:
        """This function creates an otl query to read, eval and write a swt table
        and makes a connection through otl connector

        Args:
              :: eval_names: list of strings where all eval names are stored in order to create
                             all [| eval eval_expression] expressions
        Return:
              We get dataset of swt table if swt table exists
        """
        self.log.debug('calculating swt table %s', self.name)
        expression = Query(name=self.name).get(eval_names=eval_names, saved_columns_names=saved_columns_names)

        result = self.job_create(expression=expression, cache_ttl=5)

        return result

    def job_create(self, expression: str, cache_ttl: int) -> list:
        """Wrapper for working with ot_simple_connector.job.create and
        parse and handle its exceptions"""
        try:
            self.log.debug("data_collector-job_create | trying to create job...")
            result = self.connector.jobs.create(expression, cache_ttl=cache_ttl).dataset.load()
        except ConnectionError as exception:
            message: str = 'OTL service at {%s}:{%s} seem to be unavailable, ' \
                           'check ot_simple_connector ports in a config' % (
                               CONNECTOR_CONFIG['host'], CONNECTOR_CONFIG['port'])
            self.log.exception(message)
            raise OTLServiceUnavailable(message) from exception
        except Exception as e:  # pylint: disable=broad-except, invalid-name
            self.log.debug("data_collector-job_create | exception: %s", e.args[0])
            if "failed because of" in e.args[0]:
                if "Error in  'readfile' command." in e.args[0]:
                    self.log.debug('data_collector-job_create | readFile error - raising '
                                   'OTLReadFileError exception')
                    raise OTLReadfileError(f"OTL readFile failed to read {self.name} swt table. "
                                           f"It doesn't seem to be saved.") from e
                self.log.debug('data_collector-job_create | not readFile error >> '
                               'raising OTLSubsearchFailed exception')
                raise OTLSubsearchFailed("Subsearch failed. Check logs...") from e
            if "Job with status new has no cache id" in e.args[0]:
                self.log.debug('data_collector-job_create | job with status new has no cache id >>>'
                               ' raising OTLJobWithStatusNewHasNoCacheID exception')
                raise OTLJobWithStatusNewHasNoCacheID("Job with status new has no cache id. "
                                                      "Just try again") from e
            if "Job with status failed has no cache id" in e.args[0]:
                self.log.debug('data_collector-job_create | job with status failed has no cache id '
                               '>>> raising OTLJobWithStatusFailedHasNoCacheID exception')
                raise OTLJobWithStatusFailedHasNoCacheID("Job with status failed has no cache id. "
                                                         "Just try again") from e
            if "MaxRetryError" in e.args[0]:
                message: str = 'OTL service at {%s}:{%s} seem to be unavailable, ' \
                               'check ot_simple_connector ports in a config' % (
                                   CONNECTOR_CONFIG['port'], CONNECTOR_CONFIG['host'])
                self.log.exception(message)
                raise OTLServiceUnavailable(message) from e
            raise Exception(f"unregistered exception: {e.args[0]}") from e
        self.log.debug('result=%s', result)
        return result

    def create_fresh_swt(self, query_text: str) -> list:
        """Function with query to create a fresh swt"""
        self.log.debug('creating fresh swt table with name: %s', self.name)
        expression = query_text + self.name
        self.log.debug('expression=%s', expression)
        if len(expression.split('/')) < 2:
            self.log.exception('we seem to be lacking the name of the file in expression')
            raise LackingPathNameError('Some how DataCollector has no swt name given, '
                                       'so we can not proceed the writeFile query. Call the '
                                       'developer to check DataCollector:create_fresh_swt '
                                       'function')
        result = self.job_create(expression=expression, cache_ttl=5)

        return list(result)
