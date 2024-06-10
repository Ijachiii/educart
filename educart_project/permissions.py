from rest_framework.permissions import BasePermission

class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return request.user.is_authenticated

        return request.user.is_staff
    

class IsStaffOrPostOnly(BasePermission):

    def has_permission(self, request, view):
        
        if request.method in ('POST', "PATCH", "PUT", 'HEAD', 'OPTIONS'):
            return True

        return request.user.is_staff