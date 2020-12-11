from django.urls import path, include, re_path
from .views import RowsView, RowsViewDone, TestView, CheckProductView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"rows", RowsView)
router.register(r"rowsdone", RowsViewDone)

urlpatterns = [
    path("workingrows/", include(router.urls)),
    path("test/", TestView.as_view(), name="test"),
    path("check/<int:one_c_id>/", CheckProductView.as_view(), name="check"),
]
