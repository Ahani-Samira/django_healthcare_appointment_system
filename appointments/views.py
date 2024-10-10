from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status,views
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsOwner, IsDoctor
from django.utils.translation import gettext_lazy as _
from .models import Clinic, Availability, Appointment
from .serializers import ClinicSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ClinicViewSet(ViewSet):
    '''ClinicViewSet for managing clinics.'''

    permission_classes_by_action = {
        'list': [IsDoctor | IsAdminUser, IsAuthenticated],
        'create': [IsDoctor | IsAdminUser, IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'update': [IsDoctor | IsAdminUser, IsAuthenticated],
        'partial_update': [IsAdminUser, IsAuthenticated],
        'destroy': [IsAdminUser, IsAuthenticated],
    }

    serializer_class = ClinicSerializer

    def get_permissions(self):
        '''Get permissions based on the action.'''
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [])]

    def get_serializer_class(self):
        '''Get the serializer class based on the action.'''
        return self.serializer_class

    @swagger_auto_schema(
        responses={200: ClinicSerializer(many=True)},
        operation_description=_('Retrieve a list of clinics.')
    )
    def list(self, request):
        '''Retrieve a list of clinics.'''
        clinics = Clinic.objects.all()
        serializer = self.get_serializer_class()
        data = serializer(clinics, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ClinicSerializer,
        responses={
            201: ClinicSerializer,
            400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            })),
        },
        operation_description=_('Create a new clinic.')
    )
    def create(self, request):
        '''Create a new clinic.'''
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            200: ClinicSerializer,
            404: openapi.Response('Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            })),
        },
        operation_description=_('Retrieve a specific clinic by ID.')
    )
    def retrieve(self, request, pk=None):
        '''Retrieve a specific clinic by ID.'''
        clinic = get_object_or_404(Clinic, pk=pk)
        serializer = self.get_serializer_class()(clinic)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ClinicSerializer,
        responses={
            200: ClinicSerializer,
            400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            })),
            404: openapi.Response('Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            })),
        },
        operation_description=_('Update a specific clinic.')
    )
    def update(self, request, pk=None):
        '''Update a specific clinic.'''
        clinic = get_object_or_404(Clinic, pk=pk)
        serializer = self.get_serializer_class()(clinic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ClinicSerializer,
        responses={
            200: ClinicSerializer,
            400: openapi.Response('Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            })),
            404: openapi.Response('Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            })),
        },
        operation_description=_('Partially update a specific clinic.')
    )
    def partial_update(self, request, pk=None):
        '''Partially update a specific clinic.'''
        clinic = get_object_or_404(Clinic, pk=pk)
        serializer = self.get_serializer_class()(clinic, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: openapi.Response('No Content'),
            404: openapi.Response('Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'error': openapi.Schema(type=openapi.TYPE_STRING)
            })),
        },
        operation_description=_('Delete a specific clinic.')
    )
    def destroy(self, request, pk=None):
        '''Delete a specific clinic.'''
        clinic = get_object_or_404(Clinic, pk=pk)
        clinic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
