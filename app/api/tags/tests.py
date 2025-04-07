from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User
from .models import Tag
from rest_framework_simplejwt.tokens import RefreshToken

class TagAPITestCase(APITestCase):
    def setUp(self):
        # Create an admin user
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='adminpassword123'
        )
        
        # Create a regular user (non-admin)
        self.user = User.objects.create_user(
            email='user@example.com',
            first_name='Regular',
            last_name='User',
            password='userpassword123'
        )
        
        # Create a test tag
        self.tag = Tag.objects.create(name="Test Tag")
        
        # Get tokens for authentication
        self.admin_refresh = RefreshToken.for_user(self.admin)
        self.admin_access = str(self.admin_refresh.access_token)
        
        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_access = str(self.user_refresh.access_token)
        
        # URL for tag details
        self.url = reverse('tag_details', kwargs={'tag_id': self.tag.id})
    
    def authenticate_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_access}')
    
    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access}')
    
    def clear_credentials(self):
        self.client.credentials()

class TagsListViewTest(TagAPITestCase):

    def test_create_comment(self):
        """
        Test creating a new tag
        """
        url = reverse('tags_list')
        self.authenticate_user()
        
        new_tag_data = {
            'name': 'New tag name',
        }
        
        response = self.client.post(url, new_tag_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the tag was created in the database
        self.assertTrue(Tag.objects.filter(name='New tag name').exists())
        
        # Check the returned data matches what we sent
        self.assertEqual(response.data['name'], 'New tag name')

    def test_list_tags(self):
        """
        Test retrieving list of tags
        """
        url = reverse('tags_list')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # Should see at least two tags

class TagDetailsTest(TagAPITestCase):
    def test_get_tag_details_authorized(self):
        """
        Test retrieving tag details with proper authorization
        """
        self.authenticate_admin()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.tag.id)
        self.assertEqual(response.data['name'], self.tag.name)
    
    def test_get_tag_details_unauthorized(self):
        """
        Test retrieving tag details without authorization
        """
        # No credentials provided
        self.clear_credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_tag_as_admin(self):
        """
        Test updating tag as an admin
        """
        self.authenticate_admin()
        updated_data = {
            'name': 'Updated Tag Name'
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh tag from database
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Updated Tag Name')
    
    def test_update_tag_unauthorized(self):
        """
        Test updating tag without authorization
        """
        # No credentials provided
        self.clear_credentials()
        updated_data = {
            'name': 'Updated Tag Name'
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify tag was not changed
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Test Tag')
    
    def test_update_tag_as_regular_user(self):
        """
        Test updating tag as a regular user
        """
        self.authenticate_user()
        updated_data = {
            'name': 'Updated Tag Name'
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify tag was not changed
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Test Tag')
    
    def test_delete_tag_as_admin(self):
        """
        Test deleting tag as an admin
        """
        self.authenticate_admin()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify tag was deleted
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())
    
    def test_delete_tag_unauthorized(self):
        """
        Test deleting tag without authorization
        """
        # No credentials provided
        self.clear_credentials()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify tag still exists
        self.assertTrue(Tag.objects.filter(id=self.tag.id).exists())
    
    def test_delete_tag_as_regular_user(self):
        """
        Test deleting tag as a regular user
        """
        self.authenticate_user()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify tag still exists
        self.assertTrue(Tag.objects.filter(id=self.tag.id).exists())