from django.urls import path
from . import views
from .models import Room


urlpatterns =[
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.registerUser, name = 'register'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('', views.HomePage, name= "Home"),
    path('room/<str:pk>/', views.room, name='room'),
    path(route='profile/<str:pk>', view= views.userProfile, name= 'profile'),
    path(route='create-room/', view= views.createRoom, name= 'create-room'),
    path(route='update-room/<str:pk>', view=views.updateRoom, name= 'update-room'),
    path(route= 'delete-room/<str:pk>', view=views.deleteRoom, name='delete-room'),
    path(route= 'delete-message/<str:pk>', view=views.deleteMessage, name='delete-message'),
    path(route= 'update-user/', view=views.updateUser, name='update-user'),
    path(route= 'topics/', view=views.topicsPage, name='topics'),
    path(route= 'activity/', view=views.activityPage, name='activity')
]