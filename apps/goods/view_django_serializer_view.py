from django.views import View
from .models import Goods
from django.http.response import HttpResponse, JsonResponse
from django.core import serializers


# django 的View
# 新增加django 的序列化器
class GoodsListDjangoSerializerView(View):

    # 重写get方法
    def get(self, request):
        print("request==", request)
        goods_list = Goods.objects.all()
        print("goods_list==", goods_list)
        # 把model（Python对象）的数据，转换成可以在网络中传输的数据 -- 序列化
        # 使用了django的序列化 --工具类 序列化器

        # 字符串，转换成json数据
        data = serializers.serialize("json", goods_list)
        print("data type", type(data))

        # 第一方式返回

        # 返回数据,Content-Type: application/json,告诉浏览器，json数据
        # return HttpResponse(data,"application/json")
        import json
        # 把字符串转换列表或者字典
        data = json.loads(data)
        # 第二种方式返回
        # safe=False,
        return JsonResponse(data, safe=False, )
