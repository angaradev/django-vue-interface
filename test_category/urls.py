from django.urls import path, include
from test_category.api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"products", views.SingleProductView)


urlpatterns = [
    path("products/", include(router.urls)),
    path("categories/", views.CategoriesView.as_view(), name="cat-test"),
    path(
        "category/<slug:slug>/",
        views.SingleCategorySlugView.as_view(),
        name="cat-test-slug",
    ),
]
