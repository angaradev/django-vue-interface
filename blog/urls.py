from .views import BlogViewSet
from django.urls import path, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', BlogViewSet)


urlpatterns = [

    path('', include(router.urls), name='blog-viewset'),
]
