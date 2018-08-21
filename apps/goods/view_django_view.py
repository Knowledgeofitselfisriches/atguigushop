from django.views import View
from .models import Goods
from django.http.response import HttpResponse


# 使用django的View
class GoodsListDjangoView(View):

    # 重写get方法
    def get(self, request):
        print("request==", request)
        goods_list = Goods.objects.all()[:10]
        print("goods_list==", goods_list)

        # 列表数据，装字典
        goods_lists = []
        for good in goods_list:
            # 字典
            item_dict = {}
            item_dict["name"] = good.name
            item_dict["shop_price"] = good.shop_price
            # item_dict["goods_front_image"] = good.goods_front_image
            # item_dict["add_time"] = good.add_time
            item_dict["click_num"] = good.click_num

            # 把字典添加到列表里面
            goods_lists.append(item_dict)

        import json

        # '{"name":"afu"}'
        # '[1,2,3]'

        # jons库，把python 列表，字典，转换成字符串，把字符串 转换列表，或者字典

        # 列表转换成python字符串
        data = json.dumps(goods_lists)

        # 返回数据,Content-Type: application/json,告诉浏览器，json数据
        return HttpResponse(data, "application/json")
