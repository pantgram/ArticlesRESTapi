from rest_framework import generics,filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser,OR
from .filters import ArticleFilter,ArticleCSVFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article
from django.http import HttpResponse
from api.tags.models import Tag
from .serializers import ArticleSerializer
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from api.custom_permissions import IsAnAuthor
from api.query_parameters_mixin import QueryParamValidationMixin
import csv


class ArticleView(QueryParamValidationMixin,generics.ListCreateAPIView):
    """
    Views for retrieving all articles
    """
    
    permission_classes = [IsAuthenticated]
    
    """
    Get the current articles with filters,ordering,search
    """
    queryset = Article.objects.all().distinct() # avoid duplicates
    serializer_class = ArticleSerializer 
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]  # Enable filtering and searching
    ordering_fields = '__all__'
    filterset_class = ArticleFilter  # Use our custom filter
    
    def get_queryset(self):
        """
        Override get_queryset to apply filters first, then search
        """
        # Get the base queryset which will be filtered by our custom filters
        queryset = super().get_queryset()
        
        # Get the keyword query parameter
        search_query = self.request.query_params.get('keyword', None)
        
        # If there's a keyword term, apply the search after filtering
        if search_query:
            vector = SearchVector('abstract', 'title')
            print(vector)
            
            query = SearchQuery(search_query)
            print(query)
            queryset = queryset.annotate(
                rank=SearchRank(vector, query)
            ).filter(rank__gt=0).order_by("-rank")
        
        return queryset
    
    def perform_create(self, serializer):
        """
    Perform create to the serializer
        """
        # Add current user as an author and create article
        

        authors_appended = self.request.data['authors']
        authors_appended.append(self.request.user)
        serializer.save(authors=authors_appended)
    
class RetrieveUpdateDeleteArticle(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().distinct()
    lookup_url_kwarg = 'article_id'
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """
        Override get_permissions to apply different permissions based on the action
        """
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            # Only authors can update
            return [IsAuthenticated(), OR(IsAnAuthor(), IsAdminUser())]
        elif self.request.method == 'DELETE':
            # Only authors can delete
            return [IsAuthenticated() , OR(IsAnAuthor(), IsAdminUser())]
        # Default to the class-level permissions
        return super().get_permissions()

class ArticleCSVView(QueryParamValidationMixin,generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    
    """
    Get the current articles with filters,ordering,search
    """
    queryset = Article.objects.all().distinct() # avoid duplicates
    serializer_class = ArticleSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]  # Enable filtering and searching
    search_fields = ['abstract', 'title'] # keyword search specific fields
    ordering_fields = '__all__'
    filterset_class = ArticleCSVFilter  # Use our custom filter

    def get(self, request, *args, **kwargs):

        """Generate CSV response """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="articles.csv"'
        # Create a csv writer to apply in the response
        writer = csv.writer(response)
        writer.writerow(['ID', 'title', 'abstract','authors', 'tags', 'publication_date'])  # CSV headers
        # Apply filters, ordering, and search BEFORE iterating through the articles
        filtered_queryset = self.filter_queryset(self.get_queryset())
        for article in filtered_queryset:
            writer.writerow([
                article.id,
                article.title,
                article.abstract,
                ", ".join([str(author) for author in article.authors.all()]),  # Handle Many-to-Many
                ", ".join([str(tag) for tag in article.tags.all()]),  # Handle Many-to-Many
                article.publication_date
            ])

        return response

    
        
    






