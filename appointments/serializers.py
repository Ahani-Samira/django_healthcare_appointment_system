from rest_framework import serializers
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


class AvailabilitySerializer(serializers.ModelSerializer):
    '''
    AvailabilitySerializer for serializing the availability data of doctors.

     ## Fields:
     - id: Access ID (automatically)
     - doctor: Information about the related doctor
     - clinic: Information about the related clinic
     - start_time: Start time of availability
     - end_Time: End time of availability
     - selectable_time_list: List of selectable times for appointments
 '''
    doctor = DoctorSerializer()
    clinic = ClinicSerializer()

    class Meta:
        model = Availability
        fields = '__all__'


class SelectableTimeListSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    clinic_name = serializers.SerializerMethodField()

    class Meta:
        model = Availability
        fields = ['id', 'doctor', 'clinic_name', 'selectable_time_list']
        read_only_fields = ['id', 'doctor', 'clinic_name']

    def get_clinic_name(self, obj):
        return obj.clinic.name if obj.clinic else None

    def update(self, instance, validated_data):
        instance.selectable_time_list = validated_data.get('selectable_time_list', instance.selectable_time_list)
        instance.save()
        return instance
