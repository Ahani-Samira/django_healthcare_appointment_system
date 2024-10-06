from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Doctor, Patient
from .validators import phone_number_validator


class CustomUserSerializer(serializers.ModelSerializer):
    _('''CustomUserSerializer for serializing and validating user data.

    ## Fields:
    - id: user ID (An automatically generated random UUID)
    - phone_number: user's phone number with validation
    - first_name: User's first name
    - last_name: User's last name
    - date_of_birth: user's date of birth
    - gender: the gender of the user.
    ''')

    phone_number = serializers.CharField(validators=[phone_number_validator])

    class Meta:
        model = CustomUser
        exclude = [
            'slug', 'is_active', 'is_superuser', 'is_staff',
            'groups', 'user_permissions', 'last_login',
        ]
        read_only_fields = ['phone_number', 'slug']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        return make_password(value)


class LimitCustomUserSerializer(serializers.ModelSerializer):
    _('''LimitCustomUserSerializer for serializing and validating some user data.

    ## Fields:
    - id: user ID (An automatically generated random UUID)
    - first_name: User's first name
    - last_name: User's last name
    ''')

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']


class DoctorSerializer(serializers.ModelSerializer):
    _('''DoctorSerializer for viewing Doctor information accessible to all.

       ## Fields:
       - user: Nested serializer for the LimitCustomUser data of the Doctor
       - medical_code: Doctor's medical code
       - specialty: Doctor's specialty
       - photo: Doctor's profile photo
       ''')

    user = LimitCustomUserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'medical_code', 'specialty', 'photo']
        read_only_fields = ['medical_code', 'specialty', 'photo']


class DoctorManagementSerializer(serializers.ModelSerializer):
    _('''DoctorManagementSerializer for managing Doctor information.
    
    ## Fields:
    - user: Nested serializer for the CustomUser data
    - medical_code: Doctor's medical code
    - specialty: Doctor's specialty
    - photo: Doctor's profile photo
    ''')

    user = CustomUserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'medical_code', 'specialty', 'photo']
        read_only_fields = ['medical_code', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        doctor = Doctor.objects.create(user=user_instance, **validated_data)
        return DoctorManagementSerializer(doctor).data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


class PatientSerializer(serializers.ModelSerializer):
    _('''PatientSerializer for managing Patient information.
    
    ## Fields:
    - user: Nested serializer for the CustomUser data
    - insurance_type: Patient's insurance type
    - photo: Patient's profile photo
    ''')

    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = ['user', 'insurance_type', 'photo']
        read_only_fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        patient = Patient.objects.create(user=user_instance, **validated_data)
        return PatientSerializer(patient).data

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
