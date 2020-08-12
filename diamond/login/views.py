from django.shortcuts import render
from django.http import JsonResponse
from backend.models import User


# Create your views here.
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    try:
        user = User.objects.get(username=username)
    except:
        date = {'flag': 'no', "msg": "unregisterd"}
        return JsonResponse({'request': date})
    if password == user.password:
        date_msg = "success"
        date_flag = "yes"
    else:
        date_msg = "wrong password"
        date_flag = "no"
    data = {'flag': date_flag, 'msg': date_msg}

    return JsonResponse(data)


def register(request):
    data = {'flag': 'no', "msg": "email existed"}
    username = request.POST.get("username")
    mail_address = request.POST.get("mail_address")
    password = request.POST.get("password")

    same_name_user = User.objects.get(username=username)
    if same_name_user:
        data['msg'] = '用户名已经存在'
        return JsonResponse(data)
    same_email_user = User.objects.get(email=mail_address)
    if same_email_user:
        data['msg'] = '该邮箱已经被注册了！'
        return JsonResponse(data)
    # 以下代码等价于 User.objects.create(username=username, email=mail_address, password=password)
    new_user = User()
    new_user.name = username
    new_user.password = password
    new_user.email = mail_address
    new_user.save()
    data['flag'] = 'yes'
    data['msg'] = '成功注册！'
    return JsonResponse(data)
