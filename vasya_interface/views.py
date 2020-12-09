from django.shortcuts import render
from rest_framework import viewsets
from .models import Rows
from .serializers import RowsSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics


class RowsView(viewsets.ModelViewSet):
    model = Rows

    queryset = Rows.objects.all()
    serializer_class = RowsSerializer
    permission_classes = [AllowAny]
    paginator = None


class TestView(generics.ListCreateAPIView):
    queryset = Rows.objects.all()
    serializer_class = RowsSerializer
