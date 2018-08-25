# _*_ coding:utf-8 _*_
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

UserProfile = get_user_model()


# 信号量 某个model保存后调用 注意它会将createuperuser 注册的已加密的用户再次加密
@receiver(post_save, sender=UserProfile)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()