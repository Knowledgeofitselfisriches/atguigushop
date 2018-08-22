from goods.models import Goods

__author__ = '杨光福IT讲师'

from rest_framework.views import APIView
from rest_framework.response import Response

from goods.serializers import GoodsSerializer

from rest_framework.request import Request

#django-rest-framework
#APIView(drf)-->View(django)
class GoodsListAPIView(APIView):
	#传入的request是Request类的实例化对象

	def get(self,request,format=None):

		print("request==",request)
		print("request.user==",request.user)
		print("query_params==",request.query_params)
		print("method==", request.method)

		print("pricemin==",request.query_params.get("pricemin"))
		print("pricemax==", request.query_params.get("pricemax"))

		#得到商品所有的数据
		goods_list = Goods.objects.all()

		#序列化数据
		#第一个参数是数据，第二参数是要序列化多条数据
		serializer = GoodsSerializer(goods_list,many=True)

		#取出序列化后的数据
		data = serializer.data
		print("data==",data)
		print("",type(data))

		response = Response(data=data)
		print("response==",response)
		print("response.data==", response.data)
		print("response.status_code==", response.status_code)

		#返回
		return response