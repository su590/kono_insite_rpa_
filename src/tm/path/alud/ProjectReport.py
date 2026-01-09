#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : 项目报表

参考 https://unidesk.taobao.com/direct/index?t=1713617997955

"""
import json
import os
from datetime import datetime

import requests

from sdk.encrypt import md5
from src import logger
from src.tm.path.alud.Login import getCookies
from src.tm.utils.Accounts import Account

_REPORT_HEADERS: dict[str, str] = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Bx-V": "2.5.11",
    "Referer": "https://unidesk.taobao.com/direct/index?t=1715338012145",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def tryGetProhectReport(account: Account) -> dict[str, int]:
    """
    获取一次"项目报表"的数据
    :param account: 账号
    :return dict[str, int], 除以100即为真实值
    """
    # 取 session
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)[md5(f"{account.user};{account.pwd}")]
    session: requests.Session = requests.session()
    session.cookies.update(cookies)

    # 记录结果
    results: dict[str, int] = {}

    # 循环请求
    headers: dict[str, str] = _REPORT_HEADERS.copy()
    pageNo: int = 1
    total: int = 10 ** 9
    while total > 0:
        # 请求
        url: str = (f'https://unidesk.taobao.com/api/direct/report/project/list?bizType=2&advType=1&customerType=1'
                    f'&directMediaId=103&campaignIds=%5B%5D&adgroupIds=%5B%5D&effect=15&effectType=click&ef=hourId'
                    f"&startTime={datetime.now().strftime('%Y-%m-%d')}&endTime={datetime.now().strftime('%Y-%m-%d')}"
                    f"&advertiserId=&pageNo={pageNo}&pageSize=40&orderField=&orderBy="
                    f'&timeStr={int(datetime.now().timestamp() * 1000)}&bizCode=uniDeskRtaBrand')
        response: requests.Response = session.get(
            url=url,
            headers=headers,
        )
        respJson: dict = response.json()

        # 参数递减
        if total == 10 ** 9:
            total = respJson['data']['count']
        total -= len(respJson['data']['list'])
        pageNo += 1

        # 汇总数值
        for item in filter(lambda x: '沙龙' in x['campaignName'], respJson['data']['list']):
            results['沙龙消耗'] = results.get('沙龙消耗', 0) + item['cost']
            results['沙龙成交'] = results.get('沙龙成交', 0) + item['transactionAmount']
        for item in filter(lambda x: '经典' in x['campaignName'], respJson['data']['list']):
            results['经典消耗'] = results.get('经典消耗', 0) + item['cost']
            results['经典成交'] = results.get('经典成交', 0) + item['transactionAmount']
        pass

    # 保存最新的Cookies
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)
    cookies[md5(f"{account.user};{account.pwd}")] = session.cookies.get_dict()
    with open(os.path.join(os.path.dirname(__file__), 'cookies.json'), 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)

    return results


def getProjectReport(account: Account) -> dict[str, int]:
    """
    获取项目报表
    :param account:
    :return:
    """
    try:
        results: dict[str, int] = tryGetProhectReport(account=account)
    except Exception as e:
        logger.error(e)
        with open(os.path.join(os.path.dirname(__file__), 'cookies.json'), 'r', encoding='utf-8') as f:
            cookies: dict = json.load(f)
        cookies[md5(f"{account.user};{account.pwd}")] = getCookies(account=account)
        with open(os.path.join(os.path.dirname(__file__), 'cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False)
        results: dict[str, int] = tryGetProhectReport(account=account)
    return results
