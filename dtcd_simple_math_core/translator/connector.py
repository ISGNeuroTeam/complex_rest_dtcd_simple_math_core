import logging

from ot_simple_connector.connector import Connector


class OTSimpleConnector:
    CACHE_TTL = 5
    log = logging.getLogger('dtcd_simple_math_core')

    def __init__(self, config_connector: []) -> None:
        """
        this is how connector_config must look like:
        connector_config = {"host": "s-dev-2.dev.isgneuro.com",
                            "port": "6080",
                            "user": "admin",
                            "password": "12345678"}
        it is usually set in *.conf file and saved for usage in settings.py
        """
        self.log.debug(f'Input {config_connector=}')
        self.connector = Connector(**config_connector)

    def create_query_job(self, query: str) -> list:
        self.log.debug(f'input: {query}')
        result = self.connector.jobs.create(query, cache_ttl=self.CACHE_TTL).dataset.load()
        self.log.debug(f'result: {result}')
        return result
