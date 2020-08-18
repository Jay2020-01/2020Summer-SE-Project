from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.authtoken import views as token_views
import login.views as login_views
import backend.views as backend_views
urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    path('api-token-auth/', token_views.obtain_auth_token),
    # index.html App.vue
    path('', TemplateView.as_view(template_name="index.html")),
    path('ajax/change_info/', backend_views.change_info, name='change_info'),  # 部署时记得加上，与dist相关联
    path('ajax/login/', login_views.login, name='login'),
    path('ajax/user_info/', backend_views.user_info, name='user_info'),
    path('ajax/register/', login_views.register, name='register'),
    path('ajax/newdoc/', backend_views.create_doc, name='create_doc'),
    path('ajax/create_team/', backend_views.create_team, name='create_team'),
    path('ajax/search_user/', backend_views.search_user, name='search_user')
    # backend api
]

