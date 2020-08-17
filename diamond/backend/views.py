from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from login.views import authentication
# my models
from .models import User, Document, Team, TeamUser, Comment
# third-party
from rest_framework.authtoken.models import Token
from notifications.signals import notify


# Create your views here.


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
    print('pull user info')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    data = {'username': user.username,
            'mail_address': user.email,
            'phone_number': user.phone_number,
            'wechat': user.wechat,
            'password': user.password}
    return JsonResponse(data)


# 新建文档
def create_doc(request):
    print('create doc')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    name = request.POST.get("title")
    # content = request.POST.get("content")
    # create_time = request.POST.get("create_time")
    print(name)
    # print(content)
    doc = Document.objects.create(creator=user, name=name, in_group=False)
    print(doc.name)
    print(doc.pk)
    data = {'flag': "yes", 'doc_id': doc.pk, 'msg': "create success"}
    print("success")
    return JsonResponse(data)


# 保存文档内容
def save_doc(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    print('save doc')
    content = request.POST.get("content")
    doc_id = request.POST.get("doc_id")
    # create_time = request.POST.get("modified_time")
    print(content)
    print(doc_id)
    doc = Document.objects.get(creator=user, pk=doc_id)
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
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    print("get doc")
    doc_id = request.POST.get("doc_id")
    print(doc_id)
    document = Document.objects.get(creator=user, pk=doc_id)
    data = {'name': document.name, 'content': document.content}
    print("success")
    return JsonResponse(data)


# 我创建的
def my_doc(request):
    print('my docs')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    documents = Document.objects.filter(creator=user)
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
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    team_name = request.POST.get("name")
    team = Team.objects.create(team_name=team_name)
    TeamUser.objects.create(team=team, user=user, is_leader=True)
    return JsonResponse({})


# 搜索用户
def search_user(request):
    print('search user')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    name = request.POST.get("name")
    print("key word", name)
    if name == "":
        users = User.objects.all()
    else:
        users = User.objects.filter(
            Q(username__icontains=name)
        )
    user_list = []
    for user in users:
        item = {"username": user.username, "password": user.password, "wechat": user.wechat,
                "phone_number": user.phone_number, "email": user.email}
        user_list.append(item)
    data = {"user_list": user_list}

    return JsonResponse(data)


# 拉取用户所有的团队
def get_my_team(request):
    print('get my team')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    team_user = TeamUser.objects.filter(user=user)
    team_list = []
    for relation in team_user:
        item = {'team_name': relation.team.team_name, 'team_id': relation.team.id,
                "introduction": relation.team.introduction, "is_leader": relation.is_leader}
        team_list.append(item)
    data = {"team_list": team_list}
    return JsonResponse(data)


def delete_my_team(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    team_id = request.POST.get("team_id")
    print(team_id)
    team = Team.objects.get(id=team_id)
    team.delete()
    return JsonResponse({})


# 拉取某团队队内成员
def get_team_member(request):
    print("get team list")
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    team_id = request.GET.get("team_id")
    team = Team.objects.get(id=team_id)
    team_user = TeamUser.objects.filter(team=team)
    user_list = []
    for relation in team_user:
        user_list.append(relation.user)
    data = {'user_list': user_list}
    return JsonResponse(data)


# 邀请团队成员,强制邀请 TODO 使用消息通知实现
def add_team_member(request):
    print("add team member")
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    team_id = request.GET.get("team_id")
    team = Team.objects.get(id=team_id)
    TeamUser.objects.create(team=team, user=user, is_leader=False)
    return JsonResponse({})


# 发送邀请
def send_invitation(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)

    actor = User.objects.get(id=request.POST.get("actor_id"))
    recipient = User.objects.get(id=request.POST.get("recipient_id"))
    verb = 'invate'
    target = Team.objects.get(id=request.POST.get("team_id"))

    data = {}

    notify.send(actor, recipient, verb, target)
    return JsonResponse(data)


# 接受邀请
def accept_invitation(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    # 获取团队
    team = Team.objects.get(id=request.POST.get("team_id"))
    # User作为组员加入团队
    TeamUser.objects.create(user=user, team=team, is_leader=False)
    return JsonResponse({})


# 获取未读信息
def get_user_unread_notice(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    unread_notice = user.notifications.unread()
    notice_list = []
    for notice in unread_notice:
        item = {
            'actor': notice.User.username,
            'verb': notice.CharField,
            'target_id': notice.target.id,
        }
        notice_list.append(item)
    data = {"notice_list": notice_list}
    return JsonResponse(data)


# 上传评论
def post_comment(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    # 获取被评论的文档id
    document = Document.objects.get(id=request.POST.get("doc_id"))
    # 获取评论内容
    body = request.POST.get("body")
    # 存储评论
    Comment.objects.create(user=user, document=document, body=body)
    data = {}
    return JsonResponse(data)


# 文章获取评论列表
def get_comment_list(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    # 获取被评论的文档id
    document = Document.objects.get(id=request.POST.get("doc_id"))
    # 获取评论
    comments = Comment.objects.filter(document=document)
    # 返还评论列表
    comment_list = []
    for comment in comments:
        item = {
            'actor': comment.user.username,
            'body': comment.body,
        }
        comment_list.append(item)

    data = {"comment_list": comment_list}
    return JsonResponse(data)
