from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CommentView,UpdateDeleteComment

urlpatterns = [
    # Token auth endpoint
    path('', CommentView.as_view(), name='comments'),
    path('<int:comment_id>/', UpdateDeleteComment.as_view(), name='articles'),
]