from django.urls import path, include
from test_category.api import views, vehicle_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"products", views.SingleProductView)


urlpatterns = [
    path("products/", include(router.urls)),
    path("categories/", views.CategoriesView.as_view(), name="cat-test"),
    path(
        "categories-for-testes/",
        views.CategoriesViewForTestes.as_view(),
        name="cat-testes",
    ),
    # get category by slug for red parts categories
    # url is http://localhost:8000/testcategory/category/dvigatel/
    path(
        "category/<slug:slug>/",
        views.SingleCategorySlugView.as_view(),
        name="cat-test-slug",
    ),
    path(
        "years/",
        vehicle_views.YearsView.as_view(),
        name="years",
    ),
    path(
        "vehicle/",
        vehicle_views.VehicleView.as_view(),
        name="vehicles",
    ),
]
