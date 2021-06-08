from rest_framework import serializers
from blog.models import BlogPost
from account.serializers import RegisterSerializer
from account.models import Account

class BlogPostCreateSerializer(serializers.ModelSerializer):
	# author=RegisterSerializer(read_only=True) 
	# author_id  = serializers.PrimaryKeyRelatedField(source='author', write_only=True, queryset=Account.objects.all())

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image', 'date_updated', 'author','author_id']
