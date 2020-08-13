from django.shortcuts import render
from django.http import JsonResponse
from backend.models import User


# Create your views here.
def login(request):
    print("login")
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username)
    print(password)
    print(User.objects.all())
    try:
        user = User.objects.get(username=username)
    except:
        data = {'flag': 'no', "msg": "unregisterd"}
        return JsonResponse({'request': data})
    if password == user.password:
        data_msg = "success"
        data_flag = "yes"
    else:
        data_msg = "wrong password"
        data_flag = "no"
    data = {'flag': data_flag, 'msg': data_msg}

    return JsonResponse({'request': data})


def register(request):
    print("register")
    username = request.POST.get("username")
    mail_address = request.POST.get("mail_address")
    password = request.POST.get("password")
    print(username)
    print(mail_address)
    print(password)
    try:
        if(User.objects.filter(mail_address=mail_address)):
            data = {'flag': 'no', "msg": "email existed"}
        else:
            if(User.objects.filter(username=username)):
                data = {'flag': 'no', "msg": "username existed"}
            else:
                data = {'flag': 'yes', "msg": "success"}
                user = User(username=username,
                            mail_address=mail_address, password=password)
                user.save()
    except:
        data = {'flag': 'no', "msg": "error!"}
        return JsonResponse({'request': data})

    print(User.objects.all())
    return JsonResponse({'request': data})
