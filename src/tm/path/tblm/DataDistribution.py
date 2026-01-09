#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : <None>

数据分布(付款支出费用/付款金额) < 今日实时 < 推广概览 < 数据分析 < 淘宝联盟-商家中心
参考 https://ad.alimama.com/portal/v2/report/promotionDataPage.htm

"""
import decimal
import json
import os
from datetime import datetime, date

import requests

from sdk.encrypt import md5
from src import logger
from src.tm.path.tblm.Almm import getCookies
from src.tm.utils.Accounts import Account

_SJFB_PARAMS: dict = {
    "t": 1713774807691,
    "_tb_token_": "e0e669711dee7",
    "startDate": "2024-04-22",
    "endDate": "2024-04-22",
    "period": "1d"
}
_SJFB_HEADERS: dict[str, str] = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Bx-V": "2.5.11",
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Pragma": "no-cache",
    "Referer": "https://ad.alimama.com/portal/v2/report/promotionDataPage.htm",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
_SPWD_PARAMS: dict = {
    "t": 1716536511260,
    "_tb_token_": '34d5e61ee5a47',
    "level1Dim": '2',
    "level2Dim": '2_1',
    "level3Dim": '2_1_1',
    "level4Type": "item",
    "orderMetric": 'alipayAmt',
    'orderType': 'desc',
    # 'period': 'today',
    'period': 'customDateRange',
    'groupId': None,
    'itemId': None,
    'eventValue': None,
    'startDate': '2024-05-24',
    'endDate': '2024-05-24',
    "pageNum": 1,
    "pageSize": 20,
}


def belong(name: str, keywords: list[str]) -> bool:
    for keyword in keywords:
        if keyword in name:
            return True
    return False


def tryGetDataDistribution(
        account: Account,
        dat: date,
) -> dict[str, dict[str, decimal.Decimal]]:
    """
    获取一次淘客数据 - 数据分布
    :param account: 账号
    :param dat: 请求日期，
    :return
    """
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)[md5(f"{account.user};{account.pwd}")]
    session: requests.Session = requests.session()
    session.cookies.update(cookies)

    # 请求 数据分布
    params: dict = _SJFB_PARAMS.copy()
    params['t'] = int(datetime.now().timestamp() * 1000)
    params['_tb_token_'] = cookies['_tb_token_']
    params['startDate'] = dat.strftime('%Y-%m-%d')
    params['endDate'] = dat.strftime('%Y-%m-%d')
    headers: dict = _SJFB_HEADERS.copy()
    ans: requests.Response = session.get(
        url='https://ad.alimama.com/openapi/param2/1/gateway.unionadv/analysis.overview.dimLevelTree.json',
        headers=headers,
        params=params
    )
    ansJson: dict = ans.json()

    # 记录结果
    result: dict[str, dict[str, decimal.Decimal]] = {}

    # 取 付款金额、付款支出费用
    name2type: dict[str, str] = {
        '1': '自主推广',
        '2': '服务商合作',
        '3': '官方营销活动',
    }
    result |= {'付款金额': {}, '付款支出费用': {}}
    for item in ansJson['data']:
        typ: str = name2type.get(item['name'], '未知')
        result['付款金额'][typ] = decimal.Decimal(item['reportData'].get('alipayAmt', 0))
        result['付款支出费用'][typ] = decimal.Decimal(item['reportData'].get('preTotalFee', 0))

    # 请求 商品维度
    params: dict = _SPWD_PARAMS.copy()
    params['t'] = int(datetime.now().timestamp()*1000)
    params['t'] = cookies['_tb_token_']
    params['startDate'] = dat.strftime('%Y-%m-%d')
    params['endDate'] = dat.strftime('%Y-%m-%d')
    headers: dict = _SJFB_HEADERS.copy()
    ans: requests.Response = session.get(
        url='https://ad.alimama.com/openapi/param2/1/gateway.unionadv/analysis.overview.topList.json',
        headers=headers,
        params=params
    )
    ansJson: dict = ans.json()

    # 取 直播间的付款金额、付款支出费用
    alipayAmt: decimal.Decimal = decimal.Decimal(0)
    preTotalFee: decimal.Decimal = decimal.Decimal(0)
    for item in ansJson['data'].get('list', []):
        if belong(item['itemName'], ['直播间', '香菇618', 'B站专属', '烈儿宝贝直播间']):
            alipayAmt += decimal.Decimal(item['alipayAmt'])
            preTotalFee += decimal.Decimal(item['preTotalFee'])

    # 记录商品维度
    result['付款金额']['商品维度'] = alipayAmt
    result['付款支出费用']['商品维度'] = preTotalFee

    # 保存cookies
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)
    cookies[md5(f"{account.user};{account.pwd}")] = session.cookies.get_dict()
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)

    return result


def getDataDistribution(account: Account, dat: date) -> dict[str, dict[str, decimal.Decimal]]:
    try:
        result: dict[str, dict[str, decimal.Decimal]] = tryGetDataDistribution(account, dat)
    except Exception as e:
        logger.error(e)
        with open(os.path.join(os.path.dirname(__file__), 'cookies.json'), 'r', encoding='utf-8') as f:
            cookies: dict = json.load(f)
        cookies[md5(f"{account.user};{account.pwd}")] = getCookies(account)
        with open(os.path.join(os.path.dirname(__file__), 'cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        result: dict[str, dict[str, decimal.Decimal]] = tryGetDataDistribution(account, dat)
    return result
