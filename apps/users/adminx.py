# 配置xadmin对应的后台，标题和页脚
import xadmin
from .models import VerifyCode

from xadmin.views import CommAdminView, BaseAdminView


class GlobalSettings(object):
    site_title = "天天生鲜"
    site_footer = "天天集团"
    menu_style = 'accordion'


class VerifyCodeAdmin(object):
    pass


class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True


# 注册全局配置
xadmin.site.register(CommAdminView, GlobalSettings)
xadmin.site.register(BaseAdminView, BaseXadminSetting)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
