#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : 全店销售额

"""
import decimal
import re
from datetime import datetime

import requests
from lxml import etree


def getStorewideSales(
        session: requests.Session
) -> dict[str, decimal.Decimal]:
    """
    获取一次生e经-首页-销售额
    + 达播销售额
    :param session:
    :return dict[str, str]
    """
    # 请求
    # https://f0.shengejing.com/summary_shopdata.php?someday=20240421&bborderby=trans
    saleUrl: str = (f'https://f0.shengejing.com/summary_shopdata.php?'
                    f'someday={datetime.now().strftime("%Y%m%d")}&bborderby=trans')
    html: str = session.get(saleUrl).text

    # 取 销售额
    values: str = re.findall('##(.*)##', html)[0]
    values = values.replace(' ', '')
    value: str = values.split(',')[0]
    value: decimal.Decimal = decimal.Decimal(value)

    # 取 今日top10直播间
    top10live: decimal.Decimal = decimal.Decimal('0')
    for e in etree.HTML(html).xpath('//tr[td[2]/a[contains(text(), "直播间")]]/td[3]'):
        top10live += decimal.Decimal(e.text)

    # 取 今日top10烈儿宝贝直播间
    top10le: decimal.Decimal = decimal.Decimal('0')
    for e in etree.HTML(html).xpath('//tr[td[2]/a[contains(text(), "烈儿宝贝直播间")]]/td[3]'):
        top10le += decimal.Decimal(e.text)

    return {
        '销售额': value,
        '今日top10/直播间': top10live,
        '今日top10/烈儿宝贝直播间': top10le
    }
