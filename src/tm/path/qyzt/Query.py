# -*- coding: utf-8 -*-  
"""
@date : 2024/6/1
@author: 许伟淇
@describe: 

"""
import decimal
import json
import os
import time
from datetime import timedelta, date

import requests

from src.tm.path.qyzt.CheckAccess import getCsrfId
from src.tm.path.qyzt.SessionController import getSession


def getQuery(payload: dict) -> dict[str, decimal.Decimal]:
    """
    请求全媒体智投数据
    参考 https://ud.alimama.com/index.html#!/manage/smart?bizCode=udGlobalSmart&tab=campaign&startTime=2024-06-07&endTime=2024-06-07
    :param payload: post参数项
    :return:
    """
    with open(os.path.join(os.path.dirname(__file__), 'resource', 'QueryHeaders.json'), 'r', encoding='utf-8') as f:
        headers: dict = json.load(f)
    session: requests.Session = getSession()
    datas: dict = session.post(
        url='https://ud.alimama.com/report/query.json',
        headers=headers,
        data=payload
    ).json()
    dataList: list[dict] = datas['data'].get('list', [{}])
    dataList = dataList or [{}]
    result: dict[str, decimal.Decimal] = {
        '花费': decimal.Decimal(dataList[0].get('charge', '0')),
        '总成交金额': decimal.Decimal(dataList[0].get('alipayInshopAmt', '0')),
    }
    return result


def getNowQuery() -> dict[str, decimal.Decimal]:
    with open(os.path.join(os.path.dirname(__file__), 'resource', 'QueryPayload.json'), 'r', encoding='utf-8') as f:
        payload: dict = json.load(f)
    payload['csrfId'] = getCsrfId(getSession())
    today: date = date.today()
    today: str = today.strftime('%Y-%m-%d')
    payload['startTime'] = today
    payload['endTime'] = today
    payload['timeStr'] = int(time.time() * 1000)
    return getQuery(payload)


def getYesterdayQuery() -> dict[str, decimal.Decimal]:
    with open(os.path.join(os.path.dirname(__file__), 'resource', 'QueryPayload.json'), 'r', encoding='utf-8') as f:
        payload: dict = json.load(f)
    payload['csrfId'] = getCsrfId(getSession())
    yesterday: date = date.today() - timedelta(days=1)
    yesterday: str = yesterday.strftime('%Y-%m-%d')
    payload['startTime'] = yesterday
    payload['endTime'] = yesterday
    payload['timeStr'] = int(time.time() * 1000)
    payload['splitType'] = 'day'
    return getQuery(payload)
