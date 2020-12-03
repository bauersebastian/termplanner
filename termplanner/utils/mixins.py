from django.contrib.auth import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


class IsOwnerMixin(UserPassesTestMixin):
    """
    a custom mixin for checking if the user is the owner of an object
    """

    def test_func(self):

        obj = self.get_object()

        if self.request.user == obj.user:
            return True
        else:
            raise PermissionDenied


class IsOwnerOfSemesterModuleMixin(UserPassesTestMixin):
    """
    a custom mixin for checking if the user is the owner of an object
    """

    def test_func(self):

        obj = self.get_object()

        if self.request.user == obj.semestermodule.user:
            return True
        else:
            raise PermissionDenied
