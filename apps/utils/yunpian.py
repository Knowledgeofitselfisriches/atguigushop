__author__ = '杨光福IT讲师'
import requests
import json
#云片网，发短信
class YunPian(object):
	def __init__(self):
		#云片网，账号对应的apikey，
		self.apikey = "4f70824dde066067241393c80c291ea6"
		#使用post请求该路径
		self.url = "https://sms.yunpian.com/v2/sms/single_send.json"


	#发送短信的方法
	def send_msg(self,mobile,code):

		#数据将会以请求体的方式请求
		data = {
			"apikey":self.apikey,
			"mobile":mobile,
			"text":"【尚硅谷商城】您的验证码是%s。如非本人操作，请忽略本短信" % code#模板是申请号的
		}
		#使用requests库发出post请求
		reponse = requests.post(self.url,data=data)
		text_str = reponse.text#str
		# print("text==",text_str)
		# print("text_str-type==",type(text_str))
		#把str -->dict
		text_dict = json.loads(text_str)
		# print("text_dict--type==", type(text_dict))
		return text_dict


#使用并且测试
if __name__ == "__main__":
	yp = YunPian()
	result =yp.send_msg("18920055059","1111")
	print("收到的短信===",result)



