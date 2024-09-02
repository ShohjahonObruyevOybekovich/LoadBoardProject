

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (CustomAuthToken, LogoutAPIView, RegisterAPIView, UserUpdateAPIView,
                    UserInfo, UserList, UserDeleteAPIView)

urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='user_login'),

    path('create/', RegisterAPIView.as_view(), name='user_create'),
    # path('confirm-code/', ConfirmationCodeAPIView.as_view(), name='confirm_code'),
    # path('forget-password', PasswordResetRequestView.as_view(), name='forget_password'),
    # path('reset-password/<str:uuid>/<str:token>', PasswordResetView.as_view() ,name='reset-password-view'),
    path('user-list/',UserList.as_view(), name='user_list'),
    path('user-update/<uuid:uuid>', UserUpdateAPIView.as_view(), name='user_update'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('user-info/',UserInfo.as_view(), name='user-info'),
    path('user-delete/<uuid:uuid>', UserDeleteAPIView.as_view(), name='user_delete'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]