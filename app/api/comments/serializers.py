from rest_framework import serializers
from .models import Comment
from api.articles.models import Article


class CommentSerializer(serializers.ModelSerializer):

    author =  serializers.StringRelatedField()
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    class Meta:
        model = Comment
        fields = '__all__'

