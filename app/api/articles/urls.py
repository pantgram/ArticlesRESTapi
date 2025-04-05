from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ArticleView,UpdateDeleteArticle,ArticleCSVView

urlpatterns = [
    # Token auth endpoint
    path('', ArticleView.as_view(), name='articles'),
    path('export/csv', ArticleCSVView.as_view(), name='articles_csv'),
    path('<int:article_id>/', UpdateDeleteArticle.as_view(), name='articles'),
]