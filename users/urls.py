from django.contrib import admin
from django.urls import path
from users.views import (
    register_view,
    CustomAuthToken,
    LogoutView,
    qr_api
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'

urlpatterns = [

    # url for user registration
    path('registration/', register_view, name='registration'),
    # url for user login
    path('login/api/', obtain_auth_token, name='login'),

    path('login/', CustomAuthToken.as_view(), name='custom auth token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('qr/<int:id>/', qr_api)

    # path('oauth/login/', SocialLoginView.as_view())  # Fb login auth
]
