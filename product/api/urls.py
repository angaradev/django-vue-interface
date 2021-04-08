from django.urls import path, include, re_path
from product.api import views as productApiViews
from product.api import views_site as sitetApiViews
from rest_framework.routers import DefaultRouter
from product.api import views_react as RedApiViews
from .views import (
    ImageViewSet,
    VideoViewSet,
    DescriptionViewSet,
    ProductAttributeViewSet,
    ProductAttributeList,
)
from product.api import views_a77
from product.api.views_elastic_v1 import send_json
from product.api.views_elastic_search_api import autocomplete, send_json as search_api

router = DefaultRouter()
router.register(r"images", ImageViewSet)
router.register(r"videos", VideoViewSet)
router.register(r"description", DescriptionViewSet)
router.register(r"attribute", ProductAttributeViewSet)
router.register(r"attributes", ProductAttributeList)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index1.html')),
    # Prefix in browser api/product/
    path("", include(router.urls)),
    path(
        "detail/<int:pk>/",
        productApiViews.DetailGet.as_view(),
        name="api-product-detail",
    ),
    path(
        "related/<int:pk>/",
        productApiViews.ProductRelatedGetPutDelete.as_view(),
        name="api-product-related",
    ),
    path("list/", productApiViews.ProductList.as_view(), name="api-product-list"),
    path(
        "detailcreate/",
        productApiViews.CreateNewProduct.as_view(),
        name="create-new-product",
    ),
    path(
        "selectlistunits/",
        productApiViews.SelectFieldsUnitsView.as_view(),
        name="api-select-unit-list",
    ),
    path(
        "selectlistbrands/",
        productApiViews.SelectFieldsBrandsView.as_view(),
        name="api-select-brand-list",
    ),
    path(
        "selectlistcarmodel/<int:pk>/",
        productApiViews.SelectFieldsModelsView.as_view(),
        name="api-select-carmodel-list",
    ),
    path(
        "selectpartcarmodel/",
        productApiViews.getPartCarModel.as_view(),
        name="api-select-carmodel-one",
    ),
    path(
        "selectpartcarengine/",
        productApiViews.getPartCarEngine.as_view(),
        name="api-select-carengine-one",
    ),
    path(
        "selectlistcarmodelnew/",
        productApiViews.SelectNewProductModelsView.as_view(),
        name="api-select-carmodel-new-list",
    ),
    path(
        "selectlistcarengine/",
        productApiViews.SelectFieldsEnginesView.as_view(),
        name="api-select-carengine-list",
    ),
    path("session/", productApiViews.SetSession.as_view(), name="set-session"),
    #     path('mainimage/<int:pk>/',
    #          productApiViews.ImageMainSet.as_view(), name='main-image'),
    # front end site starts here,
    path(
        "categorytree/",
        sitetApiViews.CategoriesTreeList.as_view(),
        name="category-tree-serializer",
    ),
    path(
        "categoryfirst/",
        sitetApiViews.CategoriesListFirstLevel.as_view(),
        name="category-first-serializer",
    ),
    path("mptt-test/", sitetApiViews.MpttTest.as_view(), name="mptt-test-serializer"),
    path(
        "singleproduct/<int:pk>/",
        sitetApiViews.SingleProduct.as_view(),
        name="single-product-retrive",
    ),
    path(
        "onec/<int:pk>/",
        sitetApiViews.SingleProductC.as_view(),
        name="single-product-retrivec",
    ),
    path(
        "getcarmodelsite/<int:pk>/",
        sitetApiViews.GetCarModel.as_view(),
        name="get-car-model-site",
    ),
    path(
        "getcarmodelsiteall/",
        sitetApiViews.GetCarModelList.as_view(),
        name="get-car-model-list-site",
    ),
    path(
        "getcarmakes/",
        sitetApiViews.GetCarMakes.as_view(),
        name="get-car-makes-list-site",
    ),
    path(
        "analogs/<int:pk>/",
        sitetApiViews.ProductAnalogList.as_view(),
        name="get-analogs",
    ),
    path(
        "relatedsite/<int:pk>/",
        sitetApiViews.ProductRelatedListView.as_view(),
        name="get-relatedsite",
    ),
    # Here starts urls for RedParts site
    # Namespase starts with red
    path(
        "red/singleproduct/<slug:slug>/",
        RedApiViews.RedSingleProductAPI.as_view(),
        name="red-single-product-retrive",
    ),
    ### Starts urls for a77
    path("a77categories/", views_a77.CategoriesView.as_view(), name="cat-test"),
    ### Path for select category by slug for a77
    path(
        "a77category/<slug:slug>/",
        views_a77.SingleCategorySlugView.as_view(),
        name="cat-test-slug",
    ),
    path("jsontest", send_json, name="send_json"),
    path("searchapi", search_api, name="searchapi"),
    path("autocomplete", autocomplete, name="autocomplete"),
]
