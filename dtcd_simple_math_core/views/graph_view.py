import logging

from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from ..translator.graph import Graph


class GraphView(APIView):
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
            graph.initialize()
            graph.calc()
        except Exception as e:
            self.log.error(f'Got an error: {e}')
            return ErrorResponse(error_message=str(e))

        return SuccessResponse({'swt_name': filename, 'graph': graph.dictionary})

    def get(self, request):
        """
        IMPORTANT: Turned out this method is not used in DataCAD. Seem to be deleted soon.

        Returns a saved graph fragment by its name.
        :param request: Consists of a "swt_name" (a graph fragment name)
        :return:
        """
        filename = request.data.get("swt_name", None)
        if filename is None:
            self.log.error(f'Got an error: A source wide table name is required, got None.')
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
