from django.urls import path, include
from rest_framework.routers import DefaultRouter

from password_policy import views

router = DefaultRouter()
router.register('', views.passwordPolicyViewSet)

app_name = 'password_policy'

urlpatterns = [
    path('', include(router.urls))
]