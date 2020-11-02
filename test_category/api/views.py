from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .serializers import (
    CategoriesSerializer,
    DepthOneCategorySerializer,
    NoRecursionCategorySerializer,
)
from test_category.models import Categories, Product
from rest_framework.permissions import AllowAny
from .serializers_product import ProductSerializer


class CategoriesView(generics.ListAPIView):
    serializer_class = CategoriesSerializer
    paginator = None
    permission_classes = [AllowAny]

    def get_queryset(self):

        queryset = Categories.objects.all()
        depth = int(self.request.GET.get("depth"))
        if depth and (depth == 1):
            self.serializer_class = DepthOneCategorySerializer
            return queryset.filter(level__lte=0)
        elif depth and (depth == 2):
            """
            Need to refactor or delete at all
            """
            return queryset

        else:
            return queryset


class SingleCategorySlugView(generics.RetrieveAPIView):
    queryset = Categories.objects.all()
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        q = Categories.objects.add_related_count(
            self.queryset.exclude(reverse_categories__isnull=True),
            Product,
            "categories",
            "count",
            cumulative=True,
        )
        for item in q:
            print(item.count, item.name, item.level)
        return q


class SingleCategorySlugFlatView(generics.RetrieveAPIView):
    queryset = Categories.objects.all()
    lookup_field = "slug"
    serializer_class = NoRecursionCategorySerializer
    permission_classes = [AllowAny]


class SingleProductView(viewsets.ReadOnlyModelViewSet):
    """
    Class Set for getting single product or set of products
    to show on category pages by category slug
    If no products in category dont pick up them
    """

    queryset = Product.objects.all()
    lookup_field = "slug"
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    paginator = None

    def get_queryset(self):
        category = self.request.GET.get("category")
        if category:
            queryset = self.queryset.filter(
                categories__in=Categories.objects.filter(slug=category).get_descendants(
                    include_self=True
                )
            )
            return queryset
        return self.queryset
