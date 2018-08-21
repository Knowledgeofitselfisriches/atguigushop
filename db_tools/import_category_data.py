import os

__author__ = '杨光福IT讲师'

# 1.模拟pyhton正式model环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AtguiguShop.settings")

# 2.导入django设置
import django

django.setup()

# 3.导入data/category_data.py文件里面row_data
from db_tools.data.category_data import row_data
# 导入goods/models.py/GoodsCategory类，并且实例化，存数据，--->数据库
from goods.models import GoodsCategory

# 实验：没有模拟pyhton正式model环境和导入django设置，请求下保存数据，是否可行---？不可行
# from users.models import VerifyCode
#
# verifycode = VerifyCode()
# verifycode.code = "1234"
# verifycode.mobile = "18601042258"
# verifycode.save()


# 存数据，--->数据库
for item1 in row_data:
    instance1 = GoodsCategory()
    instance1.category_type = 1  # 当前就是一级商品类目
    instance1.name = item1["name"]  # 商品类别的名称
    instance1.code = item1["code"]  # 商品类别的编码
    instance1.save()  # 保存数据库

    for item2 in item1["sub_categorys"]:
        instance2 = GoodsCategory()
        instance2.category_type = 2  # 当前就是二级商品类目
        instance2.name = item2["name"]  # 商品类别的名称
        instance2.code = item2["code"]  # 商品类别的编码
        instance2.parent_category = instance1  # 上级商品类目
        instance2.save()  # 保存到数据库

        for item3 in item2["sub_categorys"]:
            instance3 = GoodsCategory()
            instance3.category_type = 3  # 当前就是二级商品类目
            instance3.name = item3["name"]  # 商品类别的名称
            instance3.code = item3["code"]  # 商品类别的编码
            instance3.parent_category = instance2  # 上级商品类目
            instance3.save()  # 保存到数据库
            print(item3)
