from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class AnonymousUserPermissions(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_anonymous

    def handle_no_permission(self):
        raise PermissionDenied


class StaffAndSuperUserPermissions(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class SameUserPermissions(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        if hasattr(self, 'get_object') and hasattr(self, 'user'):
            obj = self.get_object()
            return self.request.user.id == obj.user.pk

        return self.request.user.id == int(self.kwargs['pk'])


class SameUserAndStaffOrSuperUserPermissions(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        if hasattr(self, 'get_object') and hasattr(self, 'user'):
            obj = self.get_object()

            return (self.request.user.id == obj.user.pk
                    or self.request.user.is_staff
                    or self.request.user.is_superuser)

        return (self.request.user.id == int(self.kwargs['pk'])
                or self.request.user.is_staff
                or self.request.user.is_superuser)


class IsStaffOrSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsSameUser(BasePermission):

    def has_permission(self, request, view):
        if hasattr(self, 'get_object') and hasattr(self, 'user'):
            obj = self.get_object()
            return self.request.user.id == obj.user.pk

        return self.request.user.id == int(self.kwargs['pk'])
