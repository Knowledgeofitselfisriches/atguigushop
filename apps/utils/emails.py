# _*_ coding:utf-8 _*_
from django.core.mail import send_mail
from AtguiguShop.settings import EMAIL_FROM, EMAIL_REGISTER
from users.models import VerifyCode


def send_email_code(email, code):
    email_ver = VerifyCode()
    email_ver.email = email
    email_ver.code = code
    email_ver.save()
    print('code', code)
    #第二步，准备参数发送邮件
    send_title = '欢迎注册天天生鲜在线网站'
    send_body = f'你的验证码:{code}\n 是请点击以下链接进行激活:\n '+ EMAIL_REGISTER
    send_mail(send_title, send_body, EMAIL_FROM, [email])