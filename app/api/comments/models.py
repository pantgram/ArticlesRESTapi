from django.db import models
from api.articles.models import Article
from api.models import User


    
class Comment(models.Model):
     
     publication_date = models.DateField(auto_now=True)
     author = models.ForeignKey(User,on_delete=models.CASCADE)
     text = models.TextField()
     article = models.ForeignKey(Article,on_delete=models.CASCADE)

     def __str__(self):
        return self.text
     
     class Meta:
        db_table = 'Comment'
        ordering = ['id']
