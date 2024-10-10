from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, AvailabilityViewSet

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinics')
router.register(r'availabilities', AvailabilityViewSet, basename='availabilities')

urlpatterns = [
    path('', include(router.urls)),
]
