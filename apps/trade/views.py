from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, \
    OrderInfoDetailSerializer
from utils.permissions import IsOwnerOrReadOnly
from rest_framework import mixins


# 购物车商品增加，删除，修改，得到列表，得到某一条
class ShoppingCartViewSet(viewsets.ModelViewSet):
    # 得到所有的数据
    queryset = ShoppingCart.objects.all()

    # 权限验证
    # 判断用户是否登录，判断请求用户和当前系统用户是否是同一一个用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # token认证
    # jwt token 认证-->根据token -->获取用户信息，如果获取到认证成，返回数据，否则认证失败不返回数据
    # 有效保护了数据安全
    # SessionAuthentication 前端存储了session id,根据后端存在数据量的session id笔记是否是同一个用户
    # 如果后端存在，就得到用户信息
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 购车/购物车id--->购物车/商品id
    lookup_field = "goods_id"

    # 序列化器
    # serializer_class = ShoppingCartSerializer

    def get_serializer_class(self):
        if self.action == "list":
            # 返回列表详情的时候详情信息
            return ShoppingCartDetailSerializer
        else:
            # 修改，删除，得到某一条
            return ShoppingCartSerializer

    # 得到当前请求的用户自己的购物车的信息
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# 订单管理接口
class OrderInfoViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,  # 提交订单，把购物车清空，添加到订单OrderGoods
                       mixins.RetrieveModelMixin,  # 得到某个订单信息
                       mixins.ListModelMixin,  # 得到所有订单信息
                       mixins.DestroyModelMixin,  # 删除订单
                       ):
    # 得到所有订单信息
    queryset = OrderInfo.objects.all()

    # 是否登录，是同一一个用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # jwt token认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 序列化器
    # serializer_class = OrderInfoSerializerl

    def get_serializer_class(self):
        if self.action == "retrieve":
            # 返回详情的数据--用新的序列化器
            return OrderInfoDetailSerializer
        else:
            return OrderInfoSerializer

    # 过滤得到自己的订单信息
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # 把购物车所有的数据删除，并且存到订单的OrderGoods
    def perform_create(self, serializer):
        # 保存后会返回OrderInfo订单的实例对象
        order_info = serializer.save()

        # 查找当前用户下购物车所有的商品
        shopping_carts = ShoppingCart.objects.filter(user=self.request.user)  # 列表

        for shopping_cart in shopping_carts:
            # 订单详情商品
            order_goods = OrderGoods()

            # 订单
            order_goods.order = order_info

            # 先要保存到OrderGoods,取出购物车的商品
            goods = shopping_cart.goods
            # 保存到订单对应的商品model
            order_goods.goods = goods

            # 订单商品详情的数量
            order_goods.goods_num = shopping_cart.nums

            # 保存OrderGoods
            order_goods.save()

            # 把购物车里面的所有的商品删除，在删除之前，
            shopping_cart.delete()
