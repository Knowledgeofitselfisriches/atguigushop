__author__ = '杨光福IT讲师'

from .models import UserFav,UserLeavingMessage,UserAddress
import xadmin

class UserFavAdmin(object):
	pass


class UserLeavingMessageAdmin(object):
	pass


class UserAddressAdmin(object):
	pass


xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserLeavingMessage,UserLeavingMessageAdmin)
xadmin.site.register(UserAddress,UserAddressAdmin)


