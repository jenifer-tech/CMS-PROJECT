from blog.models import BlogPost
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from blog.serializers import BlogPostCreateSerializer
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from blog.utils import get_object

CREATE_SUCCESS = 'created'
UPDATE_SUCCESS = 'updated'
DELETE_SUCCESS = 'deleted'	



class CreateBlogView(generics.GenericAPIView):	     
	permission_classes=[IsAuthenticated]
	serializer_class=BlogPostCreateSerializer
	parser_classes = (FormParser, MultiPartParser)
	def post(self,request):
			data = request.data
			data['author'] = request.user.pk
			serializer = BlogPostCreateSerializer(data=data)
			data = {}
			if serializer.is_valid():
				blog_post = serializer.save()
				data['response'] = CREATE_SUCCESS
				data['pk'] = blog_post.pk
				data['title'] = blog_post.title
				data['body'] = blog_post.body			
				data['created_at'] = blog_post.date_updated
				image_url = str(request.build_absolute_uri(blog_post.image.url))
				if "?" in image_url:
					image_url = image_url[:image_url.rfind("?")]
				data['image'] = image_url
				data['username'] = blog_post.author.username
				return Response(data=data)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMyBlogPost(generics.GenericAPIView):	
	serializer_class=BlogPostCreateSerializer
	parser_classes = (FormParser, MultiPartParser)
	queryset = BlogPost.objects.all()	
	def get(self, request, pk,format=None):     
		account=get_object(pk)		     
		serializer=BlogPostCreateSerializer(account)
		return Response(serializer.data)

class UpdatePostView(generics.GenericAPIView):	       
	pauthentication_classes=[TokenAuthentication]       
	permission_classes=[IsAuthenticated]
	parser_classes = (FormParser, MultiPartParser)
	serializer_class=BlogPostCreateSerializer
	queryset = BlogPost.objects.all()	
	def put(self, request, pk,format=None):     
		account=get_object(pk)
		data={} 
		user = request.user
		if account.author != user:
			data['response'] = "You don't have permission to edit this post"
			return Response(data=data)  
		if request.method == 'PUT':
			serializer = BlogPostCreateSerializer(account, data=request.data, partial=True)
			data = {}
			if serializer.is_valid():
				serializer.save()
				data['response'] = UPDATE_SUCCESS
				data['pk'] = account.pk
				data['title'] = account.title
				data['body'] = account.body				
				data['date_updated'] = account.date_updated
				image_url = str(request.build_absolute_uri(account.image.url))
				if "?" in image_url:
					image_url = image_url[:image_url.rfind("?")]
				data['image'] = image_url
				data['username'] = account.author.username
				return Response(data=data)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePost(generics.GenericAPIView):
	authentication_classes=[TokenAuthentication]       
	permission_classes=[IsAuthenticated]
	parser_classes = (FormParser, MultiPartParser)
	serializer_class=BlogPostCreateSerializer
	queryset = BlogPost.objects.all()	
	def delete(self, request, pk,format=None):     
		account=get_object(pk)		
		user = request.user
		if account.author != user:
			return Response({"response":"You don't have permission to delete the post"})
		if request.method == 'DELETE':
			operation = account.delete()
			data = {}
			if operation:
				data['response'] = DELETE_SUCCESS
			return Response(data=data)
