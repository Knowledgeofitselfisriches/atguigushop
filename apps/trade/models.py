from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods
from datetime import datetime

# Create your models here.
# 该行代码，是得到系统配置的UserProfile类的实例对象
UserProfile = get_user_model()


# 购物车
class ShoppingCart(models.Model):
    # 用户
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    # 商品
    goods = models.ForeignKey(Goods, verbose_name="商品")
    # 数量
    nums = models.IntegerField(default=1, verbose_name="购买的数量")
    # 添加时间：add_time, 得到当前时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "购物车"
        # verbose_name_plural 可以让后台的不加上s
        verbose_name_plural = verbose_name

    # 在后台管理的时候，显示当前Mode中的信息
    def __str__(self):
        return "%s购买了:%s" % (self.user.username, self.goods.name)


# 订单信息
class OrderInfo(models.Model):
    PAY_STATUS = (
        ("PAYING", "待支付"),
        ("TRADE_SUCCESS", "支付成功"),
        ("FAIL", "支付失败")
    )
    # 用户：user
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    # 订单号, 唯一：order_sn,在很多条数据中，该字段不能存在两个内容一样的
    order_sn = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="订单号")
    # 交易号（与支付宝或者微信支付相关）：trade_no
    trade_no = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="交易号")
    # 订单总金额：order_mount
    order_mount = models.FloatField(default=0.0, verbose_name="订单总额")
    # 支付的状态（待支付，支付成功，支付失败）：pay_status
    pay_status = models.CharField(max_length=20, default="PAYING", choices=PAY_STATUS, verbose_name="支付状态")
    # 支付时间：pay_time
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")

    # 订单留言：post_script
    post_script = models.CharField(max_length=200, null=True, blank=True, verbose_name="订单留言")
    # 签收人：singer_name
    signer_name = models.CharField(max_length=30, verbose_name="签收人")
    # 签收电话：singer_mobile
    signer_mobile = models.CharField(max_length=11, verbose_name="签收电话")
    # 收货地址：address
    address = models.CharField(max_length=100, verbose_name="收货地址")
    # 添加时间：add_time, 得到当前时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单信息"
        # verbose_name_plural 可以让后台的不加上s
        verbose_name_plural = verbose_name

    # 在后台管理的时候，显示当前Mode中的信息
    def __str__(self):
        return self.order_sn


# 订单的商品详情
class OrderGoods(models.Model):
    # 订单(要和订单一起呈现，关系字段related_name)：order
    order = models.ForeignKey(OrderInfo, related_name="goods")
    # 商品：goods
    goods = models.ForeignKey(Goods, verbose_name="商品")
    # 商品的数量：goods_num
    goods_num = models.IntegerField(default=1, verbose_name="商品数量")
    # 添加时间：add_time, 得到当前时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单的商品详情"
        # verbose_name_plural 可以让后台的不加上s
        verbose_name_plural = verbose_name

    # 在后台管理的时候，显示当前Mode中的信息
    def __str__(self):
        return self.goods.name
