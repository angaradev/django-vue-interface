from django.shortcuts import render
from rest_framework import viewsets
from .models import Rows
from .serializers import RowsSerializer, CheckProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product


class RowsView(viewsets.ModelViewSet):
    model = Rows

    queryset = Rows.objects.filter(isDone=False)
    # queryset = Rows.objects.all()
    serializer_class = RowsSerializer
    permission_classes = [AllowAny]
    paginator = None


class RowsViewDone(viewsets.ModelViewSet):
    model = Rows

    # queryset = Rows.objects.filter(isDone=False)
    queryset = Rows.objects.filter(isDone=True)
    serializer_class = RowsSerializer
    permission_classes = [AllowAny]
    paginator = None


class TestView(generics.ListCreateAPIView):
    queryset = Rows.objects.all()
    serializer_class = RowsSerializer


class CheckProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, one_c_id):
        try:
            product = Product.objects.get(one_c_id=one_c_id)
            serializer = CheckProductSerializer(product)
            return Response(serializer.data)
        except:
            return Response(
                {"Fail": "Product with that One C ID not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CheckMadeFoldersView(APIView):

    # 1. Make list of all folders
    # 2. Make list of all products
    # 3. Make list of not done products

    permission_classes = [AllowAny]

    def get(self, request):
        def getDonePhotos():
            # Scan all folders for make list
            parts_list = []
            for foldOne in os.listdir:
                print(foldOne)

        # try:
        # queryset = Product.objects.all()

        # product = Product.objects.filter(have_photo=True)
        have_photo_list = []
        product = Product.objects.all()
        for prod in product:
            if prod.have_photo:
                have_photo_list.append(prod)
        print(have_photo_list)

        serializer = CheckProductSerializer(product)
        return Response(serializer.data)
        # except:
        #     return Response(
        #         {"Fail": "Product with that One C ID not found"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
