
from django.urls import path, include, re_path
from product import views as productviews


urlpatterns = [
    #path('', TemplateView.as_view(template_name='index1.html')),
    path('list/<int:pk>/', productviews.Main.as_view(), name='product-list'),
    path('<int:pk>/', productviews.Detail.as_view(), name='product-detail'),
    path('create/', productviews.CreateView.as_view(), name='product-new'),
    path('category/<str:hierarchy>/', productviews.show_category, name='categories'),
    #re_path(r'^category/(?P<hierarchy>.+)/$', productviews.show_category, name='categories'),
    path('locale/', productviews.view_locale,),
]

