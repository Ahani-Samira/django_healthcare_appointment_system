from rest_framework import serializers
from users.serializers import DoctorSerializer, LimitPatientSerializer
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
        fields = ['id', 'doctor', 'clinic_name', 'start_time', 'end_time', 'selectable_time_list']
        read_only_fields = ['id', 'doctor', 'clinic_name', 'start_time', 'end_time']

    def get_clinic_name(self, obj):
        return obj.clinic.name if obj.clinic else None

    def update(self, instance, validated_data):
        instance.selectable_time_list = validated_data.get('selectable_time_list', instance.selectable_time_list)
        instance.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    '''
    AppointmentSerializer for serializing appointment data.

    ## Fields:
    - id: Access ID (automatically)
    - patient: Information about the related patient
    - availability: Availability details for the appointment
    - selected_time: Selected time for the appointment
    '''

    availability = SelectableTimeListSerializer()
    patient = LimitPatientSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'availability', 'selected_time']
        read_only_fields = ['id', 'patient', 'availability'] 

    def create(self, validated_data):
        availability_data = validated_data.pop('availability')
        appointment = Appointment.objects.create(**validated_data, availability=availability_data)
        return appointment

    def update(self, instance, validated_data):
        instance.selected_time = validated_data.get('selected_time', instance.selected_time)
        instance.save()
        return instance
