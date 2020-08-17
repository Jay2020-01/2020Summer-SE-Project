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
from rest_framework.authtoken import views as token_views
import login.views as login_views
import backend.views as backend_views
import team.views as team_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    path('api-token-auth/', token_views.obtain_auth_token),
    # index.html App.vue
    # path('', TemplateView.as_view(template_name="index.html")),
    path('ajax/change_info/', backend_views.change_info, name='change_info'),
    path('ajax/login/', login_views.login, name='login'),
    path('ajax/user_info/', backend_views.user_info, name='user_info'),
    path('ajax/register/', login_views.register, name='register'),
    path('ajax/create_doc/', backend_views.create_doc, name='create_doc'),
    path('ajax/save_doc/', backend_views.save_doc, name='save_doc'),
    path('ajax/my_doc/', backend_views.my_doc, name='my_doc'),
    path('ajax/get_doc/', backend_views.get_doc, name='get_doc'),
    path('ajax/create_team/', team_views.create_team, name='create_team'),
    path('ajax/search_user/', team_views.search_user, name='search_user'),
    path('ajax/get_my_team/', team_views.get_my_team, name='get_my_team'),
    path('ajax/get_team_member/', team_views.get_team_member, name='get_team_member'),
    path('ajax/delete_my_team/', team_views.delete_my_team, name='delete_my_team'),
    path('ajax/collect_doc/', backend_views.collect_doc, name='collect_doc'),
    path('ajax/uncollect_doc/', backend_views.uncollect_doc, name='uncollect_doc'),
    path('ajax/delete_doc/', backend_views.delete_doc, name='delete_doc'),
    path('ajax/delete_doc_completely/', backend_views.delete_doc_completely, name='delete_doc_completely'),
    path('ajax/restore_doc/', backend_views.restore_doc, name='restore_doc'),
    path('ajax/get_deleted_docs/', backend_views.get_deleted_docs, name='get_deleted_docs'),
    path('ajax/invite_user/',backend_views.invite_user, name='invite_user'),
    path('ajax/get_user_notice/',backend_views.get_user_notice, name='get_user_notice'),
    path('ajax/response_invitation/',backend_views.response_invitation, name='response_invitation'),
    path('ajax/image_upload/', backend_views.user_avatar_upload, name="user avatar upload"),
    # backend api
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 图片相关