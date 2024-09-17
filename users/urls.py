from django.urls import path
from .views import LoginView, RegisterView, UserView, UserUpdateView, UserDeleteView, UserListView, \
    UserDetailView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/user', UserView.as_view(), name='user'),
    path('auth/user/logout', LogoutView.as_view(), name='logout'),
    path('user/update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('auth/delete/user', UserDeleteView.as_view(), name='user_delete'),
    path('users', UserListView.as_view(), name='users'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]