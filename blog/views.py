from django.shortcuts import render

from rest_framework import viewsets
from .models import Post
from .serializers import BlogPostSerializer


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = BlogPostSerializer
