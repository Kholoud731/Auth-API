from django.db import models
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from .serializers import MovieSerializer, UserSerializer
from pin.api.v1 import serializers
from pin.models import Movie
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from pin.permissions import  Can_delete


@api_view(['GET', 'POST']) # login function 
def signup(request):
    if request.method == 'GET': # made to test the get with the post for the same path
        data_users = User.objects.all()
        users = UserSerializer(data_users, many=True)

        return Response(data=users.data)
    elif request.method == 'POST':
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            users = User.objects.get(id = user.data['id'])
            token= Token.objects.create(user=users)
            print(token.key)
            return Response({'msg':'User Created!', 'token':token.key})
        return Response(data=user.errors, status=status.HTTP_400_BAD_REQUEST)      

# test the token manually 
@api_view(['GET'])
def get_token(request, id):
        data_users = User.objects.get(id = id)
        users = UserSerializer(data_users)
        print(Token.objects.get(user= data_users.id))
        return Response(data=users.data)
        
'''on logout we delete the token and recreate a new one 
will ba accesssed only when the user login with the correct username and passeord'''
        
@api_view(["GET"])  
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout(request):
    print(request.user.auth_token)
    print(request.user.id)
    request.user.auth_token.delete()
    users = User.objects.get(id = request.user.id)
    token= Token.objects.create(user=users)
    print(token.key)
    return Response({'msg': 'Logged out'}, status=status.HTTP_200_OK)






@api_view(["GET", "POST"])  
def hello_world(request):
     if request.method == 'POST':
         return Response(
            {'message': 'Post request-Response'}, status=status.HTTP_201_CREATED)
     return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)
 
@api_view(["GET"])  
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def movies(request):

    movies = Movie.objects.all()
    serializer = serializers.MovieSerializer(instance=movies, many=True)
    return Response(data= serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])  
def create_movie(request):
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT","PATCH"])  
def update_movie(request, id):
    if request.method == 'PUT':
        movie = Movie.objects.filter(id = id).first()
        serializer = MovieSerializer(instance = movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PATCH':
        movie = Movie.objects.filter(id = id).first()
        serializer = MovieSerializer(instance = movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])  
@permission_classes([Can_delete])
def delete_movie(request, id):
    movie = Movie.objects.get(id = id)
    movie.delete() 

    movies = Movie.objects.all()
    serializer = serializers.MovieSerializer(instance=movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)