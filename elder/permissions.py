from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print("in permissions1 : ",request.user.id)
        # print("in permissions other1 : ",obj.id)
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        return obj.id == request.user.id

class UpdateOwnProfilePat(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("in permissions2 : ",str(request.user.email))
        print("in permissions other2 : ",str(obj.patrel).split("- ")[1])
        if request.method in permissions.SAFE_METHODS or request.method=='POST':
            print("Done")
            return True
        return str(obj.patrel).split("- ")[1].strip() == str(request.user.email)

class UpdateOwnProfileMed(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # print("in permissions3 : ",request.user.email)
        # print("in permissions other3 : ",obj.medstaff)
        # print(str(obj.medstaff) == str(request.user.email))
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        return str(obj.medstaff) == str(request.user.email)