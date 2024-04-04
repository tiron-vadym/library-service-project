from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission class to check if the current user is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
