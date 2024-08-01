from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from . models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# rooms = [
#     {'ID':1, 'name': 'Code with Python'},
#     {'ID':2, 'name': 'Code with java'},
#     {'ID':3, 'name': 'Code with C'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email= email )
        except:
            messages.error(request, 'User doesnt exists')
        
        user = authenticate(request, email= email, password= password)
        if user:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Userid and Password not matching')


    context = {'page': page}
    return render(request,'baseapp/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('Home')

def registerUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'An error occured during registration, Try again')
    return render(request, 'baseapp/login_register.html', {'form': form})

def HomePage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains=q) |
        Q(descr__icontains=q)  )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains= q)) #SHOW ACTIVITY BASED ON ROOM SELECTED
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_message': room_message}
    return render(request, 'baseapp/homepage.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user= request.user,
            room= room,
            body= request.POST.get('body') 
        )
        room.participants.add(request.user)
        return redirect('room', pk= room.id)
    contexts = {'rooms': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'baseapp/room.html', contexts)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_message': room_message, 'topics': topics}
    return render(request, 'baseapp/profile.html', context)

@login_required(login_url= 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            descr = request.POST.get('descr')
        )
        return redirect('Home')

    context = {'form': form, 'topics': topics}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url= 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not authorized for this action')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.descr = request.POST.get('descr')
        room.save()
        return redirect('Home')
    context = {'form': form,'topics': topics, room: 'room'}   
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url= 'login')
def deleteRoom(request, pk):
    room = Room.objects.get(id= pk)

    if request.user != room.host:
        return HttpResponse('You are not authorized for this action')

    if request.method == 'POST':
        room.delete()
        return redirect('Home')
    return render(request, 'baseapp/delete.html', { 'obj' : room})

@login_required(login_url= 'login')
def deleteMessage(request,pk):
    message = Message.objects.get(id= pk)
    if request.user != message.user:
        return HttpResponse('You are not authorized for this action')

    if request.method == 'POST':
        message.delete()
        return redirect('Home')
    return render(request, 'baseapp/delete.html', { 'obj' : message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'baseapp/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name_icontains=q)
    return render(request, 'baseapp/topics.html',{'topics': topics})


def activityPage(request):
    room_message = Message.objects.all()
    return render(request, 'baseapp/activity.html', {'room_message': room_message})
