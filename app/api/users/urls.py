from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView,LoginView, UserProfileView,UsersListView,RetrieveUpdateDeleteUser

urlpatterns = [
    # Token auth endpoint
    path('auth/token/register', RegisterView.as_view(), name='register'),
    path('auth/token/login', LoginView.as_view(), name='login'),
    
    # JWT refresh endpoint
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoint
    path('me/', UserProfileView.as_view(), name='user_profile'),

    path('', UsersListView.as_view(), name='users_list'),

    path('<int:user_id>/', RetrieveUpdateDeleteUser.as_view(), name='user_details'),
]