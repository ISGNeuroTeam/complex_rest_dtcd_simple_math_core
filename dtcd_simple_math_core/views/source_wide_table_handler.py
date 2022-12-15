import logging
from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from dtcd_simple_math_core.translator.swt import SourceWideTable


class SourceWideTableHandler(APIView):
    """
    Endpoint for Source Wide Table.
    It provides update by an incoming graph and reading a linked table.
    """
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    PLUGIN_NAME = "dtcd_simple_math_core"
    log = logging.getLogger(PLUGIN_NAME)

    def post(self, request):
        """
        Updates a linked SWT by an incoming graph and returns it.

        :param request: Consists of a "swt_name" (a graph fragment name) and a "graph" body in a JSON format.
        :return:
        """
        swt_name = request.data['swt_name']
        graph = request.data['graph']

        self.log.info(f"swt_name: {swt_name}")
        self.log.debug(f"graph: {graph}")

        swt = SourceWideTable(swt_name)
        swt = swt.new_iteration(graph)
        self.log.debug(f"swt: {swt}")
        return SuccessResponse(
            {
                'swt_name': swt_name,
                'swt_body': swt,
            })

    def get(self, request):
        """
        Reads an SWT table and returns it.
        :param request: Keys of request JSON object
            "swt_name" [STRING] a graph fragment name
            "tick" [NUMBER] specified tick or
                -1 last row
                0 whole table
                >0 tick from table
        :return: an SWT table in a JSONL format
        """
        swt_name = request.GET.get("swt_name", None)
        tick = request.GET.get("tick", 0)

        self.log.info(f"swt_name: {swt_name}")
        self.log.info(f"tick: {tick}")

        if swt_name is None:
            return ErrorResponse({'message': 'A source wide table name is required'})
        else:

            swt = SourceWideTable(swt_name)
            table = swt.read_tick(tick)
            self.log.debug(f"table: {table}")
            return SuccessResponse(
                {
                    'table': table
                })

