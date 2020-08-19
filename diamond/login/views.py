import requests
from django.shortcuts import render
from django.db.models.signals import post_save
from django.http import JsonResponse
from backend.models import User
from django.http import JsonResponse, HttpResponse
from rest_framework.authtoken.models import Token
from django.conf import settings
from rest_framework.authtoken import views
from django.dispatch import receiver
from diamond import settings
from diamond.settings import DEPLOY
import os
import re

if DEPLOY:
    ABSOLUTE_URL = "http://121.41.231.2:80"
else:
    ABSOLUTE_URL = "http://127.0.0.1:8000"


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def authentication(request):
    token_str = request.META.get("HTTP_AUTHORIZATION")
    try:
        token = Token.objects.get(key=token_str)
    except:
        return None
    user = User.objects.get(id=token.user_id)
    return user


# Create your views here.
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    data = {'token': None, 'user': username, 'success': False}
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse(data)
    if password == user.password:
        token = Token.objects.get(user=user)
        data['token'] = str(token)
        data['success'] = True
    return JsonResponse(data)


def register(request):
    username = request.POST.get("username")
    mail_address = request.POST.get("mail_address")
    password = request.POST.get("password")
    data = {'token': None, 'message':"用户名已被注册",'success':False}
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", mail_address) == None:
        data = {'token': None, 'message': "邮箱地址错误", 'success':False}
        return JsonResponse(data)
    if not User.objects.filter(username=username):
        user = User.objects.create(username=username, email=mail_address, password=password)
        token = Token.objects.get(user=user)
        data = {'token': str(token), 'message': "注册成功", 'success':True}
    return JsonResponse(data)


# Create your views here.
def writeFile(file_path, file):
    with open(file_path, "wb") as f:
        if file.multiple_chunks():
            for content in file.chunks():
                f.write(content)
        else:
            data = file.read()
            f.write(data)


def user_avatar_upload(request):
    user = authentication(request)
    if user is None:
        print("user is NOne")
        return HttpResponse('Unauthorized', status=401)
    print(str(user.username) + "is uploading avatar image")
    if request.method == "POST":
        fileDict = request.FILES.items()
        # 获取上传的文件，如果没有文件，则默认为None
        if not fileDict:
            return JsonResponse({'msg': 'no file upload'})
        for (k, v) in fileDict:
            print("dic[%s]=%s" % (k, v))
            fileData = request.FILES.getlist(k)
            for file in fileData:
                fileName = str(user.username) + "_" + file._get_name()
                filePath = os.path.join(settings.MEDIA_ROOT, "user_avatar", fileName)
                print('filepath = [%s]' % filePath)
                try:
                    user.avatar = "user_avatar/" + fileName
                    user.save()
                    writeFile(filePath, file)
                except:
                    return JsonResponse({'msg': 'file write failed'})
        return JsonResponse({'msg': 'success'})


# 修改用户信息.
def change_info(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)

    user.username = request.POST.get("username")
    user.email = request.POST.get("mail_address")
    user.password = request.POST.get("password")
    user.wechat = request.POST.get("wechat")
    user.phone_number = request.POST.get("phone_number")
    user.save()
    return JsonResponse({})


# 拉取用户信息
def user_info(request):
    # print('pull user info')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    # print(user.avatar.url)
    data = {'username': user.username,
            'mail_address': user.email,
            'phone_number': user.phone_number,
            'wechat': user.wechat,
            'password': user.password,
            'url': ABSOLUTE_URL + user.avatar.url}
    return JsonResponse(data)
