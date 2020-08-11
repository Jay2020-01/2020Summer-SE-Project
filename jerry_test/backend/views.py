from django.shortcuts import render
from . import models
from django.http import JsonResponse


# Create your views here.
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(username)
    print(password)
    try:
        user = models.User.objects.get(username=username)
    except:
        date = {'flag': 'no', "msg" : "unregisterd"}
        return JsonResponse({'request': date})
    if password == user.password:
        date_msg = "success"
        date_flag = "yes"
    else:
        date_msg = "wrong password"
        date_flag = "no"
    date = {'flag':date_flag,'msg': date_msg}

    return JsonResponse({'request': date})