from rest_framework.permissions import BasePermission , SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.status == "OWNER"



class IsOwnerforDeleteElseAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method == "DELETE":
            return bool(user and user.is_authenticated and user.status == "OWNER")
        return bool(user and user.is_authenticated)
    