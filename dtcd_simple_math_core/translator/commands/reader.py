import logging


class Reader:
    PLUGIN_NAME = "dtcd_simple_math_core"
    SWT_BASE_PATH = "SWT"
    FORMAT = "JSON"
    TICK_COLUMN = "_t"

    log = logging.getLogger(PLUGIN_NAME)

    @classmethod
    def read(cls, swt_name):
        complete_line = f'readFile format={cls.FORMAT} path={cls.SWT_BASE_PATH}/{swt_name}'
        cls.log.debug(f"Read otl: {complete_line}")
        return complete_line

    @classmethod
    def read_last_row(cls, swt_name):
        base_read_line = cls.read(swt_name)
        limit_line = "tail 1"
        complete_line = " | ".join((base_read_line, limit_line))
        cls.log.debug(f"Read otl: {complete_line}")
        return complete_line

    @classmethod
    def read_tick(cls, swt_name, tick):
        base_read_line = cls.read(swt_name)
        filter_line = f"search {cls.TICK_COLUMN}={tick}"
        complete_line = " | ".join((base_read_line, filter_line))
        cls.log.debug(f"Read otl: {complete_line}")
        return complete_line
