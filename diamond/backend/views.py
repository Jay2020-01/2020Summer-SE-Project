from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from django.http import JsonResponse
from .models import User, Document, Team, TeamUser
from rest_framework.authtoken.models import Token
from django.core import serializers


# 修改用户信息.
def change_info(request):
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)

    user.username = request.POST.get("username")
    user.email = request.POST.get("mail_address")
    user.password = request.POST.get("password")
    user.wechat = request.POST.get("wechat")
    user.phone_number = request.POST.get("phone_number")
    user.save()
    return JsonResponse({})


# 拉取用户信息
def user_info(request):
    print('pull user info')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    data = {'username': user.username,
            'mail_address': user.email,
            'phone_number': user.phone_number,
            'wechat': user.wechat,
            'password': user.password}
    return JsonResponse(data)


# 新建文档
def create_doc(request):
    print('create doc')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    name = request.POST.get("title")
    content = request.POST.get("content")
    Document.objects.create(creator=user, name=name, content=content, in_group=False)
    data = {'flag': "yes", 'msg': "create success"}
    print("success")
    return JsonResponse(data)


# 我创建的
def my_doc(request):
    print('my docs')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    documents = Document.objects.filter(creater=user)
    all_doc = []
    for d in documents:
        c_item = {
            'name': d.name,
            'content': d.content,
        }
        all_doc.append(c_item)
    return JsonResponse({'data': all_doc})


# 新建团队
def create_team(request):
    print('create team')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    team_name = request.POST.get("name")
    team = Team.objects.create(team_name=team_name)
    TeamUser.objects.create(team=team, user=user, is_leader=True)
    return JsonResponse({})


# 搜索用户
def search_user(request):
    print('search user')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    name = request.POST.get("name")
    print("key word", name)
    if name == "":
        user_list = User.objects.all()
    else:
        user_list = User.objects.filter(
            Q(username__icontains=name)
        )
    data = {"user_list": serializers.serialize('json', user_list)}

    return JsonResponse(data)


# 拉取用户所有的团队
def get_my_team(request):
    print('get my team')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    team_user = TeamUser.objects.filter(user=user)
    team_list = []
    for relation in team_user:
        team_list.append(relation.team)
    data = {"team_list": team_list}
    return JsonResponse(data)
