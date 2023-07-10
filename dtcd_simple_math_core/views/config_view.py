# -*- coding: utf-8 -*-
"""Module to return configuration of the plugin view"""
# pylint: disable=import-error, too-few-public-methods
import logging

from rest.views import APIView
from rest.permissions import AllowAny
from rest.response import SuccessResponse
from ..settings import SETTINGS_FILE_PATH


class ConfigView(APIView):
    """
    Endpoint for config.
    It provides config information about plugin in a situation when you can't get logs
    """
    PLUGIN_NAME = "dtcd_simple_math_core"
    log = logging.getLogger(PLUGIN_NAME)

    http_method_names = ['get']
    permission_classes = (AllowAny,)

    def get(self):
        """Receives nothing

        Returns: configuration of the plugin based on a settings.py"""

        result = {
            'logger': {
                'name': str(self.log.name),
                'level': str(self.log.level),
                'handlers': str(self.log.handlers)
            },
            'settings_file_path': str(SETTINGS_FILE_PATH)
        }

        return SuccessResponse(result)
