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

    def get(self, eval_names: List[Dict]) -> str:
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
        fields_query = self.get_fields_expression(eval_names=eval_names)
        write_query = self.get_write_expression()
        self.log.debug('read_query=%s', read_query)
        self.log.debug('eval_query=%s', eval_query)
        self.log.debug('fields_query=%s', fields_query)
        self.log.debug('write_query=%s', write_query)

        subquery = f"otloadjob otl={json.dumps(read_query + eval_query, ensure_ascii=False)}"
        self.log.debug('subquery=%s', subquery)
        result = " | ".join((subquery, fields_query, write_query))
        self.log.debug('result: %s', result)

        return result

    def get_read_expression(self, last_row: bool = False, file_path: str = "SWT",
                            file_format: str = "JSON", where: str = '') -> str:
        """Function to create readFile otl query
        Args:
            :: last_row: flag to point out whether we require the whole table or
                         just the last row of it
            :: file_path: path to swt table file inside ExternalData
            :: file_format: format of the swt table

        Returns:
            string of the otl query
        """
        self.log.debug('input: self.name=%s | last_row=%s | file_path=%s | file_format=%s',
                       self.name, last_row, file_path, file_format)
        result = f'readFile format={file_format} path={file_path}/{self.name}' \
                 f'{" | tail 1" if last_row else ""}{where} '
        self.log.debug('result: %s', result)

        return result

    @staticmethod
    def get_read_expressions(names: List[str], tick: str) -> str:
        result = ''
        for index, name in enumerate(names):
            string = f'| readFile format=json path=SWT/{name} | where _t={tick}'
            if index > 0:
                result += f'| join _t [{string}]'
            else:
                result += string
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
        self.log.debug('input: self.name=%s | append=%s | file_path=%s | file_format=%s',
                       self.name, append, file_path, file_format)
        result = f'writeFile format={file_format} {"mode=append " if append else ""}' \
                 f'path={file_path}/{self.name}'
        self.log.debug('result: %s', result)

        return result

    def get_eval_expressions(self, eval_names: List[Dict]) -> str:
        """Function to create eval otl queries
        Args:
            :: eval_names: list of dictionaries with object property names and its values

        Returns:
            string of the otl query
        """

        self.log.debug('getting eval expressions for eval_names=%s', eval_names)
        len_of_eval_names = len(eval_names)
        self.log.debug('printing all %s names', len_of_eval_names)

        for name in eval_names:
            for key, value in name.items():
                self.log.debug('eval_name: %(key)s:%(value)s', {'key': key, 'value': value})

        self.log.debug('now calculating eval expression...')

        result: str = ''
        for name in eval_names:
            _name, _expression = next(iter(name.items()))
            _exp: str = f'| eval \'{_name}\' = {_expression} '
            result += _exp
        self.log.debug('result: %s', result)

        return result

    def get_fields_expression(self, eval_names: List[Dict]) -> str:
        """Function to create fields part of the expression
        It must include the names of the fields, that must stay at the swt table

        Stay by default: _t, _sn and _time fields
        """

        self.log.debug('start getting fields expression with this names: %s', eval_names)
        eval_names_list: list = []
        for eval_name in eval_names:
            eval_names_list.append(list(eval_name.items())[0][0])
        self.log.debug('eval_names_list: %s', eval_names_list)

        eval_names_list_string = ', '.join(eval_names_list)
        self.log.debug('eval_names_list_str: %s', eval_names_list_string)

        result = 'fields _t, _sn, _time'
        if eval_names_list:
            result += ', ' + eval_names_list_string
        self.log.debug('result: %s', result)

        return result
