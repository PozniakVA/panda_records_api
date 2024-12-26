from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_staff
        )


class IsAdminUserOrCreateOnly(BasePermission):
    """"
    Requires admin or only allowed to create
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        if request.method in SAFE_METHODS or request.method in ["DELETE", "PATCH"]:
            return request.user.is_staff

        return False
