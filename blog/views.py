from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import Post, Categories
from .serializers import BlogPostSerializer, CategorySerializer, PartCategorySerializer, CategorySerializerOnly
from rest_framework.permissions import AllowAny


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Get blog post 
    '''
    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        limit = self.request.GET.get('limit')
        if limit:
            return self.queryset.all().order_by('-date')[:int(limit)]

        return self.queryset


class BlogCategoryView(ListAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializerOnly
    permission_classes = [AllowAny]
