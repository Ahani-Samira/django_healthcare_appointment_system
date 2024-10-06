from django.urls import path
from .views import (
    DoctorListAPIView, DoctorManagementCreateAPIView,
    DoctorManagementUpdateAPIView, DoctorManagementDestroyAPIView,
    PatientListAPIView, PatientCreateAPIView,
    PatientUpdateAPIView, PatientDestroyAPIView
)


urlpatterns = [
    path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('doctors/new/', DoctorManagementCreateAPIView.as_view(), name='doctor-create'),
    path('doctors/<int:id>/', DoctorManagementUpdateAPIView.as_view(), name='doctor-update'),
    path('doctors/<int:id>/delete/', DoctorManagementDestroyAPIView.as_view(), name='doctor-delete'),

    path('patients/', PatientListAPIView.as_view(), name='patient-list'),
    path('patients/new/', PatientCreateAPIView.as_view(), name='patient-create'),
    path('patients/<int:pk>/', PatientUpdateAPIView.as_view(), name='patient-update'),
    path('patients/<int:pk>/delete/', PatientDestroyAPIView.as_view(), name='patient-delete'),
]