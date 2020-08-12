from django.db import models


# Create your models here.
class User(models.Model):
    # SEX_CHOICES = (
    #     ('男', 1),
    #     ('女', 0),)
    # id = models.CharField(max_length=64,verbose_name="id")
    username = models.CharField(max_length=64, verbose_name="姓名")
    password = models.CharField(max_length=256, verbose_name="密码")
