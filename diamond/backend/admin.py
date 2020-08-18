from django.contrib import admin
from .models import User,Team,TeamUser,Permission
from .models import Document,Collection,Delete_document,UDRecord,Favorite
from .models import Recyclebin,Comment,Templet
# from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Team)
admin.site.register(TeamUser)
admin.site.register(Permission)
admin.site.register(Document)
admin.site.register(Collection)
admin.site.register(Delete_document)
admin.site.register(UDRecord)
admin.site.register(Favorite)
admin.site.register(Recyclebin)
admin.site.register(Comment)
admin.site.register(Templet)