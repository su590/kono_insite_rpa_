#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : <None>

"""
import decimal
import json
import os

import requests

from sdk.encrypt import md5
from src import logger
from src.tm.path.sej.Login import getCookies
from src.tm.path.sej.ProductAnalysisSales import getProductAnalysisSales
from src.tm.path.sej.SalesOverview import getSalesOverview
from src.tm.path.sej.StorewideSales import getStorewideSales
from src.tm.path.sej.YerterdayTop10 import getYerterdayTop10
from src.tm.path.sej.YesterdayProductAnalysisSales import getYesterdayProductAnalysisSales
from src.tm.utils.Accounts import Account, getAccount


def tryGetSej(account: Account) -> dict[str, decimal.Decimal]:
    """
    尝试获取生e经
    :param account:
    :return:
    """
    # 取 session
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)[md5(f"{account.user};{account.pwd}")]
    session: requests.Session = requests.session()
    session.cookies.update(cookies)

    # 记录结果
    results: dict[str, decimal.Decimal] = {}

    # 取 销售额、达播销售额
    value: dict[str, decimal.Decimal] = getStorewideSales(session)
    results |= value

    # 取 宝贝分析-销售额
    results['B站专属'] = getProductAnalysisSales(session, keyword='B站专属')
    results['烈儿宝贝直播间'] = getProductAnalysisSales(session, keyword='烈儿宝贝直播间')
    results['香菇618'] = getProductAnalysisSales(session, keyword='香菇618')

    # 保存最新Cookies
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)
    cookies[md5(f"{account.user};{account.pwd}")] = session.cookies.get_dict()
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)

    return results


def getSej() -> dict[str, decimal.Decimal]:
    """
    获取实时生e经数据
    :return:
    """
    sej: Account = getAccount('sej')
    try:
        results: dict[str, decimal.Decimal] = tryGetSej(account=sej)
    except Exception as e:
        logger.error(e)
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
            cookies: dict = json.load(f)
        cookies[md5(f"{sej.user};{sej.pwd}")] = getCookies(account=sej)
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        results: dict[str, decimal.Decimal] = tryGetSej(account=sej)
    return results


def tryGetYesterdaySej(account: Account) -> dict[str, decimal.Decimal]:
    """
    尝试获取 昨日 - 生e经 的各项数据
    :param account:
    :return:
    """
    # 取 session
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)[md5(f"{account.user};{account.pwd}")]
    session: requests.Session = requests.session()
    session.cookies.update(cookies)

    # 记录结果
    results: dict[str, decimal.Decimal] = {
        '直播间': getYerterdayTop10(session),
        'B站专属': getYesterdayProductAnalysisSales(session=session, keyword='B站专属'),
        '烈儿宝贝直播间': getYesterdayProductAnalysisSales(session=session, keyword='烈儿宝贝直播间'),
        '香菇618': getYesterdayProductAnalysisSales(session=session, keyword='香菇618'),
        '昨日销售额': getSalesOverview(session)
    }

    # 保存最新Cookies
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)
    cookies[md5(f"{account.user};{account.pwd}")] = session.cookies.get_dict()
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)

    return results


def getYesterdaySej() -> dict[str, decimal.Decimal]:
    """
    获取昨日的生e经数据
    :return:
    """
    sej: Account = getAccount('sej')
    try:
        results: dict[str, decimal.Decimal] = tryGetYesterdaySej(account=sej)
    except Exception as e:
        logger.error(e)
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
            cookies: dict = json.load(f)
        cookies[md5(f"{sej.user};{sej.pwd}")] = getCookies(account=sej)
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        results: dict[str, decimal.Decimal] = tryGetYesterdaySej(account=sej)
    return results


if __name__ == '__main__':
    print(getSej())
    pass
