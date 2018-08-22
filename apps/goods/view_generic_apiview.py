from rest_framework.pagination import PageNumberPagination

from goods.models import Goods
from goods.serializers import GoodsSerializer

__author__ = '杨光福IT讲师'

from rest_framework import generics
from rest_framework import mixins

#mixins 模块
#CreateModelMixin 创建数据，保存数据 -- 客户端发起post向服务器提交数据
#ListModelMixin 把数据库的数据，以列表的方式返回 ---客户端发起get请求，得到列表数据
#RetrieveModelMixin 得到列表中某一条数据， ---客户端发起get请求，得到某条数据
#UpdateModelMixin  更新某条数据       ---客户端发起的put请求 ，返回更新后的数据
#DestroyModelMixin  删除某一条数据     ---客户端发起 delete请求，返回空文档





#要得到商品列表,继承GenericAPIView，ListModelMixin得到列表
# class GoodsListGenericAPIView(generics.GenericAPIView,mixins.ListModelMixin):
#
# 	#得到商品列表
# 	queryset = Goods.objects.all()
#
# 	#配置序列化器
# 	serializer_class = GoodsListSerializer
#
# 	#忘记get
# 	def get(self,request):
# 		#调用了ListModelMixin的list方法
# 		return self.list(request)

#商品列表的分页
class GoodsListPagination(PageNumberPagination):
	#每页返回10
	page_size = 10
	#使用的字段
	page_size_query_param = 'page_size'
	#自定义页码对应的字段
	page_query_param = "page"
	#最多100
	max_page_size = 100

#要得到商品列表,继承GenericAPIView，ListModelMixin得到列表

#ListAPIView 继承GenericAPIView继承APIView继承View（django）
#GenericAPIView:可以配置queryset，配置序列化器serializer_class，配置分页pagination_class
class GoodsListGenericAPIView(generics.ListAPIView):

	#得到商品列表
	queryset = Goods.objects.all()

	#配置序列化器
	serializer_class = GoodsSerializer

	#配置分页
	pagination_class = GoodsListPagination

	# def get(self,request):
	# 	return self.list(request)



