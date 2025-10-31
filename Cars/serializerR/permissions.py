from rest_framework import permissions

class adminorReadonly(permissions.IsAdminUser):
    def has_permission(self,request):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
        
class isOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.api_user == request.user