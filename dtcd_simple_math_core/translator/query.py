# -*- coding: utf-8 -*-
"""This module describes logic of creating otl queries
"""

import json
import logging

from typing import List, Dict

from ..settings import plugin_name


class Query:
    """Class stores name of the swt table and creates otl queries to work with this swt table

    Args:
        :: name: name of the swt table
        :: log: local logger instance
    """
    name: str
    log: logging.Logger = logging.getLogger(plugin_name)

    def __init__(self, name: str = None) -> None:
        self.name = name

    def get(self, eval_names: []) -> str:
        """Function to create a major otl query to:
        - read swt table
        - calc swt table
        - write swt table

        Args:
            :: eval_names: list of all eval names required to evaluate

        Returns:
            string of the otl query
        """
        read_query = self.get_read_expression()
        eval_query = self.get_eval_expressions(eval_names=eval_names)
        write_query = self.get_write_expression()
        self.log.debug(f'{read_query=}')
        self.log.debug(f'{eval_query=}')
        self.log.debug(f'{write_query=}')

        subquery = f"otloadjob otl={json.dumps(read_query + eval_query)}"
        self.log.debug(f'{subquery=}')
        result = " | ".join((subquery, write_query))
        self.log.debug(f'result: {result=}')

        return result

    def get_read_expression(self, last_row: bool = False, file_path: str = "SWT",
                            file_format: str = "JSON") -> str:
        """Function to create readFile otl query
        Args:
            :: last_row: flag to point out whether we require the whole table or just the last row of it
            :: file_path: path to swt table file inside ExternalData
            :: file_format: format of the swt table

        Returns:
            string of the otl query
        """
        self.log.debug(
            f'input: {self.name=}{" | last_row=" + str(last_row) if last_row else ""} | {file_path=} | {file_format=}')
        result = f'readFile format={file_format} path={file_path}/{self.name}{" | tail 1" if last_row else ""}  '
        self.log.debug(f'result: {result}')

        return result

    def get_write_expression(self, append: bool = False, file_path: str = "SWT",
                             file_format: str = "JSON") -> str:
        """Function to create writeFile otl query
        Args:
            :: append: flag to point out whether we use append mode or not
                       writeFile by default rewrites file totally, but using "mode=append" allows
                       to save updated swt table without rewriting it totally.
            :: file_path: path to swt table file inside ExternalData
            :: file_format: format of the swt table

        Returns:
            string of the otl query
        """
        self.log.debug(f'input: {self.name=}{" | " + str(append) if append else ""} | {file_path=} | {file_format=}')
        result = f'writeFile format={file_format} {"mode=append " if append else ""}path={file_path}/{self.name}'
        self.log.debug(f'result: {result}')

        return result

    def get_eval_expressions(self, eval_names: List[Dict]) -> str:
        """Function to create eval otl queries
        Args:
            :: eval_names: list of dictionaries with object property names and its values

        Returns:
            string of the otl query
        """

        self.log.debug(f'getting eval expressions for {eval_names=}')
        result: str = ''
        for name in eval_names:
            _name, _expression = next(iter(name.items()))
            _exp: str = f'| eval \'{_name}\' = {_expression} '
            result += _exp
        self.log.debug(f'{result=}')

        return result
