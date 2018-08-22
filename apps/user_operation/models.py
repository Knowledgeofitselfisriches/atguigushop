from django.db import models

from django.contrib.auth import get_user_model
from goods.models import Goods
from datetime import datetime
#得到系统配置的用户


UserProfile = get_user_model()

class UserFav(models.Model):
	"""用户收藏"""
	#用户
	user = models.ForeignKey(UserProfile,verbose_name="用户")
	#商品
	goods = models.ForeignKey(Goods,verbose_name="商品")
	#添加时间,datetime.now()代码编译的时间，datetime.now：该条数据添加的时间
	add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

	class Meta:
		verbose_name = "用户收藏"
		verbose_name_plural = verbose_name
		#某个用户对某个商品只能收藏一次，但是呢可以由多个用户收藏
		unique_together = ("user","goods")


	def __str__(self):
		return "%s收藏了：%s" %(self.user.username,self.goods.name)


class UserLeavingMessage(models.Model):
	"""用户留言"""
	MSG_TYPE = (
		(1,"留言"),
		(2,"投诉"),
		(3,"表扬"),
		(4,"求购"),
		(5,"售后")
	)
	# 用户：user
	user = models.ForeignKey(UserProfile, verbose_name="用户")
	# 留言主题：subject
	subject = models.CharField(max_length=50,verbose_name="留言主题")
	# 留言的类型（1, 留言；2, 投诉, 3, 表扬, 4, 求购，5，售后）：msg_type
	message_type = models.IntegerField(verbose_name="留言类型",choices=MSG_TYPE,help_text="1, 留言；2, 投诉, 3, 表扬, 4, 求购，5，售后")
	# 留言的内容：message
	message = models.CharField(max_length=200,verbose_name="留言内容")
	# 留言的文件：file
	file = models.FileField(upload_to="message/files/",verbose_name="留言附件",help_text="留言附件")
	#添加时间,datetime.now()代码编译的时间，datetime.now：该条数据添加的时间
	add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

	class Meta:
		verbose_name = "用户留言"
		verbose_name_plural = verbose_name


	def __str__(self):
		return self.subject


#用户收货地址
class UserAddress(models.Model):
	# 用户：user
	user = models.ForeignKey(UserProfile, verbose_name="用户")
	# 省：province
	province = models.CharField(max_length=30,verbose_name="省")
	# 市：city
	city = models.CharField(max_length=30, verbose_name="市")
	# 区县：district
	district = models.CharField(max_length=30, verbose_name="区县")
	# 地址：address
	address = models.CharField(max_length=30, verbose_name="地址")
	signer_name = models.CharField(max_length=30, verbose_name="签收人")
	# 签收电话：singer_mobile
	signer_mobile = models.CharField(max_length=11, verbose_name="签收电话")

	# 添加时间,datetime.now()代码编译的时间，datetime.now：该条数据添加的时间
	add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

	class Meta:
		verbose_name = "用户收货地址"
		verbose_name_plural = verbose_name

	def __str__(self):
		return "%s省 %s市 %s区 %s" % (self.province,self.city,self.district,self.address)