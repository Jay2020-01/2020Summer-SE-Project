import requests
from django.shortcuts import render
from django.db.models.signals import post_save
from django.http import JsonResponse
from backend.models import User, UserProfile
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
    username = request.POST.get("username")
    password = request.POST.get("password")
    data = {'token': None, 'user': username}
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse(data)
    if password == user.password:
        token = Token.objects.get(user=user)
        data['token'] = str(token)
    return JsonResponse(data)


def register(request):
    username = request.POST.get("username")
    mail_address = request.POST.get("mail_address")
    password = request.POST.get("password")
    data = {'token': None, 'user': username}
    if not User.objects.filter(username=username):
        user = User.objects.create(username=username, email=mail_address, password=password)
        UserProfile.objects.create(user=user)
        token = Token.objects.get(user=user)
        data = {'token': str(token), 'user': username}
    return JsonResponse(data)
