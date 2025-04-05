from rest_framework.permissions import BasePermission

class IsAnAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # check if curr user is one of the author(s)
        return request.user in obj.authors.all()
    
class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # check if curr user is the author
        return request.user == obj.author