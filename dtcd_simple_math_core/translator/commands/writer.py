import logging


class Writer:
    PLUGIN_NAME = "dtcd_simple_math_core"
    SWT_BASE_PATH = "SWT"
    FORMAT = "JSON"
    log = logging.getLogger(PLUGIN_NAME)

    @classmethod
    def rewrite(cls, swt_name):
        complete_line = f'writeFile format={cls.FORMAT} path={cls.SWT_BASE_PATH}/{swt_name}'
        cls.log.debug(f"Write otl: {complete_line}")
        return complete_line

    @classmethod
    def append(cls, swt_name):
        complete_line = f'writeFile format={cls.FORMAT} mode=append path={cls.SWT_BASE_PATH}/{swt_name}'
        cls.log.debug(f"Write otl: {complete_line}")
        return complete_line
