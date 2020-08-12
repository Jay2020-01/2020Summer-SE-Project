from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import User


# Create your views here.
def change_info(request):
    print('change_info')
    username = request.POST.get("username")
    print(username)
    data = {'what': True}
    return JsonResponse(data)
