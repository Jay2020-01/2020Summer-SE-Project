from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.




class User(AbstractUser):
    SEX_CHOICES = (
        ('男', 1),
        ('女', 0),)
    id = models.CharField(max_length=64,verbose_name="id")
    username = models.CharField(max_length=64,verbose_name="姓名")
    wechat_num = models.CharField(max_length=64,blank=True,verbose_name="微信号")
    sex = models.CharField(max_length=1,choices=SEX_CHOICES,verbose_name='性别',default=1)
    phone = models.CharField(max_length=20,blank=True,verbose_name='电话')
    mail = models.CharField(max_length=64,blank=True,verbose_name="邮箱")

class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    leader_id = models.CharField(max_length=64)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    members = models.ManyToManyField(User, through='MemberShip')
    class Meta:
        verbose_name = '团队'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Doc(models.Model):
    title = models.CharField('文件名', max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    isintrash = models.BooleanField(default=True)
    class Meta:
        verbose_name = '文档'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

class Right(models.Model):
    right_user = models.ForeignKey(User)
    right_team = models.ForeignKey(Team)
    check_rig = models.BooleanField(default=False)
    discuss_rig = models.BooleanField(default=False)
    fix_rig = models.BooleanField(default=False)
    # share_rig = models.BooleanField(default=False) # ？ 此处并不需要