from django_filters import rest_framework as filters
from .models import Comment

class CommentFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name="publication_date", lookup_expr='year')
    month = filters.NumberFilter(field_name="publication_date", lookup_expr='month')
    author = filters.CharFilter(field_name='author',lookup_expr='exact')
    article = filters.CharFilter(field_name='article',lookup_expr='exact')
    class Meta:
        model = Comment
        fields = ['year', 'month','author','article']
