from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from users.serializers import DoctorSerializer, DoctorManagementSerializer, PatientSerializer
from .models import Clinic, Availability, Appointment


class ClinicSerializer(serializers.ModelSerializer):
    '''Clinicserializer to serve clinic data.

     ## Fields:
     - id: Clinic ID (automatically)
     - name: Clinic name
     - address: Clinic address
    '''
    class Meta:
        model = Clinic
        fields = '__all__'
