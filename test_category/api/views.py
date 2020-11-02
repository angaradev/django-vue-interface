from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .serializers import (
    CategoriesSerializer,
    DepthOneCategorySerializer,
    # NoRecursionCategorySerializer,
)
from test_category.models import Categories, Product
from rest_framework.permissions import AllowAny
from .serializers_product import ProductSerializer
from django.db.models import Count


class CategoriesView(generics.ListAPIView):
    queryset = Categories.objects.add_related_count(
        Categories.objects.all(), Product, "categories", "count", cumulative=True
    )

    serializer_class = CategoriesSerializer
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
    queryset = Categories.objects.all()
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     q = Categories.objects.add_related_count(
    #         self.queryset,
    #         Product,
    #         "categories",
    #         "count",
    #         cumulative=True,
    #     )
    #     for item in q:
    #         print(item.count, item.name, item.level)
    #     return q
    # def get_queryset(self):

    #     count_queryset = Categories.objects.add_related_count(
    #         self.queryset, Product, "categories", "count", cumulative=True
    #     )
    #     zerros = [x.id for x in count_queryset if x.count == 0]
    #     return self.queryset.exclude(id__in=zerros)


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
