from rest_framework import permissions
from rest_framework.views import Request, View

from .models import User


class IsEmployee(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated and request.user.is_employee:
                return True
            return request.user.is_authenticated and request.user == obj

        return request.user.is_authenticated and request.user.is_employee


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return request.user == obj
