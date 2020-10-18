from django.shortcuts import render

from rest_framework import viewsets
from .models import Post
from .serializers import BlogPostSerializer
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
