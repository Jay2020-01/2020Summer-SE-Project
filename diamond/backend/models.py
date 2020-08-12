from django.db import models


# from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(models.Model):
    # SEX_CHOICES = (
    #     ('男', 1),
    #     ('女', 0),)
    # id = models.CharField(max_length=64,verbose_name="id")
    username = models.CharField(max_length=64, verbose_name="姓名")
    password = models.CharField(max_length=256, verbose_name="密码")
    mail_address = models.CharField(max_length=64, verbose_name="邮箱")

# class User(AbstractUser):
#     """
#     User
#     """
#     user_id = models.CharField(max_length=64, unique=True)
#
#     username = models.CharField(max_length=64)
#
#     password = models.CharField(max_length=64)
#
#     phone_number = models.CharField(max_length=64, null=True)
#
#     email = models.EmailField(null=True)
#
#     wechat = models.CharField(max_length=64, null=True)
#
#     # starDoc = models.ManyToManyField(Doc, verbose_name="收藏文章")
#
#     # set auth mark
#     USERNAME_FIELD = 'user_id'
#
#     class Meta:
#         verbose_name = "用户"
#         verbose_name_plural = "用户集"
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse("_detail", kwargs={"pk": self.pk})
#

# class Group(models.Model):
#     """
#     Team
#     """
#
#     leader = models.OneToOneField(User, verbose_name="组长", on_delete=models.CASCADE)
#
#     #  = models.ManyToManyField(User, verbose_name="队员", on_delete=models)
#
#     groupname = models.CharField(max_length=64)
#
#     introduction = models.TextField(null=True)
#
#     class Meta:
#         verbose_name = "团队"
#         verbose_name_plural = "百团"
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse("_detail", kwargs={"pk": self.pk})
#
#
# class Document(models.Model):
#     """
#     Document
#     """
#
#     # Many-to-one: if the group does not exist, the document belonging to it will be deleted too.
#     group = models.ForeignKey(Group, verbose_name="所属团队", on_delete=models.CASCADE)
#
#     title = models.CharField(max_length=64)
#
#     content = models.AutoField()
#
#     created_date = models.DateTimeField(auto_now_add=True)
#
#     modified_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "文档"
#         verbose_name_plural = "文档集"
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse("_detail", kwargs={"pk": self.pk})
#
#
# class UDRight(models.Model):
#     """
#     User and Doc
#     """
#
#     user = models.ForeignKey(User, verbose_name="", on_delete=models.CASCADE)
#     doc = models.ForeignKey(Document, verbose_name="", on_delete=models.CASCADE)
#
#     right_type = models.BigIntegerField()
#
#     visit_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = ""
#         verbose_name_plural = "s"
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse("_detail", kwargs={"pk": self.pk})
