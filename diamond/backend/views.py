from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from login.views import authentication
from datetime import datetime

# my models
from .models import User, Document, Team, TeamUser, Comment, Collection
# third-party
from notifications.models import Notification
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


#收藏文件
def collect_doc(request):
    print("collect doc")
    doc_id = request.POST.get("doc_id")
    print(doc_id)
    user = authentication(request)
    doc = Document.objects.get(pk=doc_id)
    data = {'flag': "no",  'msg': "already collect"}
    if not Collection.objects.filter(Q(user=user)&Q(doc=doc)):
        Collection.objects.create(user=user,doc=doc)
        data = {'flag': "yes",  'msg': "collect success"}
    print("success")
    return JsonResponse(data)

# 取消收藏
def uncollect_doc(request):
    print("uncollect doc")
    doc_id = request.POST.get("doc_id")
    print(doc_id)
    user = authentication(request)
    doc = Document.objects.get(pk=doc_id)
    collection = Collection.objects.get(Q(user=user)&Q(doc=doc))
    collection.delete()
    data = {'flag': "yes",  'msg': "uncollect success"}
    print("success")
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
    created_documents = Document.objects.filter(creator=user)
    created_docs = []
    collections = Collection.objects.filter(user=user)
    collected_docs = []
    for d in created_documents:
        c_item = {
            'name': d.name,
            # 'content': d.content,
            'doc_id': d.pk,
        }
        created_docs.append(c_item)
    for d in collections:
        c_item = {
            'name': d.doc.name,
            # 'content': d.content,
            'doc_id': d.doc.pk,
        }
        collected_docs.append(c_item)
    data = {'created_docs':created_docs, 'collected_docs':collected_docs}
    return JsonResponse(data)


# 发送邀请
def invite_user(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    actor = user
    recipient = User.objects.get(username=request.POST.get("username"))
    print(request.POST.get("username"))
    verb = 'invite'
    team = Team.objects.get(id=request.POST.get("team_id"))
    print(team)
    data = {}
    notify.send(actor, recipient=recipient, verb=verb, target=team)
    return JsonResponse(data)


# 回复邀请
def response_invitation(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    notice_id = request.POST.get("notice_id")
    if request.POST.get("answer")=='Yes':
        # 用户接受邀请
        # 获取团队
        team = Team.objects.get(id=request.POST.get("team_id"))
        # User作为组员加入团队
        TeamUser.objects.create(user=user, team=team, is_leader=False)
    elif request.POST.get("answer")=='No':
        # 用户拒绝邀请
        Notification.objects.get(notice_id).delete()
    else:
        print('There must be something wrong with the data!')

    
    return JsonResponse({})




# 获取未读信息
def get_user_notice(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    unread_notice = user.notifications.unread()
    notice_list = []
    for notice in unread_notice:
        team  = notice.target
        actor = notice.actor
        item = {
            'notice_id': notice.id,
            'actor_id': actor.id,
            'actor_name':actor.username,
            'verb': notice.CharField,
            'target_id': team.id,
            'target_name': teamname,
            'sent_time': datetime.strftime(notice.timestamp, '%Y-%m-%d-%H-%M-%S-%A'),
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
