from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from wangeditor.fields import WangRichTextField

class UserProfile(models.Model):
    """
    User information file
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=64, null=True)
    wechat = models.CharField(max_length=64, null=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息集"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class GroupProfile(models.Model):
    """
    Team profile
    """

    Group = models.OneToOneField(Group, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, related_name='leader', verbose_name="组长", on_delete=models.CASCADE)
    introduction = models.TextField(null=True)

    class Meta:
        verbose_name = "团队信息"
        verbose_name_plural = "团队信息集"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Document(models.Model):
    """
    Document
    """
    # Many-to-one: need to know the creater of the document
    creator = models.ForeignKey(User, verbose_name='创建者', on_delete=models.CASCADE, null=False)

    # Many-to-one: if the group does not exist, the document belonging to it will be deleted too.
    group = models.ForeignKey(Group, verbose_name="所属团队", on_delete=models.CASCADE, null=False)
    
    name = models.CharField(max_length=64)

    # content = models.TextField(null=True)
    content = WangRichTextField()

    created_date = models.DateTimeField("创建时间", auto_now=False, auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField("修改时间", auto_now=True, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = "文档"
        verbose_name_plural = "文档集"
        default_permissions = ()
        permissions = (
            ('doc_create', '文档创建'),
            ('doc_modify', '文档修改'),
            ('doc_review', '文档查看'),
            ('doc_share', '文档分享'),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class UDRecord(models.Model):
    """
    User and Doc record
    """
    user = models.ForeignKey(User, verbose_name="", on_delete=models.CASCADE)
    doc = models.ForeignKey(Document, verbose_name="", on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)
    isStared = models.BooleanField()

    class Meta:
        verbose_name = ""
        verbose_name_plural = "s"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
