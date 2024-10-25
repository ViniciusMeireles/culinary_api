from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class HisChefPermission(permissions.BasePermission):
    """Permission for only the boss himself to edit"""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (request.user.is_authenticated and obj.user == request.user)
