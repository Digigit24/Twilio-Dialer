"""
Custom permissions for API endpoints.
"""
from rest_framework import permissions


class IsAgent(permissions.BasePermission):
    """
    Permission check for Sales Agent role.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_agent()


class IsManager(permissions.BasePermission):
    """
    Permission check for Manager/Admin role.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_manager()


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Manager can do anything, others can only read.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_manager()


class IsOwnerOrManager(permissions.BasePermission):
    """
    Object owner or manager can access.
    """

    def has_object_permission(self, request, view, obj):
        # Managers can access everything
        if request.user.is_manager():
            return True

        # Check if object has an agent field
        if hasattr(obj, 'agent'):
            return obj.agent == request.user

        # Check if object has an assigned_to field
        if hasattr(obj, 'assigned_to'):
            return obj.assigned_to == request.user

        # Default to user comparison
        return obj == request.user
