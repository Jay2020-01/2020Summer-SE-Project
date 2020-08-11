from django.db import models

class User(models.Model):
    """
    User
    """

    username = ""
    
    password = ""
    
    phone_number = ""

    mail_address = ""

    wechat = ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = "s"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Document(models.Model):
    """
    Document
    """

    group = ""

    title = ""

    content = WangRichTextField()

    created_date  = ""

    modified_date = ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Group(models.Model):
    """
    Team
    """

    leader = ""

    partner = ""

    teamname = ""

    introduction = ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

class UDRight(models.Model):
    """
    permission
    """
    
    user = ""
    doc  = ""
    
    right_type = ""

    visit_time = ""

    isStared = ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = "s"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
