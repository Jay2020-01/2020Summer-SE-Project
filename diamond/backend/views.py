from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from login.views import authentication
from datetime import datetime
import hashlib

# my models
from .models import User, Document, Team, TeamUser, Comment, Collection, Delete_document, Template
# third-party
from notifications.models import Notification
from notifications.signals import notify


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
    # print(doc_id)
    user = authentication(request)
    doc = Document.objects.get(pk=doc_id)
    collection = Collection.objects.get(Q(user=user) & Q(doc=doc))
    collection.delete()
    data = {'flag': "yes", 'msg': "uncollect success"}
    # print("success")
    return JsonResponse(data)


# 新建文档
def create_doc(request):
    print('create doc')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    name = request.POST.get("title")
    team_id = request.POST.get("team_id")
    in_group = False
    team = None
    if (int(team_id) >= 0):
        in_group = True
        team = Team.objects.get(id=team_id)
    # content = request.POST.get("content")
    # create_time = request.POST.get("create_time")
    # print(content)

    # 生成独特的原始码
    raw_code = user.username + name + str(datetime.now())
    raw_code = raw_code.encode('utf-8')
    # 生成哈希加密后的identifier
    md = hashlib.md5()
    md.update(raw_code)
    key = md.hexdigest()

    # 创建一个新文档
    doc = Document.objects.create(creator=user, name=name, in_group=in_group, team=team, key=key)

    # print(doc.pk)
    data = {'flag': "yes", 'doc_id': doc.pk, 'msg': "create success"}
    # print("success")
    return JsonResponse(data)


# 用模板新建文件
def create_doc_with_temp(request):
    print('create doc with template')
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    name = request.POST.get("title")
    team_id = request.POST.get("team_id")
    temp_id = request.POST.get("temp_id")
    print(temp_id)
    in_group = False
    team = None
    if (int(team_id) >= 0):
        in_group = True
        team = Team.objects.get(id=team_id)
    # create_time = request.POST.get("create_time")
    doc = Document.objects.create(creator=user, name=name, in_group=in_group, team=team)
    temp = Template.objects.get(pk=temp_id)
    temp_content = temp.content
    doc.content = temp_content
    doc.save()
    data = {'flag': "yes", 'doc_id': doc.pk, 'msg': "create success"}
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
    doc = Document.objects.get(creator=user, pk=doc_id)
    doc.content = content
    doc.save()
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
    # print('my docs')
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
