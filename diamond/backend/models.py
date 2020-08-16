from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey


# 用户
class User(AbstractUser):
    # username 继承
    # password 继承
    # 头像
    # avatar = ProcessedImageField(verbose_name='头像', upload_to='user_avatar/', blank=True, null=False,
    #                              default='avatar.png', processors=[ResizeToFill(150, 150)])
    phone_number = models.CharField(verbose_name='电话', max_length=64, null=True, blank=True)
    wechat = models.CharField(verbose_name='微信', max_length=64, null=True, blank=True)


# 团队
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(verbose_name="团队名称", max_length=150)
    introduction = models.TextField(verbose_name="团队介绍", null=True, blank=True)

    def __str__(self):
        return self.team_name


# 用户团队是多对多关系，这是关系表
class TeamUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_leader = models.BooleanField(verbose_name="是否是队长", default=False)


# 权限表， 用户-团队 的权限是一个多对多关系
class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    view_doc_permission = models.BooleanField(verbose_name="查看文档权限", default=False)
    change_doc_permission = models.BooleanField(verbose_name="修改文档权限", default=False)
    share_doc_permission = models.BooleanField(verbose_name="分享文档权限", default=False)
    comment_doc_permission = models.BooleanField(verbose_name="评论文档权限", default=False)


# 文档
class Document(models.Model):
    """
    Document
    """
    # Many-to-one: need to know the creator of the document
    creator = models.ForeignKey(User, related_name='created_documents', verbose_name='创建者', on_delete=models.CASCADE,
                                null=False)

    # Many-to-one: if the group does not exist, the document belonging to it will be deleted too.
    team = models.ForeignKey(Team, related_name='documents', verbose_name="所属团队", on_delete=models.CASCADE, null=True,
                             blank=True)

    in_group = models.BooleanField(blank=False)
    name = models.CharField(max_length=64)
    content = models.TextField(null=True)
    created_date = models.DateTimeField("创建时间", auto_now=False, auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField("修改时间", auto_now=True, auto_now_add=False, null=True, blank=True)

    # class Meta:
    #     verbose_name = "文档"
    #     verbose_name_plural = "文档集"
    #     default_permissions = ()
    #     permissions = (
    #         ('doc_create', '文档创建'),
    #         ('doc_modify', '文档修改'),
    #         ('doc_review', '文档查看'),
    #         ('doc_share', '文档分享'),
    #         ('doc_comment', '文档评论'),
    #     )

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

    user = models.ForeignKey(User, related_name='records', verbose_name="浏览者", on_delete=models.CASCADE)
    doc = models.ForeignKey(
        Document,
        related_name='records',
        verbose_name="浏览的文档", on_delete=models.CASCADE)
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


class Comment(MPTTModel):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    body = models.TextField()

    created_time = models.DateTimeField(auto_now_add=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )

    reply_to = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MMTTMeta:
        order_insertion_by = ['created_time']
