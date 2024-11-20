from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


# 1 for authorized user, but users who are not Admin just can do safety activities
# 2 for loaded data, just including records that associated with them
class IsAuthorized(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if user.is_superuser:
                return True
            else:
                if request.method in permissions.SAFE_METHODS:
                    return True

        return False


class IsUserReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsLectureWriteOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if user.groups.filter(name='lecture').exists():
                return True
            else:
                if request.method in permissions.SAFE_METHODS:
                    return True
                return False
        return False
