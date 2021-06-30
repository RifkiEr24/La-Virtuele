from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.is_superuser

class IsActive(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_active)

class IsActiveOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (request.user and request.user.is_active)
