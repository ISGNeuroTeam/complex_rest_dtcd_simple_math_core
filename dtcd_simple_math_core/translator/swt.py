import json

import logging
from ot_simple_connector.connector import Connector
from dtcd_simple_math_core.translator.commands.reader import Reader
from dtcd_simple_math_core.translator.commands.writer import Writer
from dtcd_simple_math_core.translator.commands.eval import Eval


class SourceWideTable:
    PLUGIN_NAME = "dtcd_simple_math_core"
    CONNECTOR_CONFIG = {"host": "s-dev-2.dev.isgneuro.com",
                        "port": "6080",
                        "user": "admin",
                        "password": "12345678"}

    CACHE_TTL = 5
    log = logging.getLogger(PLUGIN_NAME)

    def __init__(self, swt_name):
        self.swt_name = swt_name
        self.connector = Connector(**self.CONNECTOR_CONFIG)

    def _query(self, query):
        return self.connector.jobs.create(query, cache_ttl=self.CACHE_TTL).dataset.load()

    def read(self):
        query = Reader.read(self.swt_name)
        swt = self._query(query)
        return swt

    def read_last_row(self):
        query = Reader.read_last_row(self.swt_name)
        swt = self._query(query)
        return swt

    def read_tick(self, tick):
        if tick == 0:
            swt = self.read()
        elif tick == -1:
            swt = self.read_last_row()
        elif tick > 0:
            query = Reader.read_tick(self.swt_name, tick)
            swt = self._query(query)
        else:
            raise Exception(f"Wrong tick: {tick}")
        return swt

    def new_iteration(self, graph):
        # read_query = Reader.read_last_row(self.swt_name)
        read_query = Reader.read(self.swt_name)
        eval_query = Eval.from_graph(graph)
        write_query = Writer.rewrite(self.swt_name)

        # TODO fix the problem with overwriting or switch to append mode
        subquery = f"otloadjob otl={json.dumps(' | '.join((read_query, eval_query)))}"

        query = " | ".join((subquery, write_query))
        self.log.info(f"New iteration query: {query}")
        swt = self.connector.jobs.create(query, cache_ttl=self.CACHE_TTL).dataset.load()
        return swt


