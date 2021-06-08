from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import RegisterSerializer,LoginSerializer, ChangePasswordSerializer,AccountPropertiesSerializer,UpdateAccountSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from account.models import Account
from account.validation import validate_email,validate_username
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser
from account.utils import get_object

class RegisterView(generics.GenericAPIView):
	serializer_class = RegisterSerializer
	parser_classes = (FormParser, MultiPartParser)
	def post(self,request):
		
		data = {}
		username    =   request.data.get('username')        
		email       =   request.data.get('email')     
		
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data,status=status.HTTP_400_BAD_REQUEST)

		
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data,status=status.HTTP_400_BAD_REQUEST) 


		serializer=RegisterSerializer(data=request.data)
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email			
			data['password']=account.password
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

class LoginView(generics.GenericAPIView):
	authentication_classes = []
	permission_classes = []	
	serializer_class = LoginSerializer
	parser_classes = (FormParser, MultiPartParser)

	def post(self, request):		
		serializer = LoginSerializer(data=request.data)
		context = {}
		if serializer.is_valid():
			email = request.POST.get('email')
			password = request.POST.get('password')			
			account = authenticate(email=email, password=password)			
			if account:
				try:
					token = Token.objects.get(user=account)
				except Token.DoesNotExist:
					token = Token.objects.create(user=account)
				context['response'] = 'Successfully authenticated.'
				context['pk'] = account.pk
				context['email'] = email.lower()
				context['token'] = token.key
			else:
				context['response'] = 'Error'
				context['error_message'] = 'Invalid credentials'
		return Response(context)

class ChangePasswordView(UpdateAPIView):
	serializer_class = ChangePasswordSerializer
	model = Account
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	parser_classes = (FormParser, MultiPartParser)
	
	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

			
			new_password = serializer.data.get("new_password")
			confirm_new_password = serializer.data.get("confirm_new_password")
			if new_password != confirm_new_password:
				return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

			
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(generics.GenericAPIView):
	authentication_classes=[TokenAuthentication]       
	permission_classes=[IsAuthenticated]
	serializer_class=RegisterSerializer
	queryset = Account.objects.all()
	parser_classes = (FormParser, MultiPartParser)
	def get(self, request, pk,format=None):     
		account=get_object(pk)      
		serializer=RegisterSerializer(account)
		return Response(serializer.data)

class ChangeUserDetail(generics.GenericAPIView):	       
	permission_classes=[IsAuthenticated]
	authentication_classes=[TokenAuthentication]
	serializer_class=UpdateAccountSerializer
	queryset = Account.objects.all()
	parser_classes = (FormParser, MultiPartParser)

	def put(self,request,pk,format=None):
		account=get_object(pk)
		serializer=UpdateAccountSerializer(account,data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DeleteUser(APIView): 
	permission_classes=[IsAuthenticated]
	authentication_classes=[TokenAuthentication]
	serializer_class=UpdateAccountSerializer
	queryset = Account.objects.all()
	parser_classes = (FormParser, MultiPartParser)	
	def delete(self,request,pk,format=None): 
		account=get_object(pk)
		account.delete()
		return Response(status=status.HTTP_204_NO_CONTENT) 


class AccountAPIView(generics.ListAPIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[TokenAuthentication]    
	queryset = Account.objects.all()
	serializer_class = RegisterSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['id','username', 'phoneNumber','email','state']

