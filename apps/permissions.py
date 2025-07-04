from rest_framework import permissions

class IsOwnerOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Superusers can access all objects.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Superusers can access all objects
        if request.user.is_superuser:
            return True
        # Regular users can only access their own objects
        return obj.user == request.user
