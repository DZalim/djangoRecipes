from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class StaffAndSuperUserPermissions(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return not user.is_anonymous and (user.is_staff or user.is_superuser)

    def handle_no_permission(self):
        raise PermissionDenied("You do not have the required permissions.")


class SameUserPermissions(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user

        if hasattr(self, 'get_object'):
            obj = self.get_object()

            if hasattr(obj, 'user'):
                return not user.is_anonymous and user.id == obj.user.pk

            if hasattr(obj, 'recipe'):
                return not user.is_anonymous and user.id == obj.recipe.user.pk

        return user.id == int(self.kwargs['pk'])

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")


class IsStaffOrSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsSameUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        obj = view.get_object()
        return user.id == obj.user.pk
