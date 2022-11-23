from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from translator.swt import SourceWideTable


class SourceWideTableHandler(APIView):
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        swt_name = request.data['swt_name']
        graph = request.data['graph']

        swt = SourceWideTable(swt_name)
        swt = swt.new_iteration(graph)

        # do some logic here
        return SuccessResponse(
            {
                'swt_name': swt_name,
                'swt_body': swt,

            })
    pass

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
            swt = SourceWideTable(swt_name)
            table = swt.read()
            return SuccessResponse(
                {
                    'table': table
                })

    pass
