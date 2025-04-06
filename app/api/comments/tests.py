from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from api.articles.models import Article
from .models import Comment
from api.tags.models import Tag
from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class CommentTestCase(APITestCase):
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
        self.comment = Comment.objects.create(
            text="Test Comment",
            author = self.user_author,
            article = self.article
        )

        self.url =reverse('comment_details', kwargs={'comment_id':self.comment.id})
        refresh_user_author = RefreshToken.for_user(self.user_author)
        self.token_author = refresh_user_author.access_token
        refresh_user = RefreshToken.for_user(self.user)
        self.token_user= refresh_user.access_token

   
    
    def test_get_comment_details_authorized(self):
        """
        Test retrieving comment details with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.id, response.data['id'])
    
    def test_get_comment_details_unauthorized(self):
        """
        Test retrieving comment details without authorization
        """
        # No credentials provided
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting Unauthorized
    
    def test_put_article_authorized(self):
        """
        Test updating comment with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_author}')
        updated_data = {
        'text': 'Updated text',
        'author': self.user_author.id, 
        'article': self.article.id    
    }
        response = self.client.put(self.url, updated_data, format='json')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
           print(f"Error response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database to get updated values
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Updated text')
    
    def test_put_comment_unauthorized(self):
        """
        Test updating comment without authorization
        """
        # No credentials provided
        updated_data = {
        'text': 'Updated text',
        'author': self.user_author.id, 
        'article': self.article.id   
    }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting Unauthorized
        
        # Verify article was not changed
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Test Comment')

    def test_put_comment_not_allowed(self):
        """
        Test updating comment that user in not an author
        """
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        updated_data = {
        'text': 'Updated text',
        'author': self.user_author.id, 
        'article': self.article.id    
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
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=self.article.id)
    
    def test_delete_article_unauthorized(self):
        """
        Test deleting article without authorization
        """
        # No credentials provided
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)  # Expecting Unauthorized
        
        # Verify article still exists
        comment_exists = Comment.objects.filter(id=self.comment.id).exists()
        self.assertTrue(comment_exists)

    def test_delete_article_not_allowed(self):
        """
        Test deleting comment with proper authorization
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Not allowed
        
        # Verify article still exists
        comment_exists = Comment.objects.filter(id=self.comment.id).exists()
        self.assertTrue(comment_exists)
    