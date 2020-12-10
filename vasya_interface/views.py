from django.shortcuts import render
from rest_framework import viewsets
from .models import Rows
from .serializers import RowsSerializer, CheckProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product


class RowsView(viewsets.ModelViewSet):
    model = Rows

    queryset = Rows.objects.all()
    serializer_class = RowsSerializer
    permission_classes = [AllowAny]
    paginator = None


class TestView(generics.ListCreateAPIView):
    queryset = Rows.objects.all()
    serializer_class = RowsSerializer


class CheckProductView(APIView):
    def get(self, request, one_c_id):
        product = Product.objects.get(one_c_id=one_c_id)
        serializer = CheckProductSerializer(product)
        return Response(serializer.data)
