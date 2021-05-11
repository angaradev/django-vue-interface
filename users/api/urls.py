from django.urls import path
from users.api.views import CurrentUserAPIVeiw, CustomObtainAuthToken


urlpatterns = [
    path("user/", CurrentUserAPIVeiw.as_view(), name="current-user"),
    path("authenticate/", CustomObtainAuthToken.as_view(), name="current-user"),
]
