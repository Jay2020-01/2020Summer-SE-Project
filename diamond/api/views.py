from django.shortcuts import render
from django.http import JsonResponse
from .models import User


# Create your views here.
def change_info(request):
    print('change_info')
    username = request.POST.get("username", None)
    print(username)
    data = {'what': True}
    return JsonResponse(data)


def login(request):
    print("login")
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username)
    print(password)
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
    date = {'flag': date_flag, 'msg': date_msg}

    return JsonResponse({'request': date})


def register(request):
    print("register")
    username = request.POST.get("username")
    mail_address = request.POST.get("mail_address")
    password = request.POST.get("password")
    print(mail_address)
    try:
        user = User.objects.filter(mail_address=mail_address)
        date = {'flag': 'no', "msg": "email existed"}
    except:
        User.objects.create(
            username=username, mail_address=mail_address, password=password)
        date = {'flag': 'yes', "msg": "success"}

    return JsonResponse({'request': date})
