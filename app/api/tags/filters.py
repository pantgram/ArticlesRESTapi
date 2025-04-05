from django_filters import rest_framework as filters
from .models import Tag

class TagFilter(filters.FilterSet):
  
    name = filters.CharFilter(field_name='name',lookup_expr='exact')
    class Meta:
        model = Tag
        fields = ['name']