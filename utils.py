from comment.models import Comment
from comment.exceptions import CommentsNotFoundException 


def get_object(blog_id): 
    try:
        account=Comment.objects.get(pk=blog_id)			
    except Comment.DoesNotExist:
        raise CommentsNotFoundException
    return account 
 