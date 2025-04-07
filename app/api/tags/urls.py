from django.urls import path
from .views import TagView,RetrieveUpdateDeleteTag

urlpatterns = [
    path('', TagView.as_view(), name='tags_list'),
    path('<int:tag_id>/', RetrieveUpdateDeleteTag.as_view(), name='tag_details'),
]