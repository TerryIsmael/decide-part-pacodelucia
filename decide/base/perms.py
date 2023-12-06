from rest_framework import permissions

from base import mods


class UserIsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.auth:
            return False
        response = mods.post('authentication/getuser', json={'token': request.auth.key},
                response=True)
        return response.json().get('is_staff', False)

class UserIsStaffOrAdmin(permissions.BasePermission): 

    def has_permission(self, request, view):
        if not request.auth:
            if request.user.is_anonymous:
                return False
            return request.user.is_staff or request.user.is_superuser
        response = mods.post('authentication/getuser', json={'token': request.auth.key},
                response=True)
        return response.json().get('is_staff', False) or response.json().get('is_admin', False)