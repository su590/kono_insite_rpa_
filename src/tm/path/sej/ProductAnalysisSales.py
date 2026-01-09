#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : 生e经 - 宝贝分析 - "关键词" - 销售额

"""
import decimal
from datetime import datetime

import requests


_PRODUCT_HEADERS: dict[str, str] = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "f0.shengejing.com",
    "Pragma": "no-cache",
    "Referer": "https://f0.shengejing.com/index.php?tab=12",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}
_PRODUCT_PARAMS: dict = {
    "view": "base",
    "dd": "20240601",
    "_": "1717219339153",
    "sEcho": "5",
    "iColumns": "21",
    "iDisplayStart": "0",
    "iDisplayLength": "10",
    "sSearch": "today",
    "bRegex": "false",
    "sSearch_0": "B站专属",
    "bRegex_0": "false",
    "bSearchable_0": "true",
    "bRegex_1": "false",
    "bSearchable_1": "true",
    "bRegex_2": "false",
    "bSearchable_2": "true",
    "bRegex_3": "false",
    "bSearchable_3": "true",
    "bRegex_4": "false",
    "bSearchable_4": "true",
    "bRegex_5": "false",
    "bSearchable_5": "true",
    "bRegex_6": "false",
    "bSearchable_6": "true",
    "bRegex_7": "false",
    "bSearchable_7": "true",
    "bRegex_8": "false",
    "bSearchable_8": "true",
    "bRegex_9": "false",
    "bSearchable_9": "true",
    "bRegex_10": "false",
    "bSearchable_10": "true",
    "bRegex_11": "false",
    "bSearchable_11": "true",
    "bRegex_12": "false",
    "bSearchable_12": "true",
    "bRegex_13": "false",
    "bSearchable_13": "true",
    "bRegex_14": "false",
    "bSearchable_14": "true",
    "bRegex_15": "false",
    "bSearchable_15": "true",
    "bRegex_16": "false",
    "bSearchable_16": "true",
    "bRegex_17": "false",
    "bSearchable_17": "true",
    "bRegex_18": "false",
    "bSearchable_18": "true",
    "bRegex_19": "false",
    "bSearchable_19": "true",
    "bRegex_20": "false",
    "bSearchable_20": "true",
    "iSortingCols": "1",
    "iSortCol_0": "4",
    "sSortDir_0": "desc",
    "bSortable_0": "true",
    "bSortable_1": "false",
    "bSortable_2": "false",
    "bSortable_3": "false",
    "bSortable_4": "true",
    "bSortable_5": "true",
    "bSortable_6": "true",
    "bSortable_7": "true",
    "bSortable_8": "true",
    "bSortable_9": "true",
    "bSortable_10": "true",
    "bSortable_11": "true",
    "bSortable_12": "true",
    "bSortable_13": "true",
    "bSortable_14": "true",
    "bSortable_15": "true",
    "bSortable_16": "true",
    "bSortable_17": "true",
    "bSortable_18": "true",
    "bSortable_19": "true",
    "bSortable_20": "false"
}


def getProductAnalysisSales(session: requests.Session, keyword: str) -> decimal.Decimal:
    """
    获取生e经 - 宝贝分析 - "keyword" - 销售额
    :param session:
    :param keyword:
    :return:
    """
    # 组装参数
    headers: dict = _PRODUCT_HEADERS.copy()
    params: dict = _PRODUCT_PARAMS.copy()
    params['dd'] = datetime.today().strftime('%Y%m%d')
    params['sSearch_0'] = keyword
    page_size: int = 10
    params['iDisplayLength'] = page_size
    url: str = f'https://f0.shengejing.com//baobei_trans_data.php'

    # 累计值
    value: decimal.Decimal = decimal.Decimal('0.0')

    # 第一次请求
    FIRST_PAGE_NO: int = 0
    FIRST_ECHO: int = 0
    page_no: int = FIRST_PAGE_NO
    echo: int = FIRST_ECHO
    params['iDisplayStart'] = page_no
    params['sEcho'] = echo
    datas: dict = session.get(url=url, headers=headers, params=params).json()
    for x in datas['aaData']:
        value += decimal.Decimal(x[4])
    total: int = datas['iTotalDisplayRecords']
    total_pages: int = total // page_size + 1

    # 循环请求剩余页
    for i in range(total_pages - 1):
        page_no += 1
        echo += 1
        params['iDisplayStart'] = page_no
        params['sEcho'] = echo
        datas: dict = session.get(url=url, headers=headers, params=params).json()
        for x in datas['aaData']:
            value += decimal.Decimal(x[4])

    return value
