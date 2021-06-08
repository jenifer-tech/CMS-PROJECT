from blog.models import BlogPost
from blog.exceptions import BlogNotFoundException 

def get_object(blog_id): 
    try:
        account=BlogPost.objects.get(pk=blog_id)			
    except BlogPost.DoesNotExist:
        raise BlogNotFoundException
    return account 
 