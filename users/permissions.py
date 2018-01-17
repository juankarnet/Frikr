# -*- coding=utf-8 -*-
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, POST, PUT o DELETE)
        :param request:
        :param view:
        :return:
        """
        # from users.api import UserDetailAPI
        # if request.method == "POST":
        #     return True
        # elif request.user.is_superuser:
        #     return True
        # elif isinstance(view, UserDetailAPI):
        #     return True
        # else:
        #     # GET a /api/1.0/photos/
        #     return False

        if view.action == "create":
            return True
        elif request.user.is_superuser:
            return True
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        else:
            # GET a /api/1.0/photos/
            return False

    def has_object_permission(self, request, view, obj):
        """
        Si el usuario autenticado en request.user tiene permiso
        para realizar la acción (GET, POST, PUT o DELETE)
        sobre el objeto obj
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return request.user.is_superuser or request.user == obj