from django.urls import path
from . import views

urlpatterns =[
    path('', views.getRoutes ),
    path(route='rooms/', view= views.getRooms),
    path(route='rooms/<str:pk>/', view= views.getRoom)
]