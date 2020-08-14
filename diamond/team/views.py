from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def create_team(request):
    print('create success')
    return JsonResponse({})
