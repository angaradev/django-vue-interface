from django.urls import path, include, re_path
from product.api import views as productApiViews
from rest_framework.routers import DefaultRouter

from .views import ImageViewSet, VideoViewSet
router = DefaultRouter()
router.register(r'images', ImageViewSet)
router.register(r'videos', VideoViewSet)

urlpatterns = [
    #path('', TemplateView.as_view(template_name='index1.html')),
    # Prefix in browser api/product/
    path('', include(router.urls)),
    path('detail/<int:pk>/', productApiViews.DetailGet.as_view(), name='api-product-detail'),
    path('detailcreate/', productApiViews.CreateNewProduct.as_view(), name='create-new-product'),
    path('selectlistunits/', productApiViews.SelectFieldsUnitsView.as_view(), name='api-select-unit-list'),
    path('selectlistbrands/', productApiViews.SelectFieldsBrandsView.as_view(), name='api-select-brand-list'),
    path('selectlistcarmodel/<int:pk>/', productApiViews.SelectFieldsModelsView.as_view(), name='api-select-carmodel-list'),
    path('selectlistcarmodelnew/', productApiViews.SelectNewProductModelsView.as_view(), name='api-select-carmodel-new-list'),
    path('selectlistcarengine/', productApiViews.SelectFieldsEnginesView.as_view(), name='api-select-carengine-list'),
    path('session/', productApiViews.SetSession.as_view(), name='set-session'),
    ]

   