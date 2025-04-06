from django.db import models
from api.models import User
from api.tags.models import Tag

    
class Article(models.Model):
     publication_date = models.DateField(auto_now=True)
     authors = models.ManyToManyField(User)
     abstract = models.TextField()
     tags = models.ManyToManyField(Tag)
     title = models.CharField(max_length=200)

     def __str__(self):
        return self.title
   
     class Meta:
        db_table = 'Article'
        ordering = ['id']