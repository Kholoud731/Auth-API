from rest_framework.permissions import BasePermission

class Can_delete(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name="delete"):
            return True
        return False