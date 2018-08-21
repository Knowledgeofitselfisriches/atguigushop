from users.models import VerifyCode

from rest_framework import serializers
import re
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator

# 获取配置的用户
UserProfile = get_user_model()


# 在序列化器验证手机号：是否注册，是否是正确的手机号，是否频频发送
class VerifyCodeSerializer(serializers.Serializer):  # 默认的保存就会有问题
    # 自定义交易手机号,对长度的校验
    mobile = serializers.CharField(max_length=11, min_length=11)

    def validate_mobile(self, mobile):
        # 是否是正确的手机号
        if not re.match(r"1[3456789]\d{9}$", mobile):
            raise serializers.ValidationError("你输入不是手机号！")

        # 是否注册--查找UserProfile表
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机已经注册！")

        # 是否频频发送
        # 1分钟
        one_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # result = VerifyCode.objects.filter(add_time__gt=one_ago, mobile=mobile)
        if VerifyCode.objects.filter(add_time__gt=one_ago, mobile=mobile).count():
            raise serializers.ValidationError("1分钟以后再获取验证码")

        return mobile


# 用户注册的序列化器
class UserProfileSerializer(serializers.ModelSerializer):
    # required=True,该code一定要填写
    # write_only=True，可以序列化，但是不返回接口的调用方（前端），默认是可以保持

    code = serializers.CharField(help_text="验证码", label="手机收到的验证码", write_only=True, allow_blank=False, max_length=4,
                                 min_length=4, required=True)

    # 已经要填写，不允许为空，不能注册重复
    username = serializers.CharField(help_text="用户注册手机号", label="注册手机号", required=True, allow_blank=False, validators=[
        UniqueValidator(queryset=UserProfile.objects.all(), message="注册的手机号或者用户名不能重复")])

    # 用户输入的密码
    password = serializers.CharField(help_text="用户登录密码", write_only=True, label="注册密码", required=True,
                                     allow_blank=False, min_length=6, style={"input_type": "password"})

    # 在保存之前进行加密
    def create(self, validated_data):

        # 返回的就是UserProfile的实例对象，继承AbstractUser，它AbstractUser，有加密的方法
        # super(UserProfileSerializer,self).create(validated_data) 都已经保存数据了，密码是没有加密
        user = super(UserProfileSerializer, self).create(validated_data)
        # 带加密的密码
        password = validated_data["password"]
        # 内部帮我们加密AbstractUser
        user.set_password(password)  # 从明文中再次加密

        # 保存该注册用户,修改
        user.save()

        return user  # 一定要返回保存的用户

    # 参数code是用户输入
    def validate_code(self, code):

        # 从请求的参数得到手机号
        mobile = self.initial_data["username"]
        # 根据手机号得到所有的验证码列表，并且排序
        verify_codes = VerifyCode.objects.filter(mobile=mobile).order_by("-add_time")
        # 1.验证码是否存在,如果存在，就得到第0个，否则就是不存在
        if verify_codes:
            # 保存在数据库，并且是最新的验证码
            last_code = verify_codes[0]

            # 2.验证码输入是否正确，要求输入最后一个发生的验证码
            if last_code.code != code:
                raise serializers.ValidationError("1.有可能验证码输入错误2.可能没有输入最后一次收到的")

            # 3.验证码5分钟后，就提示过期
            five_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if last_code.add_time < five_ago:
                raise serializers.ValidationError("验证码已经过了5分钟，亲，请重新获取验证码！")

        else:
            # 验证码不存在
            raise serializers.ValidationError("验证不存在！")

    # code在UserProfile没有这个字段，所有需要删除
    # 传入进来的是username,本质是手机号，要把username也赋值一份给mobile
    def validate(self, attrs):
        # attrs得到所有传入的参数
        attrs["mobile"] = attrs["username"]
        # 把验证码删除，原因，UserProfile没有code字段
        del attrs["code"]
        return attrs

    class Meta:
        model = UserProfile
        fields = ("username", "code", "password")


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("name", "birthday", "gender", "email", "mobile")
