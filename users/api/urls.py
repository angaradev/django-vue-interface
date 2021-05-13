from django.urls import path, include, re_path
from users.api.views import CurrentUserAPIVeiw, CustomObtainAuthToken

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", CurrentUserAPIVeiw, basename="user")


urlpatterns = [
    # path("user/", CurrentUserAPIVeiw.as_view(), name="current-user"),
    path("", include(router.urls)),
    path("authenticate/", CustomObtainAuthToken.as_view(), name="current-user"),
]
