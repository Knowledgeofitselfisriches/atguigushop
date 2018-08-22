__author__ = '杨光福IT讲师'
# from rest_framework.serializers import Serializer,ModelSerializer
#rest_framework库就是django-rest-framework这个库
from rest_framework import serializers
from .models import Goods, GoodsCategory, GoodsImage


#序列化器,把python对象序列化成网络中中传输字符串（二进制）
#Serializer最基本的序列化器，灵活，自定义序列化的时候用到
#ModelSerializer功能比较强大，能很方便序列化我model
# ModelSerializer继承Serializer

# class GoodsListSerializer(serializers.Serializer):
# 	#序列化商品名称
# 	name = serializers.CharField()
# 	click_num  = serializers.IntegerField()
# 	goods_front_image = serializers.ImageField()
class CategorySerializer(serializers.ModelSerializer):

	#千万不能写漏
	class Meta:
		#商品类别
		model = GoodsCategory
		fields = "__all__"

class GoodsImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = GoodsImage
		fields = ["image"]
#以后大部分请求使用ModelSerializer，自定义某个字段的时候Serializer
class GoodsSerializer(serializers.ModelSerializer):
	#一对多，序列化多张图
	images = GoodsImageSerializer(many=True)

	#字段的名称
	category = CategorySerializer()

	#内部写一个类
	class Meta:
		#明确指定序列化哪个model
		model = Goods
		#指定序列化的字段
		# fields = ("name","click_num","goods_front_image","shop_price")
		#也可以吧Model所有的字段序列化
		fields = "__all__"

# 商品类别的二级类目的序列化器
class GoodsCategorySerializer3(serializers.ModelSerializer):
	class Meta:
		# 指定要序列化model
		model = GoodsCategory
		# 配置要序列化的字段
		fields = "__all__"


# 商品类别的二级类目的序列化器
class GoodsCategorySerializer2(serializers.ModelSerializer):
	#二级类目和三级类目对应关系：一对多的关系，序列化多条商品类目为三级类目的数据
	sub_cat = GoodsCategorySerializer3(many=True)
	class Meta:
		# 指定要序列化model
		model = GoodsCategory
		# 配置要序列化的字段
		fields = "__all__"


#商品类别的一级类目的序列化器
class GoodsCategorySerializer1(serializers.ModelSerializer):

	#指向二级类目：一级类目和二级类目对应关系一对多的关系
	sub_cat = GoodsCategorySerializer2(many=True)

	# 内部写一个类
	class Meta:
		# 明确指定序列化哪个model
		model = GoodsCategory
		# 指定序列化的字段
		# fields = ("name","click_num","goods_front_image","shop_price")
		# 也可以吧Model所有的字段序列化
		fields = "__all__"
