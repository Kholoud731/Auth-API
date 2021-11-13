from django.contrib import admin
from django.urls import path
from .views import hello_world, movies, create_movie,update_movie, delete_movie, signup, get_token, logout
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('home/', hello_world, name='home'),
    path('movies/', movies, name='movies'),
    path('create/', create_movie, name='create'),
    path('update/<int:id>', update_movie, name='update'),
    path('delete/<int:id>', delete_movie, name='delete'),
    path('signup/', signup, name='signup'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), # login auth returns token
    path('signup/<int:id>', get_token, name='signup'),
    path('logout/', logout, name='logout'),

]


