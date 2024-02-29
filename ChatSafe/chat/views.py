from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import (
    MinimumLengthValidator, CommonPasswordValidator,
    NumericPasswordValidator, UserAttributeSimilarityValidator
)


def home(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.success(request, 'Invalid Username or Password, Please Try Again.')
            return redirect('home')
    
    if request.user.is_authenticated:
        if Chat.objects.filter(users=request.user).exists():
            q = request.GET.get('q') if request.GET.get('q') != None else ''
            
            chats = Chat.objects.filter(users=request.user)
            if q is not "" or None:
                if User.objects.filter(username=q).exists():
                    searched_user = User.objects.get(username=q)
                    if searched_user:
                        chats = chats.filter(users=searched_user)
        else:
            chats = []
    else:
            chats = []
    context = {
        'chats': chats,
    }


    return render(request, 'chat/home.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            messages.success(request, "Username taken.")
        else:
            if password1 == password2:
                validate_password_manually(password1)
                user = User.objects.create_user(username=username, password=password1, email=email)
                # user.save()
                login(request, user)
                messages.success(request, f'Account Created Successfully. Welcome {username}')
                return redirect('home')
            else:
                messages.success(request, "Passwords don't match")
    return render(request, 'chat/signup.html')


@login_required(login_url='home')
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect('home')




@login_required(login_url='home')
def chat_view(request, pk):
    chat = Chat.objects.get(id=pk)
    messages = Message.objects.filter(chat=chat)

    if request.method == "POST":
        body = request.POST['body']
        Message.objects.create(user=request.user, chat=chat, body=body)

    context = {
        'body_messages': messages,
    }
    return render(request, 'chat/chat.html', context)

@login_required(login_url='home')
def new_chat(request, pk):
    if pk == 0:
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        if q is not "" or None:
            if User.objects.filter(username=q).exists():
                user = User.objects.get(username=q)  
            else:
                user = None
        else:
            user = None   

    else:
        user = None 
        if Chat.objects.filter(users=request.user).exists():
            chat = Chat.objects.filter(users=request.user)
            if chat.filter(users=(User.objects.get(id=pk))).exists():
                chat = chat.get(users=(User.objects.get(id=pk)))
                return redirect('chat', pk=chat.id)
            else:
                chat = Chat.objects.create(user1=request.user, user2=User.objects.get(id=pk))
                chat.save()
                chat.users.add(request.user)
                chat.users.add(User.objects.get(id=pk))
                chat.save()
                return redirect('chat', pk=chat.id)
        else:
                chat = Chat.objects.create(user1=request.user, user2=User.objects.get(id=pk))
                chat.save()
                chat.users.add(request.user)
                chat.users.add(User.objects.get(id=pk))
                chat.save()
                return redirect('chat', pk=chat.id)


    context = {
        "user": user,
    }

    return render(request, "chat/new_chat.html", context)


@login_required
def videocall(request):
    return render(request, 'chat/videocall.html', {"name": request.user.username})

def validate_password_manually(password):
    validators = [
        MinimumLengthValidator(),
        CommonPasswordValidator(),
        NumericPasswordValidator(),
        UserAttributeSimilarityValidator(),
    ]

    errors = []
    for validator in validators:
        try:
            validator.validate(password)
        except ValidationError as e:
            errors.extend(e.messages)

    if errors:
        raise ValidationError(errors)
