import logging
from dtcd_simple_math_core.settings import plugin_name


class ReadQuery:
    log = logging.getLogger(plugin_name)

    @classmethod
    def get(cls, swt_name: str, last_row: bool = False, _path: str = "SWT", _format: str = "JSON") -> str:
        cls.log.debug(f'input: {swt_name=}{" | last_row=" + str(last_row) if last_row else ""} | {_path=} | {_format=}')
        result = f'readFile format={_format} path={_path}/{swt_name}{" | tail 1" if last_row else ""}'
        cls.log.debug(f'result: {result}')
        return result
