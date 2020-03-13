from django.urls import path, include, re_path
from product.api import views as productApiViews


urlpatterns = [
    #path('', TemplateView.as_view(template_name='index1.html')),
    # Prefix in browser api/product/
    path('detail/<int:pk>/', productApiViews.DetailGet.as_view(), name='api-product-detail'),
    path('detailcreate/', productApiViews.DetailPost.as_view(), name='api-product-detail'),
    ]