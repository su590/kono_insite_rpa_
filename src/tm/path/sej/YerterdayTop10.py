#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-06
@Author   : xwq
@Desc     : <None>

"""
import decimal

import requests
from lxml import etree


def belong(name: str, keywords: list[str]) -> bool:
    """
    name是否包含keywords的任一个
    :param keywords:
    :param name:
    :return:
    """
    for keyword in keywords:
        if keyword in name:
            return True
    return False


def getYerterdayTop10(
        session: requests.Session
) -> decimal.Decimal:
    """
    获取一次 生e经-首页-昨日top中含有特定关键词的销售额
    :param session:
    :return dict[str, str]
    """
    # 请求
    url: str = 'https://f0.shengejing.com/summary_baobeidata.php?col=trans&sort=trans&sortorder=desc'
    html: str = session.get(url).text
    value: decimal.Decimal = decimal.Decimal('0')
    for tr in etree.HTML(html).cssselect('tbody tr'):
        name: str = tr.xpath('./td[2]/a[1]')[0].text.strip()
        if belong(name, ['直播间']):
            value += decimal.Decimal(tr.xpath('./td[3]')[0].text.strip())
    return value
