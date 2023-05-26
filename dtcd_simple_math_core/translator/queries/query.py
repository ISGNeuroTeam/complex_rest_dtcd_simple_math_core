import json

from dtcd_simple_math_core.translator.queries.eval import EvalQuery
from dtcd_simple_math_core.translator.queries.read import ReadQuery
from dtcd_simple_math_core.translator.queries.write import WriteQuery


class Query:

    def __init__(self, name: str = None, nodes: [] = None) -> None:
        self.name = name
        self.nodes = nodes

    def get(self) -> str:
        read_query = ReadQuery.get(self.name)
        eval_query = EvalQuery.get_from_graph(self.nodes)
        write_query = WriteQuery.get(self.name)

        # TODO fix the problem with overwriting or switch to append mode
        subquery = f"otloadjob otl={json.dumps(' | '.join((read_query, eval_query)))}"

        result = " | ".join((subquery, write_query))

        return result
