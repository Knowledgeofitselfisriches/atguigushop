import datetime

from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from AtguiguShop.settings import APPID, RETURN_URL, APP_PRIVATE_KEY_PATH, ALIPAY_PUBLIC_KEY_PATH, ALIPAY_DEBUG
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, \
    OrderInfoDetailSerializer
from utils.alipay import AliPay
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

        # 修改，删除，得到某一条
        return ShoppingCartSerializer

    # 得到当前请求的用户自己的购物车的信息
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    # 商品库存的修改
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        # 商品的库存减少
        goods.goods_num -= shop_cart.nums
        goods.save()

    # 当重购物车删除要购买的商品的时候库存增加（不购买了）
    def perform_destroy(self, instance):
        goods = instance.goods
        # 商品库存增加
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    # 商品库存的更新
    def perform_update(self, serializer):
        pre_shopcart = ShoppingCart.objects.get(id=serializer.instance.id)
        pre_num = pre_shopcart.nums

        now_shopcart = serializer.save
        now_num = now_shopcart.nums
        nums = now_num - pre_num

        goods = pre_shopcart.goods
        goods.goods_num -= nums
        goods.save()


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
    # serializer_class = OrderInfoSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            # 返回详情的数据--用新的序列化器
            return OrderInfoDetailSerializer
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


class AlipayAPIView(APIView):
    def get(self, request):
        process_query = {k: v for k, v in request.GET.items()}
        ali_sign = process_query.pop('sign')
        alipay = AliPay(
            appid=APPID,
            app_notify_url=RETURN_URL,
            app_private_key_path=APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=RETURN_URL
        )
        check_result = alipay.verify(process_query, ali_sign)
        response = redirect('index')
        if check_result:
            order_sn = process_query.get('out_trade_no', None)
            trade_no = process_query.get('trade_no', None)
            order_infos = OrderInfo.objects.filter(order_sn=order_sn)

            # 交易信息保存
            for order_info in order_infos:
                order_goods = order_info.goods.all()
                for order_good in order_goods:
                    # 根据某个个订单得到对应的商品
                    goods = order_good.goods
                    # 商品的销量等于购物车的销量加上原来的
                    goods.sold_num += order_good.goods_num
                    goods.save()

                order_info.trade_no = trade_no
                order_info.pay_status = "TRADE_SUCCESS"
                order_info.pay_time = datetime.datetime.now()
                order_info.save()

            response.set_cookie('nextPath', 'pay', max_age=2)
        return response

    def post(self, request):
        process_query = {k: v for k, v in request.POST.items()}
        ali_sign = process_query.pop('sign')
        alipay = AliPay(
            appid=APPID,
            app_notify_url=RETURN_URL,
            app_private_key_path=APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=ALIPAY_DEBUG,  # 默认False,
            return_url=RETURN_URL
        )
        check_result = alipay.verify(process_query, ali_sign)
        response = redirect('index')
        if check_result:
            order_sn = process_query.get('out_trade_no', None)
            trade_no = process_query.get('trade_no', None)
            order_infos = OrderInfo.objects.filter(order_sn=order_sn)

            # 交易信息保存
            for order_info in order_infos:
                order_goods = order_info.goods.all()
                for order_good in order_goods:
                    # 根据某个个订单得到对应的商品
                    goods = order_good.goods
                    # 商品的销量等于购物车的销量加上原来的
                    goods.sold_num += order_good.goods_num
                    goods.save()

                order_info.trade_no = trade_no
                order_info.pay_status = "TRADE_SUCCESS"
                order_info.pay_time = datetime.datetime.now()
                order_info.save()
            response.set_cookie('nextPath', 'pay', max_age=2)
        return response


