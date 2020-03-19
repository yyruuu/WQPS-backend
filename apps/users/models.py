from django.db import models
from datetime import datetime
# Create your models here.


class User(models.Model):
    """
    用户
    """
    username = models.CharField(max_length=255, unique=True, verbose_name="用户名")
    email = models.CharField(max_length=255, verbose_name="邮箱")
    password = models.CharField(max_length=255, verbose_name="密码")
    createdAt = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
