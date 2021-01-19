"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include

from rest_framework import routers
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from user import views

ROUTER = routers.SimpleRouter(trailing_slash=True)
ROUTER.register(r'', views.UserViewSet, basename='user')

SchemaView = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="Pravin.Tandale@xoriant.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc-old/', SchemaView.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),
    path('admin/', admin.site.urls),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/user/', include(ROUTER.urls)),
    path('api/password_policy/', include('password_policy.urls')),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change_password'),

]
