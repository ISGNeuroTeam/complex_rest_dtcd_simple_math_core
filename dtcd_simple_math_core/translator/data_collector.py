"""This module is for connecting to OTL service
and to actual data in ExternalData folder through OTL service
"""
import logging

from ..settings import plugin_name, CONNECTOR_CONFIG
from ot_simple_connector.connector import Connector
from .query import Query
from .errors import OTLReadfileError, OTLJobWithStatusNewHasNoCacheID


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
        self.log.debug(f'reading swt table {self.name}')
        expression = Query(name=self.name).get_read_expression(last_row=last_row)

        # TODO describe the situation [and result] when when required swt table does not exist
        result = []
        try:
            result = self.connector.jobs.create(expression, cache_ttl=5).dataset.load()
        except Exception as e:
            if "Error in  'readfile' command." in e.args[0]:
                raise OTLReadfileError(f"OTL readFile failed to read {self.name} swt table. "
                                       f"It doesn't seem to be saved.") from e
            elif "Job with status new has no cache id" in e.args[0]:
                raise OTLJobWithStatusNewHasNoCacheID(f"Job with status new has no cache id. Just try again") from e
            else:
                raise Exception(f"unregistered exception: {e.args[0]}") from e
        return result

    def calc_swt(self, eval_names: [str]) -> list:
        """This function creates an otl query to read, eval and write a swt table
        and makes a connection through otl connector

        Args:
              :: eval_names: list of strings where all eval names are stored in order to create
                             all [| eval eval_expression] expressions
        Return:
              We get dataset of swt table if swt table exists
        """
        self.log.debug(f'calculating swt table {self.name}')
        expression = Query(name=self.name).get(eval_names=eval_names)

        result = self.connector.jobs.create(expression, cache_ttl=5).dataset.load()
        self.log.debug(f'{result=}')

        return result
