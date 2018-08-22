from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField

# Create your models here.

#商品类别
class GoodsCategory(models.Model):
	CATEGORY_TYPE = (
		(1,"一级商品类别"),
		(2,"二级商品类别"),
		(3,"三级商品类别")
	)
	# 商品类别的名称: name
	name = models.CharField(max_length=30,verbose_name="类别的名称",default="")
	# 商品类目的编码：code
	code = models.CharField(max_length=30,null=True,blank=True,verbose_name="类别编码code",default="")
	# 当前类目: category_type
	category_type = models.IntegerField(choices=CATEGORY_TYPE,verbose_name="商品类别")
	# 类别的描述：desc
	desc = models.CharField(max_length=100,null=True,blank=True,verbose_name="类别描述")
	# 类目的父级：parent_category,一定要设置null=True,blank=True
	parent_category = models.ForeignKey("self",related_name="sub_cat",null=True,blank=True,verbose_name="父级商品类目")
	# 是否添加到导航：is_tab
	is_tab = models.BooleanField(default=False,verbose_name="是否添加到导航栏")

	# 添加时间：add_time, 得到当前时间
	add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")


	class Meta:
		verbose_name = "商品类别"
		#verbose_name_plural 可以让后台的不加上s
		verbose_name_plural = verbose_name

	#在后台管理的时候，显示当前Mode中的信息
	def __str__(self):
		return self.name


#商品品牌
class GoodsCategoryBrand(models.Model):
	# 属于哪个商品类别：category
	category = models.ForeignKey(GoodsCategory,null=True,blank=True,related_name="brands",verbose_name="商品类别")
	# 商品品牌的名字：name
	name = models.CharField(max_length=50,verbose_name="品牌的名称",default="")
	# 商品品牌的描述：desc
	desc = models.CharField(max_length=200,null=True,blank=True,verbose_name="品牌的描述")
	# 图片：image
	image = models.ImageField(max_length=200,upload_to="goods/brands/")
	# 添加时间：add_time, 得到当前时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "商品品牌"
		# verbose_name_plural 可以让后台的不加上s
		verbose_name_plural = verbose_name
		#自定义在数据库的表的名字
		db_table = "goods_goodsbrand"#只有这张表叫这个名字，自定义表明

	# 在后台管理的时候，显示当前Mode中的信息
	def __str__(self):
		return self.name


#商品
class Goods(models.Model):
	# 属于哪个商品类别：category
	category = models.ForeignKey(GoodsCategory,null=True,blank=True,verbose_name="商品类别")

	# 商品的名称：name
	name = models.CharField(max_length=50,default="",verbose_name="商品名称")
	# 商品简单描述：goods_brief
	goods_brief = models.CharField(max_length=200,verbose_name="商品简单描述",null=True,blank=True)
	# 商品编号：goods_sn,全网唯一
	goods_sn = models.CharField(max_length=50,verbose_name="商品编号",null=True,blank=True)
	# 点击量: click_num
	click_num = models.IntegerField(default=0,verbose_name="点击量")
	# 销售量: sold_num
	sold_num = models.IntegerField(default=0,verbose_name="销售量")
	# 库存: goods_num
	goods_num = models.IntegerField(default=0,verbose_name="库存")
	# 收藏数: fav_num
	fav_num = models.IntegerField(default=0,verbose_name="收藏数")
	# 市场价格: market_price
	market_price = models.FloatField(default=0.0,verbose_name="市场价格")
	# 本店价格: shop_price
	shop_price = models.FloatField(default=0.0,verbose_name="本店价格")
	# 封面图片：goods_front_image
	goods_front_image = models.ImageField(max_length=200,blank=True,null=True,upload_to="goods/imags/")
	# 商品简介（富文本）
	goods_desc = UEditorField('内容', width=1000, height=300,  imagePath="goods/ueditor/", filePath="goods/files/",
						    blank=True,null=True)
	# 是否免运费: ship_free
	ship_free = models.BooleanField(default=True,verbose_name="是否包邮费")
	# 是否新品: is_new
	is_new = models.BooleanField(default=False,verbose_name="是否新商品")
	# 是否热销: is_hot
	is_hot = models.BooleanField(default=False,verbose_name="是否热销商品")
	#添加时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "商品"
		# verbose_name_plural 可以让后台的不加上s
		verbose_name_plural = verbose_name

	# 在后台管理的时候，显示当前Mode中的信息
	def __str__(self):
		return self.name


#商品的轮播图
class GoodsImage(models.Model):

	#商品
	goods = models.ForeignKey(Goods,related_name="images",verbose_name="商品")
	#图片,upload_to上传图片的位置/media/goods/goosimages/
	image = models.ImageField(upload_to="goods/goodsimages/",verbose_name="图片",blank=True,null=True)
	#添加时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "商品的轮播图"
		# verbose_name_plural 可以让后台的不加上s
		verbose_name_plural = verbose_name

	# 在后台管理的时候，显示当前Mode中的信息
	def __str__(self):
		return self.goods.name



#首页的轮播图
class Banner(models.Model):
	#商品，点击的时候，跳转到对应的商品里面
	goods = models.ForeignKey(Goods, verbose_name="商品")
	#图片
	image = models.ImageField(upload_to="goods/banners/",verbose_name="图片")
	#播放顺序
	index = models.IntegerField(default=1,verbose_name="图片轮播的顺序")
	# 添加时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "首页的轮播图"
		# verbose_name_plural 可以让后台的不加上s
		verbose_name_plural = verbose_name

	# 在后台管理的时候，显示当前Mode中的信息
	def __str__(self):
		return self.goods.name





