"""diamond URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from api.views import change_info, login, register

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    
    # index.html App.vue
    path('', TemplateView.as_view(template_name="index.html")),
    path('ajax/change_info/', change_info, name='change_info'),
    path('ajax/login/', login, name='login'),
    path('ajax/register/', register, name='register'),
    # backend api
    
]
