import logging

from ..settings import connector, plugin_name
from query import Query


class DataCollector:
    log = logging.getLogger(plugin_name)
    """
    Level of abstraction between SWT and actual data in ExternalData.
    It creates expressions and uses otl connector to exchange data with spark service.
    If in future otl connector or spark service usage changes -
    it must be changed here only, not in swt or graph layer.
    """

    def __init__(self, name):
        self.name = name

    def read_swt(self, last_row: bool) -> list:
        self.log(f'getting swt table {self.name}')
        expression = Query(name=self.name).get_read_expression(last_row=last_row)
        return connector.create_query_job(expression)

    def calc_swt(self, eval_names: [str]) -> list:
        query = Query(name=self.name).get(eval_names=eval_names)

        return connector.create_query_job(query)
