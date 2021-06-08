from django.urls import path
from blog.views import CreateBlogView,GetMyBlogPost,UpdatePostView,DeletePost

app_name = 'blog'

urlpatterns = [
    path('blogpost/', CreateBlogView.as_view(), name="create new blog post"),    
    path('bloglists/<int:pk>', GetMyBlogPost.as_view(), name="list of my posts"),
    path('updatepost/<int:pk>', UpdatePostView.as_view(), name="list of my posts"),
    path('deletepost/<int:pk>', DeletePost.as_view(), name="delete my posts"),
]