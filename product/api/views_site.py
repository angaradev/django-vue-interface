from rest_framework import generics
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from product.forms import KeyWordForm
import operator
import json
from django.core import serializers
from functools import reduce
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q, Count
from product.models import (Product,
                            Units,
                            CarModel,
                            CarEngine,
                            ProductImage,
                            ProductVideos,
                            Category,
                            ProductDescription,
                            ProductAttribute,
                            ProductAttributeName)
from brands.models import BrandsDict
from product.api.serializers_site import (

    CategoryTreeSerializer,
    CategoryFirstLevelSerializer,
    MpttTestSerializer,
    GetSingleProductSerializer
)
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .helpers import modify_input_for_multiple_files
from rest_framework.permissions import AllowAny


# class CategoriesTreeList(generics.ListCreateAPIView):
#     '''

#     Recursive version

#     API View for category Tree view
#     recursively making json
#     It reseives all categories
#     '''
#     query = Q(id__gte=1, id__lte=20)
#     queryset = Category.objects.filter(query).exclude(parent__isnull=True).order_by('id')
#     serializer_class = CategoryTreeSerializer
#     permission_classes = [AllowAny]

class CategoriesTreeList(generics.ListCreateAPIView):
    '''
    No Recursive for now
    API View for category Tree view
    recursively making json
    It reseives all categories
    '''
    serializer_class = MpttTestSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        '''
        Here is sample of add_relative_count
        '''
        queryset = Category.objects.add_related_count(
            Category.objects.get(id=1).get_children(),  # Queryset
            Product,  # Related model
            'category',  # Name of the foreignkey field
            'some_count',  # Name of the property added to the collection
            cumulative=True)  # Cumulative or not.

        anc = queryset.get_ancestors(include_self=True)

        return queryset


class CategoriesListFirstLevel(generics.ListCreateAPIView):
    '''
    API View for category Tree view
    returns first level of categories
    '''
    query = Q(id__gte=1, id__lte=20)
    queryset = Category.objects.filter(query).exclude(
        parent__isnull=True).order_by('id')
    serializer_class = CategoryFirstLevelSerializer
    permission_classes = [AllowAny]


class MpttTest(generics.ListCreateAPIView):
    '''
    API View for category Tree view
    returns first level of categories
    '''
    serializer_class = MpttTestSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        query = Q(id__gte=1000, id__lte=2000)
        queryset = Category.objects.filter(id=1).exclude(
            parent__isnull=True).order_by('id')
        des = queryset.get_descendants(include_self=False)
        anc = queryset.get_ancestors(include_self=True)

        return des


class SingleProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = GetSingleProductSerializer
    permission_classes = [AllowAny]
