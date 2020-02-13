from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj): #override
        print(obj.author == request.user)
        if request.method in permissions.SAFE_METHODS:  # getlist...
            return True

        return obj.author == request.user 
