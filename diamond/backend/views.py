from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from login.views import authentication
from datetime import datetime

# my models
from .models import User, Document, Team, TeamUser, Comment, Collection, Delete_document
# third-party
from notifications.models import Notification
from notifications.signals import notify
from diamond import settings
from diamond.settings import MEDIA_URL
import os

ABSOLUTE_URL = "http://127.0.0.1:8000"


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
    print()
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    if request.method == "POST":
        fileDict = request.FILES.items()
        # 获取上传的文件，如果没有文件，则默认为None
        if not fileDict:
            return JsonResponse({'msg': 'no file upload'})
        for (k, v) in fileDict:
            print("dic[%s]=%s" % (k, v))
            fileData = request.FILES.getlist(k)
            for file in fileData:
                fileName = file._get_name()
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
    print('pull user info')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    print(user.avatar.url)
    data = {'username': user.username,
            'mail_address': user.email,
            'phone_number': user.phone_number,
            'wechat': user.wechat,
            'password': user.password,
            'url': ABSOLUTE_URL + user.avatar.url}
    return JsonResponse(data)


# 删除文档
def delete_doc(request):
    print("delete doc")
    doc_id = request.POST.get("doc_id")
    user = authentication(request)
    try:
        doc = Document.objects.get(pk=doc_id)
        if user == doc.creator:
            delete_doc = Delete_document.objects.create(creator=doc.creator, team=doc.team, in_group=doc.in_group,
                                                        name=doc.name, content=doc.content,
                                                        created_date=doc.created_date, modified_date=doc.modified_date)
            doc.delete()
            data = {'flag': "yes", 'delete_doc_id': delete_doc.pk}
            print("success")
    except expression as identifier:
        data = {'flag': "no"}
    return JsonResponse(data)


# 拉取已被删除在回收站的文档
def get_deleted_docs(request):
    print("get deleted docs")
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    deleted_documents = Delete_document.objects.filter(creator=user)
    deleted_docs = []
    for doc in deleted_documents:
        item = {
            'name': doc.name,
            'doc_id': doc.pk,
        }
        deleted_docs.append(item)
    data = {'deleted_docs': deleted_docs}
    return JsonResponse(data)


# 还原文件
def restore_doc(request):
    print("restore")
    delete_doc_id = request.POST.get("doc_id")
    user = authentication(request)
    delete_doc = Delete_document.objects.get(pk=delete_doc_id)
    data = {'flag': "no"}
    if user == delete_doc.creator:
        doc = Document.objects.create(creator=delete_doc.creator, team=delete_doc.team, in_group=delete_doc.in_group,
                                      name=delete_doc.name,
                                      content=delete_doc.content, created_date=delete_doc.created_date,
                                      modified_date=delete_doc.modified_date)
        delete_doc.delete()
        data = {'flag': "yes", 'doc_id': doc.pk}
    return JsonResponse(data)


# 彻底删除文件
def delete_doc_completely(request):
    print("delete doc completely")
    delete_doc_id = request.POST.get("doc_id")
    user = authentication(request)
    delete_doc = Delete_document.objects.get(pk=delete_doc_id)
    data = {'flag': "no"}
    if user == delete_doc.creator:
        delete_doc.delete()
        data = {'flag': "yes"}
    return JsonResponse(data)


# 收藏文件
def collect_doc(request):
    print("collect doc")
    doc_id = request.POST.get("doc_id")
    # print(doc_id)
    user = authentication(request)
    doc = Document.objects.get(pk=doc_id)
    data = {'flag': "no", 'msg': "already collected"}
    if not Collection.objects.filter(Q(user=user) & Q(doc=doc)):
        Collection.objects.create(user=user, doc=doc)
        data = {'flag': "yes", 'msg': "collect success"}
    # print("success")
    return JsonResponse(data)


# 取消收藏
def uncollect_doc(request):
    print("uncollect doc")
    doc_id = request.POST.get("doc_id")
    print(doc_id)
    user = authentication(request)
    doc = Document.objects.get(pk=doc_id)
    collection = Collection.objects.get(Q(user=user) & Q(doc=doc))
    collection.delete()
    data = {'flag': "yes", 'msg': "uncollect success"}
    print("success")
    return JsonResponse(data)


# 新建文档
def create_doc(request):
    print('create doc')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    name = request.POST.get("title")
    team_id = request.POST.get("team_id")
    in_group = True
    if (team_id == -1):
        in_group = False
    # content = request.POST.get("content")
    # create_time = request.POST.get("create_time")
    # print(content)
    doc = Document.objects.create(creator=user, name=name, in_group=in_group)
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


