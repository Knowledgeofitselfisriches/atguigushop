from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress

from rest_framework import serializers


# 收藏的序列化器
class UserFavSerializer(serializers.ModelSerializer):
    # 用户，当前用户，登录的用户是谁就是谁
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        # 反正Meta
        validators = [
            UniqueTogetherValidator(
                # 填写的Molde要是model = UserFav
                queryset=UserFav.objects.all(),
                # 某个用户对某个商品只能收藏一次，但是多个用户对该商品是可以收藏的
                fields=('user', 'goods'), message="一个用户对某个商品只能收藏一次"
            )
        ]
        model = UserFav
        fields = ("user", "goods", "id")


# 收藏详情序列化器
class UserFavDetailSerializer(serializers.ModelSerializer):
    # 返回商品详细信息,商品的信息
    goods = GoodsSerializer(many=False)

    class Meta:
        # 收藏的数据
        model = UserFav
        fields = ("goods", "id")


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    # 用户，当前用户，登录的用户是谁就是谁
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # read_only=True 前端只读取,前端可以获取，可以展示；但前端不用提交，使用默认的数据
    # 对add_time自定义序列化器
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "subject", "message_type", "message", "file", "add_time", "id")


# 收货地址序列化器
class UserAddressSerializer(serializers.ModelSerializer):
    # 用户，当前用户，登录的用户是谁就是谁
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "district", "address", "signer_name", "signer_mobile", "add_time", "id")
