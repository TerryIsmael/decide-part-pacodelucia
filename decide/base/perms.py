from rest_framework import permissions

from base import mods


class UserIsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.auth:
            return False
        response = mods.post('authentication/getuser', json={'token': request.auth.key},
                response=True)
        return response.json().get('is_staff', False)
    
class UserIsAdminToken(permissions.BasePermission):
    def has_permission(self, request, view):
        sessionid = request.COOKIES.get('sessionid', '')
        if sessionid == None or sessionid == '':
            return False
        response = mods.post('authentication/admin-auth', json={'sessionid': sessionid},
                response=True, headers = {'Content-Type': 'application/json'})
        return response.status_code == 200
        
    

