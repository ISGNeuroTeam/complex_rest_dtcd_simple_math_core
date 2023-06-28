"""Usual Django urls module for dtcd_simple_math_core plugin"""
from rest.urls import path  # pylint: disable=import-error
from .views.source_wide_table_view import SourceWideTableView
from .views.graph_view import GraphView

# Use cache_page decorator for caching view

# urlpatterns = [
#     path('example/', cache_page(60 * 15)(ExampleView.as_view())),
# ]

urlpatterns = [
    path('swt/', SourceWideTableView.as_view()),
    path('graph/', GraphView.as_view())
]
