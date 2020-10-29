from rest_framework import generics
from .serializers import CategoriesSerializer, DepthOneCategorySerializer
from test_category.models import Categories
from rest_framework.permissions import AllowAny


class CategoriesView(generics.ListAPIView):
    serializer_class = CategoriesSerializer
    paginator = None
    permission_classes = [AllowAny]

    def get_queryset(self):

        queryset = Categories.objects.all()
        depth = int(self.request.GET.get("depth"))
        print(depth)
        if depth and (depth == 1):
            self.serializer_class = DepthOneCategorySerializer
            return queryset.filter(level__lte=depth)
        elif depth and (depth == 2):
            """
            Need to refactor or delete at all
            """
            return queryset

        else:
            return queryset
