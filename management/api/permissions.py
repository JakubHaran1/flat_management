from rest_framework.permissions import BasePermission


class LandlordPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update']:
            return request.user.is_landlord
        return True
