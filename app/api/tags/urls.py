from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TagView,UpdateDeleteTag

urlpatterns = [
    path('', TagView.as_view(), name='tags'),
    path('<int:tag_id>/', UpdateDeleteTag.as_view(), name='tags'),
]