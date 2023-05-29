from rest.urls import path
from cache import cache_page
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
