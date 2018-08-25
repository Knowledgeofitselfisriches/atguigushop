from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, \
    UserAddressSerializer
from rest_framework.permissions import IsAuthenticated

from utils.permissions import IsOwnerOrReadOnly


# 用户收藏
class UserFavViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,  # 添加收藏
                     mixins.DestroyModelMixin,  # 取消收藏
                     mixins.ListModelMixin,  # 得到收藏列表
                     mixins.RetrieveModelMixin  # 得到某条收藏
                     ):
    """
    list:
        得到当前用户的收藏列表

    create:
        在当前用户下，添加某个一个商品的收藏

    destroy:
        删除当前用户下的某一个商品的收藏,根据商品的id

    retrieve:
        获取某个商品的收藏，根据商品id




    """

    # 得到所有的收藏
    queryset = UserFav.objects.all()

    # IsAuthenticated判断用户是否登录-权限验证
    # IsOwnerOrReadOnly 请求的用户和当前用户是否是同一一个用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # SessionAuthentication -->Session认证--->根据sessoin得到用户信息
    # JSONWebTokenAuthentication -->jwt token认证-->token得到用户信息
    # 数据的安全
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 收藏/收藏的id--->收藏/商品的id
    lookup_field = "goods_id"

    # 商品收藏数
    def perform_create(self, serializer):
        userfav = serializer.save()
        goods = userfav.goods
        goods.fav_num += 1
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        if goods.fav_num > 0:
            goods.fav_num -= 1
        goods.save()
        instance.delete()

    # 序列化器
    # serializer_class = UserFavSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserFavSerializer
        else:
            # 列表，返回详情收藏信息
            return UserFavDetailSerializer

    # 当前用户只能得到自己的收藏--当前用户只能得到自己的留言，得到自己的订单列表
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# 用户留言的接口
# 删除留言，提交留言，得到留言的列表
class UserLeavingMessageViewSet(viewsets.GenericViewSet,
                                mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.DestroyModelMixin
                                ):
    # 配置序列化器-
    serializer_class = UserLeavingMessageSerializer

    # 判断用户是否登录或者是否是统一一个用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # jwt token认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 得到所有留言
    queryset = UserLeavingMessage.objects.all()

    # 重写queryset
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# 增加、删除、修改、得到收货列表、得到某一条收货地址
class UserAddressViewSet(viewsets.ModelViewSet):
    # 得到所有的数据
    queryset = UserAddress.objects.all()

    # 设置序列化器
    serializer_class = UserAddressSerializer

    # 判断用户是否登录或者是否是统一一个用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # jwt token认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 得到用户自己的收货地址
    def get_queryset(self):
        # 根据user去过滤
        # user = admin
        return self.queryset.filter(user=self.request.user)
