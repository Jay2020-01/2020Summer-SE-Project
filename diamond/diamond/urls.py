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
import login.views as login_views
import backend.views as backend_views
urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    
    # index.html App.vue
    path('', TemplateView.as_view(template_name="index.html")),
    path('ajax/change_info/', backend_views.change_info, name='change_info'),
    path('ajax/login/', login_views.login, name='login'),
    path('ajax/register/', login_views.register, name='register'),
    path('ajax/newdoc/', backend_views.newdoc, name='newdoc'),
    # backend api
    
]
