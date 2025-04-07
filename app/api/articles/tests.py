from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User
from api.tags.models import Tag
from .models import Article
from rest_framework_simplejwt.tokens import RefreshToken
import csv
import io

class ArticleAPITestCase(APITestCase):
    def setUp(self):
        # Create a user who is an author
        self.author = User.objects.create_user(
            email='author@example.com',
            first_name='Author',
            last_name='User',
            password='authorpassword123'
        )
        
        # Create a regular user (non-author)
        self.user = User.objects.create_user(
            email='user@example.com',
            first_name='Regular',
            last_name='User',
            password='userpassword123'
        )
        
        # Create a test tag
        self.tag = Tag.objects.create(name="Test Tag")
        
        # Create a test article
        self.article = Article.objects.create(
            title="Test Article",
            abstract="This is a test abstract for the article"
        )
        
        # Set authors and tags
        self.article.authors.set([self.author])
        self.article.tags.set([self.tag])
        
        # Get tokens for authentication
        self.author_refresh = RefreshToken.for_user(self.author)
        self.author_access = str(self.author_refresh.access_token)
        
        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_access = str(self.user_refresh.access_token)
        
        # URL for article details
        self.url = reverse('article_details', kwargs={'article_id': self.article.id})
    
    def authenticate_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.author_access}')
    
    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access}')
    
    def clear_credentials(self):
        self.client.credentials()

class ArticlesListViewTest(ArticleAPITestCase):
    def test_create_article(self):
        """
        Test creating a new article
        """
        url = reverse('articles_list')
        self.authenticate_author()
        
        new_article_data = {
            'title': 'New Test Article',
            'abstract': 'This is an abstract for the new test article',
            'authors': [self.author.id],
            'tags': [self.tag.name]
        }
        
        response = self.client.post(url, new_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the article was created in the database
        self.assertTrue(Article.objects.filter(title='New Test Article').exists())
        
        # Check the returned data matches what we sent
        self.assertEqual(response.data['title'], 'New Test Article')
        self.assertEqual(response.data['abstract'], 'This is an abstract for the new test article')
        
    def test_list_articles(self):
        """
        Test retrieving list of articles
        """
        url = reverse('articles_list')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # Should see at least two article

class ArticleDetailsTest(ArticleAPITestCase):
    def test_get_article_details_authorized(self):
        """
        Test retrieving article details with proper authorization
        """
        self.authenticate_author()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.article.id)
        self.assertEqual(response.data['title'], self.article.title)
    
    def test_get_article_details_unauthorized(self):
        """
        Test retrieving article details without authorization
        """
        # No credentials provided
        self.clear_credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_article_as_author(self):
        """
        Test updating article as an author
        """
        self.authenticate_author()
        updated_data = {
            'title': 'Updated Title',
            'abstract': 'Updated abstract text',
            'authors': [self.author.id],
            'tags': [self.tag.name]
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh article from database
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')
        self.assertEqual(self.article.abstract, 'Updated abstract text')
    
    def test_update_article_unauthorized(self):
        """
        Test updating article without authorization
        """
        # No credentials provided
        self.clear_credentials()
        updated_data = {
            'title': 'Updated Title',
            'abstract': 'Updated abstract text',
            'authors': [self.author.id],
            'tags': [self.tag.name]
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify article was not changed
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Test Article')
    
    def test_update_article_as_non_author(self):
        """
        Test updating article as a non-author user
        """
        self.authenticate_user()
        updated_data = {
            'title': 'Updated Title',
            'abstract': 'Updated abstract text',
            'authors': [self.author.id],
            'tags': [self.tag.name]
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify article was not changed
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Test Article')
    
    def test_delete_article_as_author(self):
        """
        Test deleting article as an author
        """
        self.authenticate_author()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify article was deleted
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())
    
    def test_delete_article_unauthorized(self):
        """
        Test deleting article without authorization
        """
        # No credentials provided
        self.clear_credentials()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify article still exists
        self.assertTrue(Article.objects.filter(id=self.article.id).exists())
    
    def test_delete_article_as_non_author(self):
        """
        Test deleting article as a non-author user
        """
        self.authenticate_user()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify article still exists
        self.assertTrue(Article.objects.filter(id=self.article.id).exists())

class ArticleDetailsTest(ArticleAPITestCase):
    def test_get_article_details_authorized(self):
        """Test retrieving article details with proper authorization"""
        self.authenticate_author()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.article.id)
    
    def test_get_article_details_unauthorized(self):
        """Test retrieving article details without authorization"""
        self.clear_credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ArticleCSVViewTest(ArticleAPITestCase):
    def test_authenticated_access(self):
        """Test that authenticated users can access CSV endpoint"""
        url = reverse('articles_csv')  # Added CSV view URL
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_unauthenticated_access(self):
        """Test that unauthenticated users are denied access"""
        url = reverse('articles_csv')  # Added CSV view URL
        self.clear_credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_csv_content(self):
        """Test CSV response structure and data"""

        self.authenticate_user()
        url = reverse('articles_csv')  # Added CSV view URL
        response = self.client.get(url)
        csv_file = io.StringIO(response.content.decode("utf-8"))
        reader = csv.reader(csv_file)

        # Validate headers
        headers = next(reader)
        expected_headers = ["ID", "title", "abstract", "authors", "tags", "publication_date"]
        self.assertEqual(headers, expected_headers)

        # Validate article data
        row = next(reader)
        self.assertEqual(row[1], "Test Article")
        self.assertEqual(row[2], "This is a test abstract for the article")
        self.assertEqual(row[3], "Author User")
        self.assertEqual(row[4], "Test Tag")