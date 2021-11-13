from rest_framework import serializers
from pin.models import Movie
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        ) 
        if self.validated_data.get('password') != self.validated_data.get('password2'):
           raise serializers.ValidationError(
                {
                   'password': "Password doesn't match"
               }
           )

        user.set_password(validated_data['password']) 
        user.save()
        return user  


class MovieSerializer(serializers.ModelSerializer):
    casts = serializers.StringRelatedField(many=True)
    Categories = serializers.StringRelatedField(many=True)
    class Meta:
          model = Movie
          fields = '__all__'