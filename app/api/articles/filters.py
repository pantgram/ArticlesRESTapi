from django_filters import rest_framework as filters
from .models import Article

class ArticleFilter(filters.FilterSet):
    strict = True
    year = filters.NumberFilter(field_name="publication_date", lookup_expr='year')
    month = filters.NumberFilter(field_name="publication_date", lookup_expr='month')
    authors = filters.BaseInFilter(field_name='authors',lookup_expr='in')
    tags = filters.BaseInFilter(field_name='tags',lookup_expr='in')
    class Meta:
        model = Article
        fields = ['year', 'month','authors','tags']

class ArticleCSVFilter(filters.FilterSet):
    strict = True
    year = filters.NumberFilter(field_name="publication_date", lookup_expr='year')
    month = filters.NumberFilter(field_name="publication_date", lookup_expr='month')
    authors = filters.BaseInFilter(field_name='authors',lookup_expr='in')
    tags = filters.BaseInFilter(field_name='tags',lookup_expr='in')
    id = filters.BaseInFilter(field_name='id',lookup_expr='in')
    class Meta:
        model = Article
        fields = ['year', 'month','authors','tags','id']
