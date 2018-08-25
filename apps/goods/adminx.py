from .models import GoodsCategory, GoodsCategoryBrand, Goods, GoodsImage, Banner, IndexCategoryAd
import xadmin


class GoodsCategoryAdmin(object):
    # 列表方式显示
    list_display = ["id", "name", "category_type", "parent_category", "is_tab"]
    # 过滤的字段
    list_filter = ["category_type", "parent_category", "name"]


class GoodsCategoryBrandAdmin(object):

    def get_context(self):
        context = super(GoodsCategoryBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context


class GoodsAdmin(object):
    # 这些字段，以列表的方式显示
    list_display = ["name", "category",
                    "goods_sn", "click_num", "sold_num", "goods_num", "fav_num", "is_new", "is_hot",
                    "market_price", "shop_price", "goods_brief"]
    # 添加搜索的字段
    search_fields = ["name", "goods_sn", "click_num", "sold_num", "goods_num", "fav_num", "is_new", "is_hot",
                     "market_price", "shop_price", "goods_brief"]
    # 富文本显示
    style_fields = {"goods_desc": "ueditor"}

    class GoodsIamgesInlines(object):
        # 编辑model
        model = GoodsImage
        # 样式-表格
        style = "tab"
        # 每次能添加多少个
        extra = 2

    # 注意对齐
    inlines = [GoodsIamgesInlines]


class GoodsImageAdmin(object):
    pass


class BannerAdmin(object):
    pass


class IndexCategoryAdAdmin(object):
    def get_context(self):
        context = super(IndexCategoryAdAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context


# 注册商品类别model到后台管理
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
# 注册商品品牌model到后台管理
xadmin.site.register(GoodsCategoryBrand, GoodsCategoryBrandAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(IndexCategoryAd, IndexCategoryAdAdmin)
