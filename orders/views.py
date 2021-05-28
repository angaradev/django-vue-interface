from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Orders
from .serializers import OrderSerializer


class OrderAPIView(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    paginator = None
