from product.models import Product, Units, CarModel, CarEngine
from brands.models import BrandsDict
from product.api.serializers import ProductSerializer, UnitsSerializer, BrandsDictSerializer, CarModelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Class to work with detailed product all methods exept
# POST post is right below there


class DetailGet(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailPost(APIView):
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SelectFieldsUnitsView(APIView):
    def get(self, request):
        units_list = Units.objects.all()
        serializer = UnitsSerializer(units_list, many=True)
        return Response(serializer.data)


class SelectFieldsBrandsView(APIView):

    def get(self, request):
        units_list = BrandsDict.objects.all()
        serializer = BrandsDictSerializer(units_list, many=True)
        return Response(serializer.data)

class SelectFieldsModelsView(APIView):

    def get(self, request):
        units_list = CarModel.objects.all()
        serializer = CarModelSerializer(units_list, many=True)
        return Response(serializer.data)
