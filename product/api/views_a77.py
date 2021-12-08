from collections import defaultdict
from rest_framework.decorators import action
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from product.api.serializers import ProductSerializer
from product.api.serializers_a77 import ProductA77Serializer
from rest_framework import mixins
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
    queryset = Category.objects.add_related_count(  # type: ignore
        Category.objects.filter(parent=1), Product, "category", "count", cumulative=True
    )

    serializer_class = CategoriesSerializerfFlat  # CategoriesSerializer
    paginator = None  # type: ignore
    permission_classes = [AllowAny]

    def get_queryset(self):

        depth = self.request.GET.get("depth")
        if depth and (depth == "1"):
            self.serializer_class = DepthOneCategorySerializer
            return self.queryset.filter(level__lte=0)

        else:
            return self.queryset.all()


class SingleCategorySlugView(generics.RetrieveAPIView, mixins.RetrieveModelMixin):

    queryset = Category.objects.add_related_count(  # type: ignore
        Category.objects.all(), Product, "category", "count", cumulative=True
    )
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]
    model = Product


class GetProductBySlugView(generics.RetrieveAPIView):
    """
    Class retreive single product by slug
    """

    queryset = Product.objects.all()
    lookup_field = "slug"
    serializer_class = ProductA77Serializer
    permission_classes = [AllowAny]


class GetProductsByCatNumbers(APIView):
    """Get all parts by array of cat numbers"""

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """Getting array and serilizing qyeryset"""
        numbers = request.GET.getlist("numbers")
        qs = Product.objects.filter(cat_number__in=numbers)
        serializer = ProductA77Serializer(qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
