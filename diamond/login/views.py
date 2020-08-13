import requests
from django.shortcuts import render
from django.db.models.signals import post_save
from django.http import JsonResponse
from backend.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.authtoken import views
from django.dispatch import receiver


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your views here.
def login(request):
    print("login")
    print("header : " + str(request.META.get("HTTP_API_AUTH")))
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username)
    print(password)
    print(User.objects.all())
    try:
        user = User.objects.get(username=username)
    except:
        data = {'flag': 'no', "msg": "unregisterd"}
        print('login fail')
        return JsonResponse({'request': data})
    if password == user.password:
        data_msg = "success"
        data_flag = "yes"
    else:
        data_msg = "wrong password"
        data_flag = "no"
    data = {'flag': data_flag, 'msg': data_msg}
    print('login success')
    return JsonResponse({'request': data})


def register(request):
    print("register")
    username = request.POST.get("username")
    mail_address = request.POST.get("mail_address")
    password = request.POST.get("password")
    if User.objects.filter(mail_address=mail_address):
        data = {'flag': 'no'}
    else:
        user = User(username=username, mail_address=mail_address, password=password)
        user.save()
        token = Token.objects.get(user=user)
        data = {'token': str(token), 'user': username}
        print(str(token))
    return JsonResponse(data)
