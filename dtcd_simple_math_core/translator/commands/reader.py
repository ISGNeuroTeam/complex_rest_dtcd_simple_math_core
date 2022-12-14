class Reader:
    SWT_BASE_PATH = "SWT"
    FORMAT = "JSON"
    TICK_COLUMN = "_t"

    @classmethod
    def read(cls, swt_name):
        return f'readFile format={cls.FORMAT} path={cls.SWT_BASE_PATH}/{swt_name}'

    @classmethod
    def read_last_row(cls, swt_name):
        base_read_line = cls.read(swt_name)
        limit_line = "tail 1"
        complete_line = " | ".join((base_read_line, limit_line))
        return complete_line

    @classmethod
    def read_tick(cls, swt_name, tick):
        base_read_line = cls.read(swt_name)
        filter_line = f"search {cls.TICK_COLUMN}={tick}"
        complete_line = " | ".join((base_read_line, filter_line))
        return complete_line
