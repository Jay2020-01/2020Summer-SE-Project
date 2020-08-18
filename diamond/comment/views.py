from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from login.views import authentication
from datetime import datetime

# my models
from backend.models import User, Document, Team, TeamUser, Comment, Collection, Delete_document, Template

# Create your views here.
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
            'comment_id': comment.id,
            'user': comment.user.username,
            'content': comment.body,
            'post_time': datetime.strftime(comment.created_time, '%Y-%m-%d %H-%M'),
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