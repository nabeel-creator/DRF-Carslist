from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from userinfo.views import RegisterUser, LogoutUser, ViewUser

urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('logout/', LogoutUser.as_view(), name='logout_user'),
    path('view/', ViewUser.as_view(), name='view_user'),
]