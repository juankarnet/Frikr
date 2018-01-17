
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from users.api import UserViewSet

# API Routers
router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = [
    #API urls
    url(r'1.0/', include(router.urls)),
]
