import logging

from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from dtcd_simple_math_core.translator.graph import Graph


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
        :return
        """
        swt_name = request.data['swt_name']
        graph = request.data['graph']

        self.log.info(f"swt_name: {swt_name}")
        self.log.debug(f"graph: {graph}")

        try:
            _graph = Graph(swt_name, graph_dict=graph)
            _graph.new_iteration()
            self.log.debug(f"Updated graph: {_graph.graph_dict}")
            return SuccessResponse({
                    'swt_name': swt_name,
                    'graph': _graph.graph_dict,
                })
        except Exception as e:
            self.log.error("GraphHandler POST exception", exc_info=True)
            return ErrorResponse({'message': str(e)})

    def get(self, request):
        """
        Returns a saved graph fragment by its name.
        :param request: Consists of a "swt_name" (a graph fragment name)
        :return:
        """
        swt_name = request.GET.get("swt_name", None)
        if swt_name is None:
            return ErrorResponse({'message': 'A source wide table name is required'})
        else:
            try:
                graph = Graph.read(swt_name)
                return SuccessResponse({
                    'swt_name': swt_name,
                    'graph': graph.graph_dict,
                })
            except Exception as e:
                self.log.error("GraphHandler GET exception", exc_info=True)
                return ErrorResponse({'message': str(e)})
