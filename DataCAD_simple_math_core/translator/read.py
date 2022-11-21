class Read:
    WST_BASE_PATH = "SWT"
    FORMAT = "CSV"

    @classmethod
    def read(cls, wst_name):
        return f'readFile format={cls.FORMAT} path={cls.WST_BASE_PATH}/{wst_name}'

    @classmethod
    def read_last_row(cls, wst_name):
        base_read_line = cls.read(wst_name)
        limit_line = "tail 1"
        complete_line = " | ".join((base_read_line, limit_line))
        return complete_line
