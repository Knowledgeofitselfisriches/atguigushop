from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # 如果是get请求，不管什么用户都可以给你返回数据
        if request.method in permissions.SAFE_METHODS:
            return True
        # 对应post,delele,update
        # Instance must have an attribute named `owner`.4
        # 如果是同一用户，返回True
        return obj.user == request.user
