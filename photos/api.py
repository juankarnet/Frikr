# -*- coding: utf-8 -*-

#from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from models import Photo, Comment
from photos.serializers import PhotoSerializer, PhotoListSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from photos.views import Photos_Queryset

class PhotoViewSet(Photos_Queryset, ModelViewSet):

    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'owner__first_name')
    ordering_fields = ('name', 'owner')
    def get_queryset(self):
        return self.get_photos_queryset(self.request)

    def get_serializer_class(self):
        return PhotoListSerializer if self.action == 'list' else PhotoSerializer

    def perform_create(self, serializer):
        """
        Asigna automáticamente la autoría de la nueva foto al
        usuario autenticado
        :param serializer:
        :return:
        """
        serializer.save(owner=self.request.user)

class CommentViewSet(ModelViewSet):

    #queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def list(self, request):
        self.check_permissions(request)
        # Instanciación de instanciador manual
        paginator = PageNumberPagination()
        comments = Comment.objects.all()
        # Paginar el queryset
        comments = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(comments, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        self.check_permissions(request)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        self.check_permissions(request)
        comment_selected = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment_selected)
        serializer = CommentSerializer(comment_selected)
        return Response(serializer.data)

    def update(self, request, pk):
        self.check_permissions(request)
        comment_selected = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment_selected)
        serializer = CommentSerializer(instance=comment_selected, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        self.check_permissions(request)
        user_selected = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, user_selected)
        user_selected.delete()
        return Response(status.HTTP_204_NO_CONTENT)

# class PhotoListAPI(Photos_Queryset ,ListCreateAPIView):
#
#     queryset = Photo.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     def get_serializer_class(self):
#         return PhotoSerializer if self.request.method == 'POST' else PhotoListSerializer
#
#     def get_queryset(self):
#         return self.get_photos_queryset(self.request)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
# class PhotoDetailAPI(Photos_Queryset ,RetrieveUpdateDestroyAPIView):
#
#     queryset = Photo.objects.all()
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = PhotoSerializer
#
#     def get_queryset(self):
#         return self.get_photos_queryset(self.request)
