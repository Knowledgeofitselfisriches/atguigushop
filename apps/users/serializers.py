from users.models import VerifyCode

from rest_framework import serializers
import re
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator

UserProfile = get_user_model()


class VerifyCodeSerializer(serializers.Serializer):  # 默认的保存就会有问题

    email = serializers.CharField(max_length=30, min_length=11)

    def validate_email(self, email):
        # 是否是正确的邮箱
        if not re.match(r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$", email):
            raise serializers.ValidationError("请输入正确的邮箱！")

        # 是否注册--查找UserProfile表
        if UserProfile.objects.filter(email=email).count():
            raise serializers.ValidationError("该邮箱已经注册！")

        # 是否频频发送
        # 1分钟
        one_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # result = VerifyCode.objects.filter(add_time__gt=one_ago, mobile=mobile)
        if VerifyCode.objects.filter(add_time__gt=one_ago, email=email).count():
            raise serializers.ValidationError("1分钟以后再获取验证码")

        return email


# 用户注册的序列化器
class UserProfileSerializer(serializers.ModelSerializer):

    code = serializers.CharField(help_text="验证码", label="手机收到的验证码", write_only=True, allow_blank=False,
                                 max_length=4, min_length=4, required=True)

    username = serializers.CharField(help_text="用户注册手机号", label="注册手机号/邮箱", required=True, allow_blank=False,
                                     validators=[ UniqueValidator(queryset=UserProfile.objects.all(),
                                                                  message="注册的手机号或者用户名不能重复")])

    password = serializers.CharField(help_text="用户登录密码", write_only=True, label="注册密码", required=True,
                                     allow_blank=False, min_length=6, style={"input_type": "password"})

    def create(self, validated_data):

        user = super(UserProfileSerializer, self).create(validated_data)
        password = validated_data["password"]
        user.set_password(password)  # 从明文中再次加密
        user.save()

        return user

    # 参数code是用户输入
    def validate_code(self, code):

        # 从请求的参数得到手机号
        email = self.initial_data["username"]
        # 根据手机号得到所有的验证码列表，并且排序
        # verify_codes = VerifyCode.objects.filter(mobile=mobile).order_by("-add_time")
        verify_codes = VerifyCode.objects.filter(email=email).order_by("-add_time")
        # 1.验证码是否存在,如果存在，就得到第0个，否则就是不存在
        if verify_codes:
            # 保存在数据库，并且是最新的验证码
            last_code = verify_codes[0]

            # 2.验证码输入是否正确，要求输入最后一个发生的验证码
            if last_code.code.lower() != code.lower():
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
        attrs["email"] = attrs["username"]
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
