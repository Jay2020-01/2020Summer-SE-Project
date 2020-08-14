from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import User, UserProfile, Document, Group, GroupProfile
from rest_framework.authtoken.models import Token


# Create your views here.
def change_info(request):
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    user_profile = UserProfile.objects.get(user=user)

    user.username = request.POST.get("username")
    user.email = request.POST.get("mail_address")
    user.password = request.POST.get("password")
    user_profile.wechat = request.POST.get("wechat")
    user_profile.phone_number = request.POST.get("phone_number")

    user.save()
    user_profile.save()
    return JsonResponse({})


def user_info(request):
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    user_profile = UserProfile.objects.get(user=user)
    data = {'username': user.username,
            'mail_address': user.email,
            'phone_number': user_profile.phone_number,
            'wechat': user_profile.wechat,
            'password': user.password}
    return JsonResponse(data)


def create_doc(request):
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    name = request.POST.get("title")
    content = request.POST.get("content")
    Document.objects.create(creator=user, name=name, content=content)
    data = {'flag': "yes", 'msg': "create success"}
    print("success")
    return JsonResponse(data)


def create_team(request):
    print('create team')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    team_name = request.POST.get("name")
    team = Group.objects.create(name=team_name)
    GroupProfile.objects.create(Group=team, leader=user)
    return JsonResponse({})
