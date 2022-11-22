from ot_simple_connector.connector import Connector
from translator.read import Read


class SourceWideTable:

    CONNECTOR_CONFIG = {"host": "s-dev-2.dev.isgneuro.com",
                        "port": "6080",
                        "user": "admin",
                        "password": "12345678"}

    def __init__(self, swt_name):
        self.swt_name = swt_name
        self.connector = Connector(**self.CONNECTOR_CONFIG)

    def read(self):
        query = Read.read(self.swt_name)
        swt = self.connector.jobs.create(query, cache_ttl=60).dataset.load()
        return swt

    def read_last_row(self):
        query = Read.read_last_row(self.swt_name)
        swt = self.connector.jobs.create(query, cache_ttl=60).dataset.load()
        return swt
