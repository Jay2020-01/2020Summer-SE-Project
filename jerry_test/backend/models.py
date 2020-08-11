from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64,verbose_name="姓名")
    password = models.CharField(max_length=16,verbose_name="密码")
    mail = models.CharField(max_length=64,blank=True,verbose_name="邮箱")

    def __str__(self):
        return str(self.username)