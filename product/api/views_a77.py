from collections import defaultdict
from rest_framework.decorators import action
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from product.api.serializers_a77 import (
    CategoriesSerializerfFlat,
)
from product.models import Category, Product
from rest_framework.permissions import AllowAny
from django.db.models import Count


class CategoriesView(generics.ListAPIView):
    # queryset = Categories.objects.all()
    queryset = Category.objects.add_related_count(
        Category.objects.all(), Product, "category", "count", cumulative=True
    )

    serializer_class = CategoriesSerializerfFlat  # CategoriesSerializer
    # paginator = None
    permission_classes = [AllowAny]

    def get_queryset(self):

        depth = self.request.GET.get("depth")
        if depth and (depth == "1"):
            self.serializer_class = DepthOneCategorySerializer
            return self.queryset.filter(level__lte=0)

        else:
            return self.queryset.all()
