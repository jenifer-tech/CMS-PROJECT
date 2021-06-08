from rest_framework import serializers

from account.models import Account

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields=['id','username','email','password','gender','dateOfBirth',
        'phoneNumber','state','city','address']
        extra_kwargs = {
                'password': {'write_only': True},
        }   

    def save(self):

        account = Account(
                    username    =self.validated_data['username'],
                    email       =self.validated_data['email'],                    
                    gender      =self.validated_data['gender'],             
                    dateOfBirth =self.validated_data['dateOfBirth'],                    
                    phoneNumber =self.validated_data['phoneNumber'], 
                    state       =self.validated_data['state'], 
                    city        =self.validated_data['city'], 
                    address     =self.validated_data['address'],                                             
                )
        password = self.validated_data['password']        
        account.set_password(password)
        account.save()
        return account

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    class Meta:
        model = Account
        fields = ['email', 'password']

class AccountPropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ['pk', 'username', 'email', ]

class UpdateAccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields=['pk','username','phoneNumber','gender','dateOfBirth','state','city','address']

class CreateAccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields='__all__'
class ChangePasswordSerializer(serializers.Serializer):
    
	old_password 				= serializers.CharField(required=True)
	new_password 				= serializers.CharField(required=True)
	confirm_new_password 		= serializers.CharField(required=True)

