from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from dtcd_simple_math_core.translator.graph import Graph


class GraphHandler(APIView):
    """
    Endpoint for graph.
    It provides update SWT by new expressions in graph and a merged graph with a linked SWT last row.
    """
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        """
        Updates a linked SWT and merges executed calculations with an incoming graph. Returns it.
        :param request: Consists of a "swt_name" (a graph fragment name) and a "graph" body in a JSON format.
        :return
        """
        swt_name = request.data['swt_name']
        graph = request.data['graph']

        _graph = Graph(swt_name, graph_dict=graph)
        new_graph = _graph.new_iteration()

        return SuccessResponse(
            {
                'swt_name': swt_name,
                'graph': new_graph,
            })

    @staticmethod
    def get(request):
        """
        Returns a saved graph fragment by its name.
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

            graph = Graph.read(swt_name)
            return SuccessResponse(
                {
                    'swt_name': swt_name,
                    'graph': graph.graph_dict,
                })

    pass