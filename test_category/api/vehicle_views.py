from rest_framework import generics
from rest_framework.permissions import AllowAny
from test_category.models import Years, Vehicle, Makes
from test_category.api.vehicle_serializers import YearsSerializer


class YearsView(generics.ListAPIView):
    # queryset = Categories.objects.all()
    queryset = Years.objects.all()
    serializer_class = YearsSerializer
    paginator = None
    permission_classes = [AllowAny]
