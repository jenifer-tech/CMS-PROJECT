from django.urls import path
from comment.views import CommentList,CommentDetail

app_name = 'comment'

urlpatterns = [
    path('comments/', CommentList.as_view(), name="create a new comments on post"),    
    path('altercomment/<int:pk>', CommentDetail.as_view(), name="Approved the comment by Admin"),
   
]