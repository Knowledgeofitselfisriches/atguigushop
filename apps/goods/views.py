from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle , AnonRateThrottle
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from goods.filters import GoodsFilter
from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, GoodsCategorySerializer1, BannerSerializer, IndexGoodsCategorySerializer
from django_filters import rest_framework as filters
from rest_framework_extensions.cache.mixins import CacheResponseMixin


# mixins 模块
# CreateModelMixin 创建数据，保存数据 -- 客户端发起post向服务器提交数据
# ListModelMixin 把数据库的数据，以列表的方式返回 ---客户端发起get请求，得到列表数据
# RetrieveModelMixin 得到列表中某一条数据， ---客户端发起get请求，得到某条数据
# UpdateModelMixin  更新某条数据       ---客户端发起的put请求 ，返回更新后的数据
# DestroyModelMixin  删除某一条数据     ---客户端发起 delete请求，返回空文档
class GoodsPagination(PageNumberPagination):
    # 每页返回10
    page_size = 12
    # 使用的字段
    page_size_query_param = 'page_size'
    # 自定义页码对应的字段
    page_query_param = "page"
    # 最多100
    max_page_size = 100


# GenericViewSet继承GenericAPIView类

# 写接口的时候：model名称+ViewSet
# GoodsViewSet()

# 1.继承GenericViewSet
# 2.继承mixins.ListModelMixin,返回列表，得到某条数据RetrieveModelMixin，更新某条数据UpdateModelMixin，
# 删除某条数据DestroyModelMixin，增加某条数据CreateModelMixin

# 对于保存：提交数据原样保存，只要继承CreateModelMixin就行
# GenericViewSet->GenericAPIView->APIView->View(django)
class GoodsViewSet(CacheResponseMixin, GenericViewSet, ListModelMixin, RetrieveModelMixin):
    # throttle_classes = ( AnonRateThrottle, UserRateThrottle,)
    # 商品列表,固定的写法,所有的商品
    queryset = Goods.objects.all()

    # 配置序列化器
    serializer_class = GoodsSerializer

    # 配置分页
    pagination_class = GoodsPagination

    # 配置过滤器和指定过滤的字段
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    # 字段的名称是Model里面有的
    # filterset_fields = ('name', 'shop_price')

    # 过滤器的类,配置的就是自定义的过滤器
    filter_class = GoodsFilter

    # 搜索的字段
    search_fields = ("name", "shop_price", "goods_desc")

    # 根据那些字段排序
    ordering_fields = ("add_time", "shop_price", "sold_num")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # todo 刷站行为 后期采用redis 缓存处理 策略
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# # 覆盖queryset的数据，在基础上进行过滤，shop_price大于或者等于100
# def get_queryset(self):
# 	#shop_price大于或者等于100,能返回
# 	pricemin = self.request.query_params.get("pricemin",0)#100
# 	#如果传入参数
# 	if pricemin:
# 		self.queryset = self.queryset.filter(shop_price__gte=int(pricemin))
# 	return self.queryset


# 商品类别的接口
class GoodsCategoryViewSet(GenericViewSet,  # 分页，设置序列化器，得到所有数据
                           ListModelMixin,  # 取出所有的商品列表
                           RetrieveModelMixin,  # 得到某一条商品类别
                           ):
    # 配置得到所有的商品类别的数据，取所有数据的时候根据category_type=1
    # 所有的数据都是一级类目
    queryset = GoodsCategory.objects.filter(category_type=1)

    # 配置序列化器
    serializer_class = GoodsCategorySerializer1


class BannerViewSet(GenericViewSet, ListModelMixin):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class IndexGoodsCategoryViewSet(GenericViewSet, ListModelMixin):
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexGoodsCategorySerializer
