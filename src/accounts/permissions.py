from rest_framework import permissions


class IsObjectOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.username == view.kwargs['username'])
