from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPITestCase(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword123'
        )
        
        # Create an admin user using create_superuser
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpassword123'
        )
        
        # Verify admin status
        self.assertTrue(self.admin.is_admin)
        
        # Get tokens for authentication
        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_access = str(self.user_refresh.access_token)
        
        self.admin_refresh = RefreshToken.for_user(self.admin)
        self.admin_access = str(self.admin_refresh.access_token)

    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access}')
    
    def authenticate_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
    
    def clear_credentials(self):
        self.client.credentials()


class AuthViewTest(UserAPITestCase):
    def test_create_new_user(self):
        """Test creating a new user through the auth endpoint"""
        url = reverse('auth')
        data = {
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_authenticate_existing_user(self):
        """Test authenticating an existing user"""
        url = reverse('auth')
        data = {
            'email': 'user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_authenticate_wrong_credentials(self):
        """Test authentication with wrong credentials"""
        url = reverse('auth')
        data = {
            'email': 'user@example.com',
            'first_name': 'Wrong',
            'last_name': 'User',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


class UserProfileViewTest(UserAPITestCase):
    def test_get_user_profile_authenticated(self):
        """
        Test retrieving user profile when authenticated
        """
        url = reverse('user_profile')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
    
    def test_get_user_profile_unauthenticated(self):
        """
        Test retrieving user profile when not authenticated
        """
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UsersListViewTest(UserAPITestCase):
    def test_list_users(self):
        """
        Test retrieving list of users
        """
        url = reverse('users_list')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # Should see at least both users
    
    
    def test_list_users_unauthenticated(self):
        """
        Test retrieving list of users without authentication
        """
        url = reverse('users_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveUpdateDeleteUserTest(UserAPITestCase):
    def test_retrieve_user_as_admin(self):
        """
        Test retrieving a specific user as admin
        """
        url = reverse('user_details', kwargs={'user_id': self.user.id})
        self.authenticate_admin()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
    
    def test_retrieve_user_as_regular_user(self):
        """
        Test retrieving a specific user as regular user
        """
        url = reverse('user_details', kwargs={'user_id': self.admin.id})
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_user_as_admin(self):
        """
        Test updating a user as admin
        """
        url = reverse('user_details', kwargs={'user_id': self.user.id})
        self.authenticate_admin()
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
    
    def test_update_user_as_regular_user(self):
        """Test updating a user as admin"""
        url = reverse('user_details', kwargs={'user_id': self.user.id})
        self.authenticate_user()
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user.refresh_from_db()
    
    def test_delete_user_as_admin(self):
        """Test deleting a user as admin"""
        url = reverse('user_details', kwargs={'user_id': self.user.id})
        self.authenticate_admin()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email='user@example.com').exists())
    
    def test_delete_user_as_regular_user(self):
        """Test deleting a user as regular user"""
        url = reverse('user_details', kwargs={'user_id': self.admin.id})
        self.authenticate_user()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(email='admin@example.com').exists())