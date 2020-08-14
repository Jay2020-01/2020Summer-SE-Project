from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .models import User
from .models import Document


# Create your views here.
def change_info(request):
    print('change_info')
    username = request.POST.get("username")
    password = request.POST.get("password")
    phone_number = request.POST.get("phone_number")
    mail_address = request.POST.get("mail_address")
    wechat = request.POST.get("wechat")
    data = {'success': True}
    return JsonResponse(data)

def newdoc(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    print(title)
    print(content)
    document = Document(title=title,content=content)
    # document.save()
    data = {'flag': True}
    return JsonResponse({'request': data})