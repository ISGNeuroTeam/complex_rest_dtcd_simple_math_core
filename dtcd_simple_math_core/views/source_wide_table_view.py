import logging

from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from ..translator.swt import SourceWideTable
from ..translator.graph import Graph


class SourceWideTableView(APIView):
    """
    Endpoint for Source Wide Table.
    It provides update by an incoming graph and reading a linked table.
    """
    PLUGIN_NAME = "dtcd_simple_math_core"
    log = logging.getLogger(PLUGIN_NAME)

    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        """
        Updates a linked SWT by an incoming graph and returns it.

        :param request: Consists of a "swt_name" (a graph fragment name) and a "graph" body in a JSON format.
        :return:
        """
        swt_name = request.data['swt_name']
        graph_data = request.data['graph']

        graph = Graph(swt_name, graph=graph_data)
        graph.initialize()
        swt = graph.swt()

        return SuccessResponse(
            {
                'swt_name': swt_name,
                'swt_body': swt,
            })

    @staticmethod
    def get(request):
        """
        Reads an SWT table and returns it.

        :param request: Consists of a "swt_name" (a graph fragment name)
        :return:
        """
        swt_name = request.GET.get("swt_name", None)
        if swt_name is None:
            return ErrorResponse(
                {
                    'message': 'A source wide table name is required'
                }
            )
        else:
            swt = SourceWideTable(swt_name)
            table = swt.read()
            return SuccessResponse(
                {
                    'table': table
                })
