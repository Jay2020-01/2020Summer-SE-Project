from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings

class UserProfile(models.Model):
    """
    User information file
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=64, null=True, blank=True)

    wechat = models.CharField(max_length=64, null=True, blank=True)

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

    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    groupname = models.CharField(max_length=150)

    leader = models.ForeignKey(User,related_name='leader', verbose_name="组长", on_delete=models.CASCADE)

    introduction = models.TextField(null=True, blank=True)

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
    creater = models.ForeignKey(User, verbose_name='创建者', on_delete=models.CASCADE, null=False)

    # Many-to-one: if the group does not exist, the document belonging to it will be deleted too.
    group = models.ForeignKey(Group, verbose_name="所属团队", on_delete=models.CASCADE, null=True, blank=True)

    in_group = models.BooleanField(blank=False)

    name = models.CharField(max_length=64)

    content = models.TextField(null=True)

    created_date  = models.DateTimeField("创建时间", auto_now=False, auto_now_add=True, null=True, blank=True)
    
    modified_date = models.DateTimeField("修改时间", auto_now=True, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = "文档"
        verbose_name_plural = "文档集"
        default_permissions = ()
        permissions = (
            ('doc_create', '文档创建'),
            ('doc_modify', '文档修改'),
            ('doc_review', '文档查看'),
            ('doc_share' , '文档分享'),
        )
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    def is_in_group(self):
        return self.in_group

class UDRecord(models.Model):
    """
    the document browsing history of user
    """
    
    user = models.ForeignKey(User, verbose_name= "浏览者", on_delete=models.CASCADE)
    doc  = models.ForeignKey(Document, verbose_name= "浏览的文档", on_delete=models.CASCADE)

    visit_time = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "浏览记录"
        verbose_name_plural = "浏览记录集"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Favorite(models.Model):
    """
    the favorite model
    """
    
    # one-to-one
    user = models.OneToOneField(User, verbose_name="收藏家", on_delete=models.CASCADE)
    # Many-to-many
    documents = models.ManyToManyField(Document, verbose_name="收藏文档")


class Recyclebin(models.Model):
    """
    the recyclebin
    """
    user = models.OneToOneField(User, verbose_name="回收站", on_delete=models.CASCADE)
    
    documents = models.ManyToManyField(Document, verbose_name="回收文件")