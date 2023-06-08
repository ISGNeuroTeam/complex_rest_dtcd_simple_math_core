import json
import logging

from ..settings import plugin_name


class Query:
    name: str
    log: logging.Logger = logging.getLogger(plugin_name)

    def __init__(self, name: str = None) -> None:
        self.name = name

    def get(self, eval_names: []) -> str:
        read_query = self.get_read_expression()
        eval_query = self.get_eval_expressions(eval_names=eval_names)
        write_query = self.get_write_expression()

        subquery = f"otloadjob otl={json.dumps(' | '.join((read_query, eval_query)))}"
        result = " | ".join((subquery, write_query))

        return result

    def get_read_expression(self, last_row: bool = False, _path: str = "SWT",
                            _format: str = "JSON") -> str:
        self.log.debug(
            f'input: {self.name=}{" | last_row=" + str(last_row) if last_row else ""} | {_path=} | {_format=}')
        result = f'readFile format={_format} path={_path}/{self.name}{" | tail 1" if last_row else ""}'
        self.log.debug(f'result: {result}')
        return result

    def get_write_expression(self, append: bool = False, _path: str = "SWT",
                             _format: str = "JSON") -> str:
        self.log.debug(f'input: {self.name=}{" | " + str(append) if append else ""} | {_path=} | {_format=}')
        result = f'writeFile format={_format} {"mode=append " if append else ""}path={_path}/{self.name}'
        self.log.debug(f'result: {result}')
        return result

    @staticmethod
    def get_eval_expressions(eval_names: []) -> str:
        result: str = ''
        for name in eval_names:
            _name, _expression = next(iter(name.items()))
            _exp: str = f'| eval \'{_name}\' = {_expression}'
            result += _exp

        return result
