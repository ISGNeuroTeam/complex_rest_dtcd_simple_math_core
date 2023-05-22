import logging
from dtcd_simple_math_core.settings import plugin_name


class WriteQuery:
    log = logging.getLogger(plugin_name)

    @classmethod
    def get(cls, swt_name: str, append: bool = False, _path: str = "SWT", _format: str = "JSON") -> str:
        cls.log.debug(f'input: {swt_name=}{" | " + append if append else ""} | {_path=} | {_format=}')
        result = f'writeFile format={_format} {"mode=append " if append else ""}path={_path}/{swt_name}'
        cls.log.debug(f'result: {result}')
        return result
