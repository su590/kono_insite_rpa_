# -*- coding: utf-8 -*-
"""
@date : 2024/5/24
@author: 许伟淇
@describe:

"""
import random
import time

import requests


def get_sms_captcha(typ: str) -> str | None:
    """
    获取手机短信验证码
    使用举例：get_sms_captcha("抖店魔渍")
    :param typ: 验证码的type，如 "抖店魔渍"
    :return:
    """
    res: requests.Response = requests.get(
        url=f"http://10.1.140.31:7997/getcode?type={typ}",
    )
    if res.status_code == 200:
        return res.text
    return None


def get_new_sms_captcha(typ: str, old_captcha: str, timeout: float = 600, raise_err: bool = False) -> str | None:
    """
    获取新的验证码
    :param typ: 验证码type
    :param old_captcha: 旧验证码
    :param timeout: 限时
    :param raise_err: 超时是否报错，否则返回None
    :return:
    """
    new_captcha: str = get_sms_captcha(typ)
    while timeout > 0 and new_captcha == old_captcha:
        sleep: float = random.random() * 10
        timeout -= sleep
        time.sleep(sleep)
        new_captcha: str = get_sms_captcha(typ)
    if new_captcha != old_captcha:
        return new_captcha
    if raise_err:
        raise TimeoutError('短信超时')
    return None
