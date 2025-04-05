from rest_framework import status, views,generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from api.models import User
from api.serializers import UserSerializer

class AuthView(views.APIView):
    """
    Handles user creation
    """
    # doesn't need authentication to access this endpoint
    permission_classes = [AllowAny]
    
    def post(self, request):
    
        
        # Create or update user
        try:
            data = request.data
            # Check if user already exists
            user_exists = User.objects.filter(email=data['email']).exists()
            if user_exists:
            # Authenticate existing user
                check, user = User.objects.check_user_credentials(data['email'], data['first_name'], data['last_name'], data['password'])
                if check is False:
                    return Response(
                    {"error": "Invalid credentials"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
                else: 
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
            
                    return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    })
            else:
            # Create new user
                user = User.objects.create_user(
                data['email'],
                data['first_name'],
                data['last_name'],
                data['password']
            )
                
            # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
            # return them to the user
                return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            
        except Exception as e:
            return Response({"error": f"User creation failed: {str(e)}"}, 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

class UserProfileView(views.APIView):
    """
    View for retrieving and updating the authenticated user's profile
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get the current user's profile
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UsersListView(generics.ListAPIView):
    """
    View for retrieving aall users
    """
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]  
    queryset = User.objects.all()