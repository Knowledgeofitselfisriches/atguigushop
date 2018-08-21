# -*- coding: utf-8 -*-

# pip install pycryptodome(一定要安装这个包)
# pip install winrandom


from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes

import json


# 阿里支付类
class AliPay(object):
    """
    支付宝支付接口
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.importKey(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    # 1.根据商品信息如何生成支付链接

    # 实例化阿里支付这个类
    alipay = AliPay(
        appid="2016091800536282",
        # 支付宝服务器主动通知商户服务器里指定的页面http/https路径
        app_notify_url="http://127.0.0.1:8000/alipay/return/",
        app_private_key_path="../trade/keys/private_key.txt",
        alipay_public_key_path="../trade/keys/pay_key.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False生产，debug=True开发环境，沙箱环境,
        # 同步通知，回调这个地址
        return_url="http://127.0.0.1:8000/alipay/return/"
    )

    url = alipay.direct_pay(
        subject="买一件内裤",  # 订单的标题
        # 订单号
        out_trade_no="201808211222",  # 每次测试的时候，修改该字段
        # 支付的总金额
        total_amount=100
    )
    # 沙箱环境
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    print("生成的支付链接：")
    print(re_url)

    # return_url = 'http://118.190.202.67:8000/?total_amount=0.01&timestamp=2017-08-15+17%3A15%3A13&sign=jnnA1dGO2iu2ltMpxrF4MBKE20Akyn%2FLdYrFDkQ6ckY3Qz24P3DTxIvt%2BBTnR6nRk%2BPAiLjdS4sa%2BC9JomsdNGlrc2Flg6v6qtNzTWI%2FEM5WL0Ver9OqIJSTwamxT6dW9uYF5sc2Ivk1fHYvPuMfysd90lOAP%2FdwnCA12VoiHnflsLBAsdhJazbvquFP%2Bs1QWts29C2%2BXEtIlHxNgIgt3gHXpnYgsidHqfUYwZkasiDGAJt0EgkJ17Dzcljhzccb1oYPSbt%2FS5lnf9IMi%2BN0ZYo9%2FDa2HfvR6HG3WW1K%2FlJfdbLMBk4owomyu0sMY1l%2Fj0iTJniW%2BH4ftIfMOtADHA%3D%3D&trade_no=2017081521001004340200204114&sign_type=RSA2&auth_app_id=2016080600180695&charset=utf-8&seller_id=2088102170208070&method=alipay.trade.page.pay.return&app_id=2016080600180695&out_trade_no=201702021222&version=1.0'
#
# o = urlparse(return_url)
# query = parse_qs(o.query)
# processed_query = {}
# ali_sign = query.pop("sign")[0]
# for key, value in query.items():
#     processed_query[key] = value[0]
# print(alipay.verify(processed_query, ali_sign))
