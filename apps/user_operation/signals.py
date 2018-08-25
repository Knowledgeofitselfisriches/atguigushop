# _*_ coding:utf-8 _*_
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from user_operation.models import UserFav

UserProfile = get_user_model()


# 信号量 某个model保存后调用 注意它会将createuperuser 注册的已加密的用户再次加密
@receiver(post_save, sender=UserFav)
def save_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
        goods = instance.goods
        if goods.fav_num > 0:
            goods.fav_num -= 1
        goods.save()
        instance.delete()