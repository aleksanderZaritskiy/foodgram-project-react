from rest_framework import permissions


class GreateOrUpdateOrReadOnlyRecipePermissions(permissions.BasePermission):
    """Права для рецептов, редактировать и удалять может только автор"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            or request.user == obj.author
        )
