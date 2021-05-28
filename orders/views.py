from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Orders
from .serializers import OrderSerializer
from rest_framework.response import Response
from users.models import AutoUser, CustomUser


class OrderAPIView(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    paginator = None

    def list(self, request, *args, **kwargs):
        user = request.GET.get("user", None)
        autouser = request.GET.get("autouser", None)

        queryset = self.queryset
        try:
            if user:
                queryset = self.queryset.filter(user=CustomUser.objects.get(id=user))
            elif autouser:
                queryset = self.queryset.filter(
                    autouser=AutoUser.objects.get(id=autouser)
                )

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                "Orders for that usern is not exists yet",
                status=status.HTTP_404_NOT_FOUND,
            )
