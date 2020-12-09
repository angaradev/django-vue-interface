from django.urls import path, include, re_path
from .views import RowsView, TestView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"rows", RowsView)

urlpatterns = [
    path("workingrows/", include(router.urls)),
    path("test/", TestView.as_view(), name="test"),
]
