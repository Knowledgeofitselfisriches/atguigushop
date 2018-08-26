from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import VerifyCode
from users.serializers import VerifyCodeSerializer, UserProfileSerializer, UserProfileDetailSerializer

from utils.emails import send_email_code
from utils.string_tools import verify_code


# 使用自定义用户替换系统的了
UserProfile = get_user_model()

# def handler404(request):
#     ret = render(request, 'hander404.html')
#     ret.status_code = 404
#     return ret
#
# def handler500(request):
#     ret = render(request, 'hander500.html')
#     ret.status_code = 500
#     return ret


class CustomModelBackend(ModelBackend):

    # 认证--手机号，账号，邮箱 三个都可以登录
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username 可以是手机号，账号，邮箱
        # password 密码
        try:
            # 根据账号或者手机号或者邮箱查询数据，只有一条数据
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))

            # 校验密码是否正确
            if user.check_password(password):
                # 如果密码正确把账号返回
                return user
        except Exception as e:
            print("e==", e)
            return None


# 发送验证码的接
class VerifyCodeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    # 得到所有的验证码
    queryset = VerifyCode.objects.all()

    # 在序列化器验证手机号：是否注册，是否是正确的手机号，是否频频发送
    serializer_class = VerifyCodeSerializer
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        print(request.data)
        request.data['email'] = request.data['mobile']
        del request.data['mobile']
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]

        code = verify_code()
        print("email===", email, "code==", code)
        send_email_code(email, code)
        # {'code': 0, 'msg': '发送成功', 'count': 1, 'fee': 0.05, 'unit': 'RMB', 'mobile': '18813228601', 'sid': 27395798790}
        return Response({"email": email, "msg": 'ok'}, status=status.HTTP_201_CREATED)


from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


# 用户注册,得到某个用户RetrieveModelMixin
class UserProfileViewSet(viewsets.GenericViewSet,
                         mixins.CreateModelMixin,  # 注册用户
                         mixins.RetrieveModelMixin,  # 得到某一条信息RetrieveModelMixin
                         mixins.UpdateModelMixin,  # 添加UpdateModelMixin
                         ):
    """
    create:
        用户手机注册，传入的参数有手机号（username）,验证码code,用户密码password


    """

    # 得到所有的用户
    queryset = UserProfile.objects.all()

    # 判断用户是否登录
    # permission_classes = (IsAuthenticated,)

    # 配置token认证--传入的token-->用户(验证)---后期的用户收藏
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 配置序列化器---要注释掉原来的配置
    # serializer_class = UserProfileSerializer
    # 动态的获取不同的序列化器
    def get_serializer_class(self):

        if self.action == "create":  # 用户注册的时候，需要验证码校验的，返回的数据也只需token
            return UserProfileSerializer
        else:
            return UserProfileDetailSerializer

    # 用户/1  或者/用户/10 --->得到当前登录的用户
    def get_object(self):
        return self.request.user

    # 动态的返回不同的信息，返回IsAuthenticated，做了登录的验证
    # 如果返回[]，就是不做登录的验证
    def get_permissions(self):

        if self.action == "retrieve":
            return [IsAuthenticated()]  # 获取用户的时候，需要权限验证
        else:
            # 注册的情况，是不需要判断是否登录！其他情况，都要补要写权限验证
            return []

    # 重写保存用户方法
    def create(self, request, *args, **kwargs):
        # 得到序列化器UserProfileSerializer
        serializer = self.get_serializer(data=request.data)
        # 做序列化器的验证
        serializer.is_valid(raise_exception=True)
        # UserProfile实例对象
        user = self.perform_create(serializer)

        # 负载
        payload = jwt_payload_handler(user)

        token = jwt_encode_handler(payload)

        response_data = serializer.data
        # 加上token和name ,对应有些接口，已经做了判断是否登录等（已经需要token），已经做做了jwt 认证配置的都要传token,
        response_data["token"] = token
        # 返回name
        response_data["name"] = user.username

        # 得到头信息
        headers = self.get_success_headers(response_data)

        # 返回数据
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 返回的UserProfile实例对象
        return serializer.save()  # 一定要修改成返回值
