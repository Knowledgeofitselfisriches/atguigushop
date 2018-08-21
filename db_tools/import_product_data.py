import os

__author__ = '杨光福IT讲师'

#1.模拟pyhton正式model环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AtguiguShop.settings")

#2.导入django设置
import django
django.setup()


#3.导入数据，和对应的Model
from db_tools.data.product_data import row_data

from goods.models import Goods,GoodsCategory, GoodsImage

for goods_detail in row_data:
	# print(goods_detail)
	instance = Goods()
	instance.market_price = float(goods_detail["market_price"].replace("￥","").replace("元",""))
	#商品名称
	instance.name = goods_detail["name"] if goods_detail["name"] is not None else ""
	#商品简单描述
	instance.goods_brief = goods_detail["desc"] if goods_detail["desc"] else ""
	#本店价格
	instance.shop_price = float(goods_detail["sale_price"].replace("￥","").replace("元",""))
	#商品详细介绍
	instance.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] else ""

	#商品的封面
	instance.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""


	#设置商品属于哪个商品类别
	categorys_name = goods_detail["categorys"][-1]#'根茎类',或者
	#查询数据库看看根茎类，是否存在
	categorys = GoodsCategory.objects.filter(name=categorys_name)#返回的是列

	if categorys:
		#商品数据哪个类目
		instance.category = categorys[0]

	#保存商品数据
	instance.save()

	#保存商品轮播图
	for image in goods_detail["images"]:
		print(image)
		goods_image = GoodsImage()
		#商品--商品轮播图和商品建立关系
		goods_image.goods = instance
		#图片
		goods_image.image = image
		#保存商品轮播图
		goods_image.save()






