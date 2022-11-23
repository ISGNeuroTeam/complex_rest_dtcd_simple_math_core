from ot_simple_connector.connector import Connector
from translator.commands.reader import Reader
from translator.commands.writer import Writer
from translator.commands.eval import Eval


class SourceWideTable:

    CONNECTOR_CONFIG = {"host": "s-dev-2.dev.isgneuro.com",
                        "port": "6080",
                        "user": "admin",
                        "password": "12345678"}

    CACHE_TTL = 60

    def __init__(self, swt_name):
        self.swt_name = swt_name
        self.connector = Connector(**self.CONNECTOR_CONFIG)

    def read(self):
        query = Reader.read(self.swt_name)
        swt = self.connector.jobs.create(query, cache_ttl=self.CACHE_TTL).dataset.load()
        return swt

    def read_last_row(self):
        query = Reader.read_last_row(self.swt_name)
        swt = self.connector.jobs.create(query, cache_ttl=self.CACHE_TTL).dataset.load()
        return swt

    def new_iteration(self, graph):
        read_query = Reader.read_last_row(self.swt_name)
        eval_query = Eval.from_graph(graph)
        write_query = Writer.rewrite(self.swt_name)
        query = " | ".join((read_query, eval_query, write_query))
        swt = self.connector.jobs.create(query, cache_ttl=self.CACHE_TTL).dataset.load()
        return swt


