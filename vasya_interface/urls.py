from django.urls import path, include, re_path
from .views import RowsView


urlpatterns = [
    path("rows/", RowsView.as_view(), name="rows"),
]
