from rest.urls import path
from cache import cache_page
from .views.source_wide_table_handler import SourceWideTableHandler
from .views.graph_handler import GraphHandler

# Use cache_page decorator for caching view

# urlpatterns = [
#     path('example/', cache_page(60 * 15)(ExampleView.as_view())),
# ]

urlpatterns = [
    path('swt/', SourceWideTableHandler.as_view()),
    path('graph/', GraphHandler.as_view())
]
