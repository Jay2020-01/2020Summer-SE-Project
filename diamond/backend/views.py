from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import User, UserProfile, Document
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

def newdoc(request):
    print("newdoc")
    name = request.POST.get("title")
    content = request.POST.get("content")
    document = Document(name = name, content = content)
    print(name)
    print(content)
    # document.save()
    data = {'flag': "yes", 'msg': "some infos"}
    return JsonResponse(data)