from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
     Permission to only allow the owner of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsDoctor(permissions.BasePermission):
    """
    Custom permission to only allow doctors to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor
