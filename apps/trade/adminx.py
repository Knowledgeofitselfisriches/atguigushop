
from .models import ShoppingCart, OrderInfo, OrderGoods
import xadmin


class ShoppingCartAdmin(object):
	pass


class OrderInfoAdmin(object):
	pass


class OrderGoodsAdmin(object):
	pass


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderGoods, OrderGoodsAdmin)

