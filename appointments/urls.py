from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, AvailabilityViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinics')
router.register(r'availabilities', AvailabilityViewSet, basename='availabilities')
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', include(router.urls)),
]
