from django.urls import include,path

urlpatterns = [
    path('Users/',include("api.users.urls")),
    path('Articles/',include("api.articles.urls")),
    path('Comments/',include("api.comments.urls")),
    path('Tags/',include("api.tags.urls")),
    
]
