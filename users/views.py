from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsOwner
from .models import Doctor, Patient
from .serializers import DoctorSerializer, DoctorManagementSerializer, PatientSerializer


class DoctorListAPIView(ListAPIView):
    """
        List all doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]

class DoctorManagementCreateAPIView(CreateAPIView):
    """
       Create a new doctor.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorManagementSerializer
    permission_classes = [AllowAny]

class DoctorManagementUpdateAPIView(UpdateAPIView):
    """
       Update a doctor.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorManagementSerializer
    permission_classes = [JWTAuthentication, IsOwner]

class DoctorManagementDestroyAPIView(DestroyAPIView):
    """
       Delete a doctor.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorManagementSerializer
    permission_classes = [JWTAuthentication, IsAdminUser]

class PatientListAPIView(ListAPIView):
    """
        List all items.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsOwner]

class PatientCreateAPIView(CreateAPIView):
    """
        Create a new item.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]

class PatientUpdateAPIView(UpdateAPIView):
    """
       Update a patient.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [JWTAuthentication, IsOwner]

class PatientDestroyAPIView(DestroyAPIView):
    """
       delete a patient.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [JWTAuthentication, IsAdminUser]
