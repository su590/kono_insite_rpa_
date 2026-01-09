# -*- coding: utf-8 -*-  
"""
@date : 2024/6/1
@author: 许伟淇
@describe: 

"""
import decimal
import json
import os

from _decimal import Decimal

from src import logger
from src.tm.path.qyzt.Login import getCookies
from src.tm.path.qyzt.Query import getNowQuery, getYesterdayQuery
from src.tm.utils.Accounts import Account, getAccount


def getQyzt() -> dict[str, Decimal]:
    qyzt: Account = getAccount('qyzt')
    try:
        result: dict[str, decimal.Decimal] = getNowQuery()
    except Exception as e:
        logger.warning(e)
        cookies: dict = getCookies(qyzt)
        with open(os.path.join(os.path.dirname(__file__), 'resource', 'Cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        result: dict[str, decimal.Decimal] = getNowQuery()
    return result


def getYesterdayQyzt() -> dict[str, Decimal]:
    qyzt: Account = getAccount('qyzt')
    try:
        result: dict[str, decimal.Decimal] = getYesterdayQuery()
    except Exception as e:
        logger.warning(e)
        cookies: dict = getCookies(qyzt)
        with open(os.path.join(os.path.dirname(__file__), 'resource', 'Cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        result: dict[str, decimal.Decimal] = getYesterdayQuery()
    return result
