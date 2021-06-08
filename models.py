from django.db import models
from django.conf import settings
from blog.models import BlogPost


class Comment(models.Model):	
    commentsbody 		= models.TextField(max_length=5000, null=False, blank=True)	
    is_approved         = models.BooleanField(default=False)
    created  		    = models.DateTimeField(auto_now_add=True, verbose_name="date of comments")	
    author 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post                = models.ForeignKey(BlogPost,on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
