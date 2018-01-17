# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status

from users.permissions import UserPermission
from users.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ViewSet

class UserViewSet(ViewSet):

    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def list(self, request):
        self.check_permissions(request)
        # Instanciación de instanciador manual
        paginator = PageNumberPagination()
        users = User.objects.all()
        # Paginar el queryset
        users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        self.check_permissions(request)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        self.check_permissions(request)
        user_selected = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user_selected)
        serializer = UserSerializer(user_selected)
        return Response(serializer.data)

    def update(self, request, pk):
        self.check_permissions(request)
        user_selected = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user_selected)
        serializer = UserSerializer(instance=user_selected, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        self.check_permissions(request)
        user_selected = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user_selected)
        user_selected.delete()
        return Response(status.HTTP_204_NO_CONTENT)
