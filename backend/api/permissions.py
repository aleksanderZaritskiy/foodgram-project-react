from rest_framework import permissions


class IsAllowAnyOrReadUserProfile(permissions.BasePermission):
    """Права для djoser эндпоинтов users/me, users/, users/{id}"""

    def has_permission(self, request, view):
        return (
            request.path == '/api/users/me/'
            or request.user.is_authenticated
        )


class IsAnyReadUserPostorAuthorUpdateRecipePermissions(
    permissions.BasePermission
):
    """Права для рецептов, редактировать и удалять может только автор"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return any(
            (
                request.method in permissions.SAFE_METHODS,
                (request.method == ['POST'] and request.user.is_authenticated),
                request.user == obj.author,
            )
        )
