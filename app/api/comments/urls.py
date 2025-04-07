from django.urls import path
from .views import CommentView,RetrieveUpdateDeleteComment

urlpatterns = [
    # Token auth endpoint
    path('', CommentView.as_view(), name='comments_list'),
    path('<int:comment_id>/', RetrieveUpdateDeleteComment.as_view(), name='comment_details'),
]