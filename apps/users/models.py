from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.

# 整个项目中，只有UserProfile，才继承AbstractUser，其他的Model都是继承models.Model
class UserProfile(AbstractUser):
    """用户信息"""
    GENDER = (
        ("male", "男"),
        ("female", "女")
    )
    # 姓名
    # blank=True,null=True该字段可以不填写或者为空
    # help_text="姓名"，在前后端分离的项目中，注释会出现在文档中
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="姓名", help_text="姓名")
    # 性别
    gender = models.CharField(max_length=6, choices=GENDER, default="female", verbose_name="性别")
    # 出生年月
    birthday = models.DateField(blank=True, null=True, verbose_name="出生年月")
    # 邮箱
    email = models.EmailField(max_length=50, default="", blank=True, null=True, verbose_name="邮箱")
    # 手机号
    mobile = models.CharField(max_length=11, verbose_name="手机号码", help_text="手机号")

    class Meta:
        verbose_name = "用户信息"
        # verbose_name_plural 可以让后台的不加上s
        verbose_name_plural = verbose_name

    # 在后台管理的时候，显示当前Mode中的信息
    def __str__(self):
        return self.username


# 验证码
class VerifyCode(models.Model):
    # 验证码：code
    code = models.CharField(max_length=4, verbose_name="验证码")
    # 手机号：mobile
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    # 添加时间：add_time, 得到当前时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "验证码"
        # verbose_name_plural 可以让后台的不加上s
        verbose_name_plural = verbose_name

    # 在后台管理的时候，显示当前Mode中的信息
    def __str__(self):
        return self.code
