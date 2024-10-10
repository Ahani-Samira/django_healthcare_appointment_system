from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinics')

urlpatterns = [
    path('', include(router.urls)),
]
