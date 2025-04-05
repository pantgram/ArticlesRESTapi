from rest_framework import serializers
from .models import Article
from api.models import User
from api.tags.models import Tag


class ArticleSerializer(serializers.ModelSerializer):

    authors = serializers.SlugRelatedField(many=True, queryset=User.objects.all(), slug_field='id')
    tags = serializers.SlugRelatedField(many=True, queryset=Tag.objects.all(), slug_field='name')

    class Meta:
        model = Article
        fields = '__all__'

