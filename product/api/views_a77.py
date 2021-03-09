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

from test_category.api.serializers import (
    DepthOneCategorySerializer,
    CategoriesSerializer,
)


class CategoriesView(generics.ListAPIView):
    """
    FLAT-
    This view takes categories in flat fashon only get parent in there
    """

    # queryset = Categories.objects.all()
    queryset = Category.objects.add_related_count(
        Category.objects.filter(parent=1), Product, "category", "count", cumulative=True
    )

    serializer_class = CategoriesSerializerfFlat  # CategoriesSerializer
    paginator = None
    permission_classes = [AllowAny]

    def get_queryset(self):

        depth = self.request.GET.get("depth")
        if depth and (depth == "1"):
            self.serializer_class = DepthOneCategorySerializer
            return self.queryset.filter(level__lte=0)

        else:
            return self.queryset.all()


class SingleCategorySlugView(generics.RetrieveAPIView):

    queryset = Category.objects.add_related_count(
        Category.objects.all(), Product, "category", "count", cumulative=True
    )
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]
