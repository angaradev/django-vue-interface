from django.contrib import admin
from django.urls import path, include, re_path

from django_registration.backends.one_step.views import RegistrationView
from django.conf import settings
from django.conf.urls.static import static

from users.forms import CustomUserForm
from core.views import IndexTemplateView
from django.views.generic import TemplateView
from home.views import Home, DocumentationView, React


admin.site.site_header = "Мега Интерфейс"
admin.site.site_title = "Интерфейс"


urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("", Home.as_view(), name="home"),
    path("documentation/", DocumentationView.as_view(), name="documentation"),
    path("admin/", admin.site.urls),
    path(
        "accounts/register/",
        RegistrationView.as_view(
            form_class=CustomUserForm,
            success_url="/",
        ),
        name="django_r",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("django_registration.backends.one_step.urls")),
    path("product/", include("product.urls"), name="product-main"),
    path("api/brands/", include("brands.api.urls")),
    path("api/user/", include("users.api.urls")),
    path("api/product/", include("product.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/rest-auth/", include("rest_auth.urls")),
    path("api/rest-auth/registration/", include("rest_auth.registration.urls")),
    path("branddict/", include("brand_dict.urls")),
    path("blog/", include("blog.urls")),
    path("vasyainterface/", include("vasya_interface.urls")),
    path("companypages/", include("company_pages.urls")),
    # path("testcategory/", include("test_category.urls")),
    path("react/", React.as_view(), name="react"),
    re_path(r"^(?:react.*)/$", React.as_view(), name="react-router"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point")]
