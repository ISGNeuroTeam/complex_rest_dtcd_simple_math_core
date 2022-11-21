from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse
from ot_simple_connector.connector import Connector


class SimpleMath(APIView):
    http_method_names = ['post', 'get']
    permission_classes = (AllowAny,)
    connector = Connector(
        host="192.168.4.193",
        port="80",
        user="admin",
        password="12345678"
    )

    def post(self, request):
        body_param1 = request.data['param1']
        body_param2 = request.data['param2']
        # do some logic here
        return SuccessResponse(
            {
                'message': 'Hello world',
                'body_param1': body_param1
            })
    pass

    def get(self, request):
        msg = self.connector.jobs.create("| readFile format=csv path=lamp_simple_math/example_of_swt.csv", cache_ttl=60).dataset.load()

        return SuccessResponse(
            {
                'message': msg
            })

    pass
