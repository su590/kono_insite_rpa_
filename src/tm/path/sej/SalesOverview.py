#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-06
@Author   : xwq
@Desc     : <None>

"""
import decimal
import re

import requests
from lxml import etree


def getSalesOverview(
        session: requests.Session,
) -> decimal.Decimal:
    """
    获取生e经-销售分析-销售概况
    参考 https://f0.shengejing.com/index.php?tab=10
    :param session:
    :return:
    """
    reponse: str = session.get(
        url='https://f0.shengejing.com/index.php?tab=10',
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "f0.shengejing.com",
            "Pragma": "no-cache",
            "Referer": "https://f0.shengejing.com/index.php?login=true",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
    ).text
    text: str = etree.HTML(reponse).xpath('//td[contains(text(), "昨天销售数据")]/../td[@headers="汇总数据"]')[0].text
    text: str = re.sub('[\n\t ]', '', text)
    value: str = re.findall('(\d+(\.\d+)?)', text)[0][0]

    return decimal.Decimal(value)
