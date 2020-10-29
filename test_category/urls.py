from django.urls import path, include
from test_category.api import views


urlpatterns = [
    path("categories/", views.CategoriesView.as_view(), name="cat-test"),
    path(
        "category/<slug:slug>/",
        views.SingleCategorySlugView.as_view(),
        name="cat-test-slug",
    ),
]
