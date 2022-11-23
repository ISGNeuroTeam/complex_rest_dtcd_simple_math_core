from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from translator.swt import SourceWideTable
from translator.graph import Graph


class GraphHandler(APIView):
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        swt_name = request.data['swt_name']
        graph = request.data['graph']

        _graph = Graph(graph, swt_name)
        new_graph = _graph.new_iteration()

        return SuccessResponse(
            {
                'swt_name': swt_name,
                'graph': new_graph,
            })

    @staticmethod
    def get(request):
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
                    'graph': graph,
                })

    pass
