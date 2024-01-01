from rest_framework_roles.roles import is_user, is_anon


def is_super(request, view):
    return is_user(request, view) and request.user.is_superuser


def is_admin(request, view):
    return is_user(request, view) and request.user.is_admin


def is_teacher(request, view):
    return is_user(request, view) and request.user.is_teacher


def is_student(request, view):
    return is_user(request, view) and request.user.is_student


def is_guardian(request, view):
    return is_user(request, view) and request.user.is_guardian


ROLES = {
    'anon': is_anon,
    'user': is_user,
    'super': is_super,
    'admin': is_admin,
    'teacher': is_teacher,
    'student': is_student,
    'guardian': is_guardian
}
