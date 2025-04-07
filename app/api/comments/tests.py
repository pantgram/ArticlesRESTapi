from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import User
from api.articles.models import Article
from .models import Comment
from api.tags.models import Tag
from rest_framework_simplejwt.tokens import RefreshToken

class CommentAPITestCase(APITestCase):
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
        
        # Create a test tag and article
        self.tag = Tag.objects.create(name="Test Tag")
        self.article = Article.objects.create(
            title="Test Article",
            abstract="This is a test abstract for the article"
        )
        
        # Set authors and tags for the article
        self.article.authors.set([self.author])
        self.article.tags.set([self.tag])
        
        # Create a test comment
        self.comment = Comment.objects.create(
            text="Test Comment",
            author=self.author,
            article=self.article
        )
        
        # Get tokens for authentication
        self.author_refresh = RefreshToken.for_user(self.author)
        self.author_access = str(self.author_refresh.access_token)
        
        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_access = str(self.user_refresh.access_token)
        
        # URL for comment details
        self.url = reverse('comment_details', kwargs={'comment_id': self.comment.id})
    
    def authenticate_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.author_access}')
    
    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access}')
    
    def clear_credentials(self):
        self.client.credentials()

class CommentsListViewTest(CommentAPITestCase):
    def test_create_comment(self):
        """
        Test creating a new comment
        """
        url = reverse('comments_list')
        self.authenticate_author()
        
        new_comment_data = {
            'text': 'New comment text',
            'author': self.author.id,
            'article': self.article.id
        }
        
        response = self.client.post(url, new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the comment was created in the database
        self.assertTrue(Comment.objects.filter(text='New comment text').exists())
        
        # Check the returned data matches what we sent
        self.assertEqual(response.data['text'], 'New comment text')
        self.assertEqual(response.data['article'], self.article.id)

    def test_list_comments(self):
        """
        Test retrieving list of comments
        """
        url = reverse('comments_list')
        self.authenticate_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # Should see at least two comments
class CommentDetailsTest(CommentAPITestCase):
    def test_get_comment_details_authorized(self):
        """
        Test retrieving comment details with proper authorization
        """
        self.authenticate_author()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.comment.id)
        self.assertEqual(response.data['text'], self.comment.text)
    
    def test_get_comment_details_unauthorized(self):
        """
        Test retrieving comment details without authorization
        """
        # No credentials provided
        self.clear_credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_comment_as_author(self):
        """
        Test updating comment as the author
        """
        self.authenticate_author()
        updated_data = {
            'text': 'Updated comment text',
            'author': self.author.id,
            'article': self.article.id
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh comment from database
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Updated comment text')
    
    def test_update_comment_unauthorized(self):
        """
        Test updating comment without authorization
        """
        # No credentials provided
        self.clear_credentials()
        updated_data = {
            'text': 'Updated comment text',
            'author': self.author.id,
            'article': self.article.id
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify comment was not changed
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Test Comment')
    
    def test_update_comment_as_non_author(self):
        """
        Test updating comment as a non-author user
        """
        self.authenticate_user()
        updated_data = {
            'text': 'Updated comment text',
            'author': self.author.id,
            'article': self.article.id
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify comment was not changed
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Test Comment')
    
    def test_delete_comment_as_author(self):
        """
        Test deleting comment as the author
        """
        self.authenticate_author()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify comment was deleted
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
    
    def test_delete_comment_unauthorized(self):
        """
        Test deleting comment without authorization
        """
        # No credentials provided
        self.clear_credentials()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify comment still exists
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())
    
    def test_delete_comment_as_non_author(self):
        """
        Test deleting comment as a non-author user
        """
        self.authenticate_user()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify comment still exists
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())