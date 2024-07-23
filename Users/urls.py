from django.urls import path
from .views import *

urlpatterns = [
    path('register', registrationAPIView.as_view(), name="registration"),
    path('new-tokens', getNewTokenAPIView.as_view(), name="get new tokens"),
    path('login', loginAPIView.as_view(), name="login"),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailsAPIView.as_view(), name='user-details'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
]
