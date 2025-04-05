from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthView, UserProfileView,UsersListView

urlpatterns = [
    # Token auth endpoint
    path('auth/token', AuthView.as_view(), name='spotify_auth'),
    
    # JWT refresh endpoint
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoint
    path('me/', UserProfileView.as_view(), name='user_profile'),

    path('', UsersListView.as_view(), name='users'),
]