
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from photos import views as photo_views
from photos.api import PhotoViewSet # PhotoListAPI, PhotoDetailAPI
from users import views as users_views

from photos.views import HomeView, DetailView, CreateView, PhotoListView, UserPhotosView
from users.api import UserViewSet #UserListAPI, UserDetailAPI
from users.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# API Routers
router = DefaultRouter(trailing_slash=False)
router.register(r'api/1.0/photos', PhotoViewSet)
router.register(r'api/1.0/users', UserViewSet, base_name='user')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    #Photo urls
    url(r'^$', HomeView.as_view(), name='photos_home'),
    url(r'^my-photos/$', login_required(UserPhotosView.as_view()), name='user_photos'),
    url(r'^photos/(?P<pk>[0-9]+)$', DetailView.as_view(), name='photo_detail'),
    url(r'^photos/create_photo$', CreateView.as_view(), name='photo_create'),
    url(r'^photos/$', PhotoListView.as_view(), name='photos_list'),

    # Photos API URLs
    # url(r'^api/1.0/photos/$', PhotoListAPI.as_view(), name='photo_list_api'),
    # url(r'^api/1.0/photos/(?P<pk>[0-9]+)$', PhotoDetailAPI.as_view(), name='photo_detail_api')

    #Users urls
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),

    #Users API URLs
    #url(r'^api/1.0/users/$', UserListAPI.as_view(), name='user_list_api'),
    #url(r'^api/1.0/users/(?P<pk>[0-9]+)$', UserDetailAPI.as_view(), name='user_detail_api')

    #API urls
    url(r'', include(router.urls)),
]
