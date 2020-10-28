from rest_framework import generics
from .serializers import CategoriesSerializer
from test_category.models import Categories
from rest_framework.permissions import AllowAny


class CategoriesView(generics.ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    paginator = None
    permission_classes = [AllowAny]
