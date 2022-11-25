class Writer:
    SWT_BASE_PATH = "SWT"
    FORMAT = "CSV"

    @classmethod
    def rewrite(cls, swt_name):
        return f'writeFile format={cls.FORMAT} path={cls.SWT_BASE_PATH}/{swt_name}'

    @classmethod
    def append(cls, swt_name):
        return f'writeFile format={cls.FORMAT} mode=append path={cls.SWT_BASE_PATH}/{swt_name}'
