import json
import os
from rest.test import APIClient, TestCase
from http import HTTPStatus


class TestView(TestCase):
    def test_post(self):
        client = APIClient()
        parent_folder = os.path.dirname(__file__)
        with open(f'{parent_folder}/resources/graphs/example_2.json', 'r') as f:
            graph_json_example_body = json.loads(f.read())
        response = client.post('/dtcd_simple_math_core/v1/graph/', graph_json_example_body, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
