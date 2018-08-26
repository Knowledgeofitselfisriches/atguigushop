"""AtguiguShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.generic import TemplateView

from goods.view_apiview import GoodsListAPIView
from goods.view_django_serializer_view import GoodsListDjangoSerializerView
from goods.view_django_view import GoodsListDjangoView
from rest_framework.authtoken import views

import xadmin
from django.views.static import serve
from AtguiguShop.settings import MEDIA_ROOT
from AtguiguShop.settings import STATIC_ROOT
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
# 配置主路由
from goods.view_generic_apiview import GoodsListGenericAPIView
from goods.views import GoodsViewSet, GoodsCategoryViewSet, BannerViewSet, IndexGoodsCategoryViewSet
from rest_framework_jwt.views import obtain_jwt_token

from trade.views import ShoppingCartViewSet, OrderInfoViewSet, AlipayAPIView
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from users.views import VerifyCodeViewSet, UserProfileViewSet

router = routers.DefaultRouter()
# 注册商品列表
router.register(r"goods", GoodsViewSet)
# 注册商品类别的路由
router.register(r"categorys", GoodsCategoryViewSet)
# 生成验证并且发送给用户
router.register(r"code", VerifyCodeViewSet)

# 配置用户-注册后期-（修改，得到用户）
router.register(r"users", UserProfileViewSet)

# 注册用户收藏
router.register(r"userfavs", UserFavViewSet)
# 注册用户留言
router.register(r"messages", UserLeavingMessageViewSet)
# 注册用户收货地址
router.register(r"address", UserAddressViewSet)
# 注册购物车
router.register(r"shopcarts", ShoppingCartViewSet)

# 订单管理
router.register(r"orders", OrderInfoViewSet)
# 首页轮播图
router.register(r"banners", BannerViewSet)
router.register(r"indexgoods", IndexGoodsCategoryViewSet)

# 配置全局404 500
# handler404 = 'users.views.handler_404'
# handler500 = 'users.views.handler_500'
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),  # 配置xadmin的路由
    # 配置xadmin后台能显示图片的路径
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    # url(r"^goods/",goods_list,name="goods"),
    # 使用django 的View 返回商品列表
    url(r"^goods1/", GoodsListDjangoView.as_view(), name="goods1"),
    # django的serializer序列化model
    url(r"^goods2/", GoodsListDjangoSerializerView.as_view(), name="goods2"),
    url(r'^goods3/', GoodsListAPIView.as_view(), name="goods3"),
    url(r'^goods4/', GoodsListGenericAPIView.as_view(), name="goods4"),
    # 注意http://127.0.0.1:8000
    url(r'^', include(router.urls)),
    # 配置用户登录和登出
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 配置文档路径
    url(r'^docs/', include_docs_urls(title='硅谷商城在线文档')),
    # django-rest-framework的token认证
    url(r'^api-token-auth/', views.obtain_auth_token),

    # json web token认证--根据用户和密码-->jwt 的token 一定要加￥ 防止冲突
    url(r'^login/$', obtain_jwt_token),
    # 第三方登录
    url('', include('social_django.urls', namespace='social')),
    # 注意http://127.0.0.1:8000
    url(r'^', include(router.urls)),

    url(r'^alipay/return/', AlipayAPIView.as_view(), name="alipay"),
    url(r'^index/', TemplateView.as_view(template_name='index.html'), name='index')

]
