from    rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view): #override
        is_admin = super().has_permission(request, view) #is admin
        print("admin= ")
        print(is_admin)
        #print("safe =" + request.method)
        #print(request.method in permissions.SAFE_METHODS)
        return request.method in permissions.SAFE_METHODS or is_admin #dà permessi per metodi di lettura(SAFE_METHODS) anche per chi non è admin


class IsOwnProfileOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        is_mine=False
        if request.method in permissions.SAFE_METHODS:  # getlist...
            return True

        is_mine = obj.user == request.user #obj.user_profile == request.user.profile
        print("own profile =")
        print(is_mine) 
        return  is_mine  #or request.method in permissions.SAFE_METHODS