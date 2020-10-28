from django.urls import path, include
from test_category.api import views


urlpatterns = [
    path("categories/", views.CategoriesView.as_view(), name="cat-test"),
]
