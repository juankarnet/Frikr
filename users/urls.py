
from django.conf.urls import url, include
from users.views import LoginView, LogoutView

urlpatterns = [

    #Users urls
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),
]
