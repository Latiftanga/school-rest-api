from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """School admin user priviledges"""

    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        return user.is_admin


class IsSuper(BasePermission):
    """Super user priviledges"""
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_superuser


class IsTeacher(BasePermission):
    """School teacher user priviledges"""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_teacher


class IsStudent(BasePermission):
    """School student user priviledges"""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_student


class IsGuardian(BasePermission):
    """School guardian user priviledges"""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_guardian


class IsUser(BasePermission):
    """School guardian user priviledges"""

    def has_permission(self, request, view):
        return request.user.is_authenticated
