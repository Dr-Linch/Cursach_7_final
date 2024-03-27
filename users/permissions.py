from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    massage = "You are not allowed to access this actions"

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return request.method in ('GET', 'PUT', 'PATCH', 'DELETE')
        return False


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Проверка пользователя на правообладания
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.pk == request.user.pk
