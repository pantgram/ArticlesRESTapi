from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Comment
from .serializers import CommentSerializer
from .filters import CommentFilter
from api.query_parameters_mixin import QueryParamValidationMixin
from api.custom_permissions import IsAuthor

class CommentView(QueryParamValidationMixin,generics.ListCreateAPIView):
    """
    View for retrieving and creating comments
    """
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all().distinct() # avoid duplicates
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = '__all__'
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        """
        Custom logic to associate the comment with the logged-in user
        """
        
        serializer.save(author=self.request.user)

class RetrieveUpdateDeleteComment(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().distinct()
    lookup_url_kwarg = 'comment_id'
    filter_backends = [DjangoFilterBackend]  # Enable filtering and searching

    def get_permissions(self):
        """
        Override get_permissions to apply different permissions based on the action
        """
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            # Only authors can update
            return [IsAuthenticated(), IsAuthor()]
        elif self.request.method == 'DELETE':
            # Only authors  can delete
            return [IsAuthenticated() , IsAuthor()]
        # Default to the class-level permissions
        return super().get_permissions()
