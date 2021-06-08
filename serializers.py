from rest_framework import serializers
from comment.models import Comment
from account.models import Account
from blog.models import BlogPost
from blog.serializers import BlogPostCreateSerializer
from account.serializers import RegisterSerializer


class CommentSerializer(serializers.ModelSerializer):
    #author = serializers.ReadOnlyField(source='author.username')
    author=RegisterSerializer(read_only=True) 
    author_id  = serializers.PrimaryKeyRelatedField(source='author', write_only=True, queryset=Account.objects.all())
    post=BlogPostCreateSerializer(read_only=True) 
    post_id=serializers.PrimaryKeyRelatedField(source='post', write_only=True, queryset=BlogPost.objects.all())
    class Meta:
        model = Comment
        fields = ['id', 'commentsbody', 'author', 'author_id','post','post_id']        