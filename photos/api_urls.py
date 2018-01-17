
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from photos.api import PhotoViewSet, CommentViewSet

# API Routers
router = DefaultRouter(trailing_slash=False)
router.register(r'photos', PhotoViewSet)
router.register(r'comments', CommentViewSet, base_name='comment')

urlpatterns = [

    #API urls
    url(r'1.0/', include(router.urls)),
]
