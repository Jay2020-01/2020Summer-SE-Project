from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from django.http import JsonResponse
from .models import User, UserProfile, Document, Group, GroupProfile
from rest_framework.authtoken.models import Token
from django.core import serializers


# 修改用户信息.
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


# 拉取用户信息
def user_info(request):
    print('pull user info')
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


# 新建文档
def create_doc(request):
    print('create doc')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    name = request.POST.get("title")
    # content = request.POST.get("content")
    # create_time = request.POST.get("create_time")
    print(name)
    # print(content)
    doc = Document.objects.create(creater=user, name=name, in_group = False)
    print(doc.name)
    print(doc.pk)
    data = {'flag': "yes", 'doc_id': doc.pk , 'msg': "create success"}
    print("success")
    return JsonResponse(data)


# 保存文档内容
def save_doc(request):
    print('save doc')
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    content = request.POST.get("content")
    doc_id = request.POST.get("doc_id")
    # create_time = request.POST.get("modified_time")
    print(content)
    print(doc_id)
    doc = Document.objects.get(creater=user, pk=doc_id)
    print(doc.name)
    print(doc.content)
    print(doc.pk)
    doc.content = content
    doc.save()
    print(doc.content)
    data = {'flag': "yes", 'msg': "modified success"}
    # print("success")
    return JsonResponse(data)


# 获取文档内容
def get_doc(request):
    print("get doc")
    token_str = request.META.get("HTTP_AUTHORIZATION")
    token = Token.objects.get(key=token_str)
    user = User.objects.get(id=token.user_id)
    doc_id = request.POST.get("doc_id")
    print(doc_id)
    document = Document.objects.get(creater=user, pk=doc_id)
    data = {'name': document.name, 'content': document.content}
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
            # 'content': d.content,
            'doc_id': d.pk,
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
    team = Group.objects.create(name=team_name)
    GroupProfile.objects.create(Group=team, leader=user)
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
