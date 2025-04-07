from django.urls import path
from .views import ArticleView,RetrieveUpdateDeleteArticle,ArticleCSVView

urlpatterns = [
    # Token auth endpoint
    path('', ArticleView.as_view(), name='articles_list'),
    path('export/csv/', ArticleCSVView.as_view(), name='articles_csv'),
    path('<int:article_id>/', RetrieveUpdateDeleteArticle.as_view(), name='article_details'),
]