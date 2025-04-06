from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from .models import Article
from api.tags.models import Tag
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class ArticleTestCase(APITestCase):
    def setUp(self):
        self.user_author = User.objects.create_user(email="testAuthor01@gmail.com", first_name="Test", last_name= "User01", password="TestPassword10!")
        self.user = User.objects.create_user(email="test02@gmail.com", first_name="Test", last_name= "User02", password="TestPassword20!")
        self.tag = Tag.objects.create(name="Test Tag")
        self.article = Article.objects.create(
            abstract="Test Paragraph",
            title="Test Title"
        )
        
        self.article.authors.set([self.user_author])
        self.article.tags.set([self.tag])
        self.url =reverse('article_details', kwargs={'article_id':self.article.id})
        refresh_user_author = RefreshToken.for_user(self.user_author)
        self.token_author = refresh_user_author.access_token
        refresh_user = RefreshToken.for_user(self.user)
        self.token_user= refresh_user.access_token

   
    
    def test_get_article_details_authorized(self):
        """
        Test retrieving article details with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.id, response.data['id'])
    
    def test_get_article_details_unauthorized(self):
        """
        Test retrieving article details without authorization
        """
        # No credentials provided
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting Unauthorized
    
    def test_put_article_authorized(self):
        """
        Test updating article with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        updated_data = {
        'title': 'Updated Title',
        'abstract': 'Updated abstract text',
        'authors': [self.user_author.id], 
        'tags': [self.tag.name]     
    }
        response = self.client.put(self.url, updated_data, format='json')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
           print(f"Error response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database to get updated values
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')
        self.assertEqual(self.article.abstract, 'Updated abstract text')
    
    def test_put_article_unauthorized(self):
        """
        Test updating article without authorization
        """
        # No credentials provided
        updated_data = {
        'title': 'Updated Title',
        'abstract': 'Updated abstract text',
        'authors': [self.user_author.id], 
        'tags': [self.tag.name]     
    }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting Unauthorized
        
        # Verify article was not changed
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Test Title')

    def test_put_article_not_allowed(self):
        """
        Test updating article that user in not an author
        """
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        updated_data = {
        'title': 'Updated Title',
        'abstract': 'Updated abstract text',
        'authors': [self.user_author.id], 
        'tags': [self.tag.name]     
    }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Not allowed
        
    
    
    def test_delete_article_authorized(self):
        """
        Test deleting article with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # No Content on successful deletion
        
        # Verify article was deleted
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(id=self.article.id)
    
    def test_delete_article_unauthorized(self):
        """
        Test deleting article without authorization
        """
        # No credentials provided
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)  # Expecting Unauthorized
        
        # Verify article still exists
        article_exists = Article.objects.filter(id=self.article.id).exists()
        self.assertTrue(article_exists)

    def test_delete_article_not_allowed(self):
        """
        Test deleting article with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Not allowed
        
        # Verify article still exists
        article_exists = Article.objects.filter(id=self.article.id).exists()
        self.assertTrue(article_exists)
    