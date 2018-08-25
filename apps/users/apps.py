from django.apps import AppConfig


class UsersConfig(AppConfig):
    # name = 'apps.users'
    name = 'users'  # 正确的
    verbose_name = "用户管理"

    # def ready(self):
        # import users.signals
