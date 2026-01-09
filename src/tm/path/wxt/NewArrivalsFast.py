#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : 货品运营 - 上新快

参考 https://one.alimama.com/index.html#!/manage/item?bizCode=onebpAdStrategyShangXin

"""
import datetime
import decimal
import json
import os

import requests

from src.tm.path.wxt._CommonRequest import _commonRequest


def getNewArrivalsFast(
        session: requests.Session,
        csrfId: str,
        date: datetime.date,
) -> dict[str, decimal.Decimal]:
    """
    按日期获取 货品运营/上新快 shuju1
    :param session:
    :param csrfId:
    :param date:
    :return:
    """
    dirname: str = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dirname, 'params', 'NewArrivalsFast.json'), 'r', encoding='utf-8') as f:
        params: dict[str, str] = json.load(f)
    with open(os.path.join(dirname, 'headers', 'NewArrivalsFast.json'), 'r', encoding='utf-8') as f:
        headers: dict[str, str] = json.load(f)
    with open(os.path.join(dirname, 'payload', 'NewArrivalsFast.json'), 'r', encoding='utf-8') as f:
        payload: dict[str, str] = json.load(f)

    return _commonRequest(
        session=session,
        csrfId=csrfId,
        url='https://one.alimama.com/report/query.json',
        params=params,
        headers=headers,
        payload=payload,
        date=date,
    )
