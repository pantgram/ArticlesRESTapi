from rest_framework import generics,filters
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .filters import TagFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tag
from .serializers import TagSerializer
from api.query_parameters_mixin import QueryParamValidationMixin

# Create your views here.
class TagView(QueryParamValidationMixin,generics.ListCreateAPIView):

    

    """
    Views for retrieving all Tags
    """
    
    permission_classes = [IsAuthenticated]
    
    """
    Get the current articles with search
    """
    queryset = Tag.objects.all().distinct() # avoid duplicates
    serializer_class = TagSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]  # Enable searching and filtering
    filterset_class = TagFilter  # Use our custom filter
    ordering_fields = '__all__'
    search_fields = ['name']
    


    def perform_create(self, serializer):
        """
    Perform create to the serializer
        """
        # Save article
        serializer.save()

class UpdateDeleteTag(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = TagSerializer
    queryset = Tag.objects.all().distinct()
    lookup_url_kwarg = 'tag_id'
    filter_backends = [DjangoFilterBackend]  # Enable filtering and searching