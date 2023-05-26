import logging

from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from dtcd_simple_math_core.translator.test_graph import Graphy as Graph


class GraphHandler(APIView):
    """
    Endpoint for graph.
    It provides update SWT by new expressions in graph and a merged graph with a linked SWT last row.
    """
    PLUGIN_NAME = "dtcd_simple_math_core"
    log = logging.getLogger(PLUGIN_NAME)

    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Updates a linked SWT and merges executed calculations with an incoming graph. Returns it.

        :param request: Consists of a "swt_name" (a graph fragment name) and a "graph" body in a JSON format.
        :return:
        """
        filename = request.data['swt_name']
        graph_dict = request.data['graph']

        try:
            graph = Graph(filename, graph=graph_dict)
            graph.calc()
        except Exception as e:
            # TODO Add logging of a caught  exception.
            return ErrorResponse(
                {
                    'message': str(e)
                }
            )

        return SuccessResponse(
            {
                'swt_name': filename,
                'graph': graph.dictionary,
            })

    @staticmethod
    def get(request):
        """
        Returns a saved graph fragment by its name.
        :param request: Consists of a "swt_name" (a graph fragment name)
        :return:
        """
        filename = request.GET.get("swt_name", None)
        if filename is None:
            return ErrorResponse(
                {
                    'message': 'A source wide table name is required'
                }
            )
        else:

            graph = Graph.read_from_file(filename)
            return SuccessResponse(
                {
                    'swt_name': filename,
                    'graph': graph.dictionary,
                })
