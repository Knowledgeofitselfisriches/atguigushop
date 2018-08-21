from goods.models import Goods
from goods.serializers import GoodsSerializer
import time
import random

from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, OrderGoods


# 序列化OrderGoods
class OrderGoodsSerializer(serializers.ModelSerializer):
    # 订单商品和商品的关系--一对一关系，序列化只需要一条
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderInfoDetailSerializer(serializers.ModelSerializer):
    # 订单和订单商品关系--一对多的关系，要序列化多条
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


# 订单的序列化器
class OrderInfoSerializer(serializers.ModelSerializer):
    # 用户，当前用户，登录的用户是谁就是谁
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # 订单号不让前端编写
    order_sn = serializers.CharField(read_only=True)
    # 交易号不让前端编写,支付宝相关的，支付产生后才有
    trade_no = serializers.CharField(read_only=True)
    # 支付状态，成功支付后，才修改，默认是待支付
    pay_status = serializers.CharField(read_only=True)
    # 支付时间
    pay_time = serializers.DateTimeField(read_only=True)
    # 添加时间
    add_time = serializers.DateTimeField(read_only=True)

    # 生成订单号，订单号要去全网唯一：时间戳+用户id+随机两位数
    def generate_order_sn(self):
        order_sn = "{timestr}{userid}{randomint}".format(timestr=time.strftime("%Y%m%d%H%M%S"),
                                                         userid=self.context["request"].user,
                                                         randomint=random.randint(10, 99))
        return order_sn

    # attrs 字典
    def validate(self, attrs):
        # 生成的订单添加Model
        attrs["order_sn"] = self.generate_order_sn()

        # 返回
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    # 购物车对应的商品
    goods = GoodsSerializer(many=False)

    # 重重强调一下：Meta只是针对ModelSerializer,如果你继承的是Serializer,不起作用
    class Meta:
        model = ShoppingCart
        fields = "__all__"


# 为什么不继承ModelSerializer,而是继承Serializer呢？
# 集成Serializer，可以更加灵活的重写创建方法
class ShoppingCartSerializer(serializers.Serializer):
    # 购车id
    # id = serializers.IntegerField()

    # 用户，当前用户，登录的用户是谁就是谁
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # 购物车购买商品的数量
    nums = serializers.IntegerField(required=True, min_value=1, help_text="购车商品的数量",
                                    error_messages={"min_value": "购买数量至少为1"})

    # 把商品id当初主键
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # 第二参数：ShoppingCart实例对象，第三个参数：验证的数据
    def update(self, instance, validated_data):
        # ShoppingCart实例对象
        shopping_cart = instance
        # 修改购买商品的数量
        shopping_cart.nums = validated_data["nums"]
        # 保存数据
        shopping_cart.save()

        return shopping_cart

    # 如果这个商品已经在购物车里面存在5个，在添加5个，只修改数量就行了--重新写保存商品的方法
    def create(self, validated_data):
        # 得到请求过来的用户
        user = self.context['request'].user

        # 用户提交,validated_data从商品信息
        goods = validated_data["goods"]

        # 往购物车添加的购买商品数量
        nums = validated_data["nums"]

        # 根据用户和商品，去购物车查找该商品是否存在
        exisited = ShoppingCart.objects.filter(user=user, goods=goods)  # 列表[商品]

        if exisited:
            # 如果存在，不用添加新数据，而是在原来购物车的基础上添加数量即可
            # 变成具体的某一条数据，是ShoppingCart实例对象，购物车里面的信息
            exisited = exisited[0]
            # 已经购买了5件+5件
            exisited.nums += nums
            # 保存数据-修改数据
            exisited.save()

        else:
            # 如果不存在，就创建新的数据ShoppingCart，添加一条ShoppingCat nums =5
            # 创建成果后把数据返回
            exisited = ShoppingCart.objects.create(**validated_data)

        return exisited
