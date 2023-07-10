# -*- coding: utf-8 -*-
"""Module to return response for swt request view"""
# pylint: disable=import-error, broad-except, too-few-public-methods
import logging
from typing import Any

from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse, ErrorResponse

from ..translator.swt import SourceWideTable


class SourceWideTableView(APIView):
    """
    Endpoint for Source Wide Table.
    It provides update by an incoming graph and reading a linked table.
    """
    PLUGIN_NAME = "dtcd_simple_math_core"
    log: logging.Logger = logging.getLogger(PLUGIN_NAME)

    http_method_names: list[str] = ['get']
    permission_classes: tuple[Any] = (AllowAny,)

    @staticmethod
    def get(request):
        """
        Receives data about swt in URL.
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

        swt = SourceWideTable(swt_name)
        try:
            table = swt.read()
        except Exception as exception:
            return ErrorResponse(error_message=str(exception))

        return SuccessResponse({'table': table})
