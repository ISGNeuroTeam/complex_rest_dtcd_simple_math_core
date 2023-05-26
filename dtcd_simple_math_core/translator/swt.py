import json
import logging

from dtcd_simple_math_core.translator.queries.read import ReadQuery
from dtcd_simple_math_core.translator.queries.write import WriteQuery
from dtcd_simple_math_core.translator.queries.eval import EvalQuery
from dtcd_simple_math_core.settings import plugin_name, connector


class SourceWideTable:
    log = logging.getLogger(plugin_name)

    def __init__(self, swt_name: str, ) -> None:
        self.log.debug(f'Input {swt_name=}')
        self.swt_name = swt_name

    def read(self, last_row: bool = False) -> list:
        query = ReadQuery.get(self.swt_name, last_row=last_row)
        swt = connector.create_query_job(query)
        return swt

    def new_iteration(self, graph_name: str) -> list:
        read_query = ReadQuery.get(self.swt_name)
        eval_query = EvalQuery.get_from_graph(graph_name)
        write_query = WriteQuery.get(self.swt_name)

        subquery = f"otloadjob otl={json.dumps(' | '.join((read_query, eval_query)))}"

        query = " | ".join((subquery, write_query))
        swt = connector.create_query_job(query)
        return swt
