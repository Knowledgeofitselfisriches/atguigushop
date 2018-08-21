# _*_ coding:utf-8 _*_
import string
import random


def verify_code(length):
    s = string.ascii_letters
    n = string.digits
    source = f"{s}{n}"
    code = "".join(random.sample(source, length))
    return code


def short_message(length=4):
    source = string.digits
    code = "".join(random.sample(source, length))
    return code


if __name__ == '__main__':
    print(short_message(4))
