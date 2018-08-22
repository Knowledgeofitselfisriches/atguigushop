from django.db.models import Q

__author__ = '杨光福IT讲师'
from goods.models import Goods
from django_filters import rest_framework as filters
#model名称+Filter
class GoodsFilter(filters.FilterSet):
	#最小价格100  ---> 大于或者等于
	pricemin = filters.NumberFilter(field_name="shop_price",lookup_expr="gte")

	#最大价格200 --- > 小于或者等于
	pricemax = filters.NumberFilter(field_name="shop_price",lookup_expr="lte")

	#检索name字段对应的内容： 我是中国人-->人，我，中国人
	name = filters.CharFilter(field_name="name",lookup_expr="icontains")

	#自定义top_category过滤字段,名字不能改
	top_category = filters.NumberFilter(method="filter_top_category")

	#调用方法，返回什么就得到什么数据
	#第一个GoodsFilter实例对象，第二参数：所有商品数据集合，第三个参数top_category，第四个参数商品类别的id
	def filter_top_category(self, queryset, name, value):
		# print("self==",self)
		# print("queryset==", queryset)
		# print("queryset size==",len(queryset))
		# #top_category
		# print("name==",name)
		# #1,24,40 商品类别的id号
		# print("value==",value)
		#如果没有传入top_category，返回没有过滤的数据
		if name:
			#根据传入的商品列表的id，查找该商类别对应的商品，并且返回列表
			#category_id和category__id等价
			#category__parent_category__id 和category__parent_category_id 等价
			queryset = queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value))
			return queryset

		return queryset

	#内部类
	class Meta:
		#指定对Goods进行过滤
		model = Goods
		fields = ("pricemin","pricemax","name","is_hot")