from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from .models import Tag
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class TagTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create_superuser(email="testAuthor01@gmail.com", first_name="Test", last_name= "User01", password="TestPassword10!")
        self.user = User.objects.create_user(email="test02@gmail.com", first_name="Test", last_name= "User02", password="TestPassword20!")
        self.tag = Tag.objects.create(name="Test Tag") 
        self.url = reverse('tag_details', kwargs={'tag_id':self.tag.id})
        refresh_user_admin = RefreshToken.for_user(self.user_admin)
        self.token_admin = refresh_user_admin.access_token
        refresh_user = RefreshToken.for_user(self.user)
        self.token_user= refresh_user.access_token

   
    
    def test_get_tag_details_authorized(self):
        """
        Test retrieving tag details with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tag.id, response.data['id'])
    
    def test_get_tag_details_unauthorized(self):
        """
        Test retrieving tag details without authorization
        """
        # No credentials provided
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting Unauthorized
    
    def test_put_tag_authorized(self):
        """
        Test updating tag with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        updated_data = {
        'name':'Updated Test'   
    }
        response = self.client.put(self.url, updated_data, format='json')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
           print(f"Error response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database to get updated values
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Updated Test')
    
    def test_put_tag_unauthorized(self):
        """
        Test updating tag without authorization
        """
        # No credentials provided
        updated_data = {
        'name':'Updated Test'   
    }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting Unauthorized
        
        # Verify tag was not changed
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'Test Tag')

    def test_put_tag_not_allowed(self):
        """
        Test updating tag that user in not an admin
        """
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        updated_data = {
        'name':'Updated Test'   
    }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Not allowed
        
    
    
    def test_delete_tag_authorized(self):
        """
        Test deleting tag with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # No Content on successful deletion
        
        # Verify tag was deleted
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(id=self.tag.id)
    
    def test_delete_tag_unauthorized(self):
        """
        Test deleting tag without authorization
        """
        # No credentials provided
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)  # Expecting Unauthorized
        
        # Verify tag still exists
        tag_exists = Tag.objects.filter(id=self.tag.id).exists()
        self.assertTrue(tag_exists)

    def test_delete_tag_not_allowed(self):
        """
        Test deleting tag with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Not allowed
        
        # Verify tag still exists
        tag_exists = Tag.objects.filter(id=self.tag.id).exists()
        self.assertTrue(tag_exists)
    