# 获取文档内容及收藏状态
def get_doc(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    # 还需判断该用户权限
    print("get doc")
    doc_id = request.POST.get("doc_id")
    # team_id = request.POST.get("team_id")
    # print(doc_id)
    doc = Document.objects.get(pk=doc_id)
    # team = None
    # if team_id != -1:
        # team = Team.objects.get(pk=team_id)
    islike = True
    if not Collection.objects.filter(Q(user=user) & Q(doc=doc)):
        islike = False
    data = {'name': doc.name, 'content': doc.content, 'islike': islike}
    # print("success")
    return JsonResponse(data)


# 我创建和收藏的文档信息
def my_doc(request):
    print('my docs')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    # 还需修改：
    # 只显示个人创建的，不显示团队文档
    created_documents = Document.objects.filter(creator=user)
    created_docs = []
    collections = Collection.objects.filter(user=user)
    collected_docs = []
    for d in created_documents:
        if not d.in_group:
            c_item = {
                'name': d.name,
                # 'content': d.content,
                'doc_id': d.pk,
            }
            created_docs.append(c_item)
    for d in collections:
        if not d.doc.in_group:
            c_item = {
                'name': d.doc.name,
                # 'content': d.content,
                'doc_id': d.doc.pk,
            }
            collected_docs.append(c_item)
    data = {'created_docs': created_docs, 'collected_docs': collected_docs}
    return JsonResponse(data)


# 发送邀请
def invite_user(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    actor = user
    recipient = User.objects.get(username=request.POST.get("username"))
    print(request.POST.get("username"))
    verb = 'invite ' + recipient.username + " to"
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
    if request.POST.get("answer") == 'Yes':
        # 用户接受邀请
        # 获取团队
        team = Team.objects.get(id=request.POST.get("team_id"))
        # User作为组员加入团队
        TeamUser.objects.create(user=user, team=team, is_leader=False)
        print('Success')
    elif request.POST.get("answer") == 'No':
        # 用户拒绝邀请
        print('Refuse')
    else:
        print('There must be something wrong with the data!')

    Notification.objects.get(id=notice_id).delete()

    return JsonResponse({})


# 获取未读信息
def get_user_notice(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    unread_notice = user.notifications.unread()
    notice_list = []
    for notice in unread_notice:
        team = notice.target
        actor = notice.actor
        item = {
            'notice_id': notice.id,
            'actor_id': actor.id,
            'actor_name': actor.username,
            'verb': notice.verb,
            'target_id': team.id,
            'target_name': team.team_name,
            'sent_time': datetime.strftime(notice.timestamp, '%Y-%m-%d %H-%M'),
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
            'comment_id':comment.id,
            'user': comment.user.username,
            'content': comment.body,
            'post_time':datetime.strftime(comment.created_time, '%Y-%m-%d %H-%M'),
        }
        comment_list.append(item)

    data = {"comment_list": comment_list, "current_user": user.username}
    return JsonResponse(data)


def delete_comment(request):
    print("delete comment")
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    # 获取评论id
    comment_id = request.POST.get("comment_id")
    Comment.objects.get(id=comment_id).delete()
    return JsonResponse({})



# #最近浏览的文档信息
# def my_browse_doc(request):
#     print('my browse docs')
#     user = authentication(request)
#     if user is None:
#         return HttpResponse('Unauthorized', status=401)
#     browsing = Browsing.objects.filter(user=user)
#     browsing_docs = []
#     for d in browsing:
#         c_item = {
#             'name': d.doc.name,
#             # 'content': d.content,
#             'doc_id': d.doc.pk,
#         }
#         browsing_docs.append(c_item)
#     data = {'browsing_docs':browsing_docs}
#     return JsonResponse(data)

# #新建、更新浏览记录
# def update_browsing(request):
#     user = authentication(request)
#     doc_id = request.POST.get("doc_id")
#     doc = Document.objects.get(pk=doc_id)
#     if user is None:
#         return HttpResponse('Unauthorized', status=401)
#     oldb = Browsing.objects.filter(Q(user=user) & Q(doc=doc))
#     if oldb:
#         oldb.delete()
#     newb = Browsing.objects.create(user=user,doc=doc)
#     data = {"message": 1}
#     return JsonResponse(data)