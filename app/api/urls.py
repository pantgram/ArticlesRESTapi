from django.urls import include,path

urlpatterns = [
    path('users/',include("api.users.urls")),
    path('articles/',include("api.articles.urls")),
    path('comments/',include("api.comments.urls")),
    path('tags/',include("api.tags.urls")),
    
]
