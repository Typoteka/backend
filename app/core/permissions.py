from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, _view):
        return request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            return obj.owner == request.user

        return False
