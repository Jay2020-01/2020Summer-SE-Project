from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from login.views import authentication
from datetime import datetime

# Create your views here.

# 发送邀请
def invite_user(request):
    user = authentication(request)
    if user is None:
        return HttpResponse('Unauthorized', status=401)
    actor = user
    recipient = User.objects.get(username=request.POST.get("username"))
    # print(request.POST.get("username"))
    verb = 'invite ' + recipient.username + " to"
    team = Team.objects.get(id=request.POST.get("team_id"))
    # print(team)
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