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

class RetrieveUpdateDeleteTag(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = TagSerializer
    queryset = Tag.objects.all().distinct()
    lookup_url_kwarg = 'tag_id'
    filter_backends = [DjangoFilterBackend]  # Enable filtering and searching

    def get_permissions(self):
        """
        Override get_permissions to apply different permissions based on the action
        """
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            # Only authors can update
            return [IsAuthenticated(),IsAdminUser()]
        elif self.request.method == 'DELETE':
            # Only authors can delete
            return [IsAuthenticated() , IsAdminUser()]
        # Default to the class-level permissions
        return super().get_permissions()