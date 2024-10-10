from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


class IsOwner(permissions.BasePermission):
    _("""
     Permission to only allow the owner of an object to view or edit it.
    """)

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsDoctor(permissions.BasePermission):
    _("""
    Custom permission to only allow doctors to access certain views.
    """)

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor
