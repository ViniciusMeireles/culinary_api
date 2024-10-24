from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class RecipePermission(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (request.user.is_authenticated and obj.chef.user_id == request.user.id)
