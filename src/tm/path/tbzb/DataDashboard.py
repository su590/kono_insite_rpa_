#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-07
@Author   : xwq
@Desc     : <None>

"""
import datetime
import decimal
import json
import os.path
import re
import time
from urllib.parse import unquote

import execjs
import requests

from src import logger
from src.tm.path.tbzb.Login import getCookies
from src.tm.path.tbzb.SessionController import SessionController
from src.tm.utils.Accounts import Account


def getSign(token: str, data: str, timestamp: int) -> str:
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Sign.js'), 'r', encoding='utf-8'
    ) as f:
        signJsContent: str = f.read()
    signJs: execjs._external_runtime.ExternalRuntime.Context = execjs.compile(signJsContent)
    sign: str = signJs.call(
        'i',
        token + '&' + str(timestamp) + '&' + '12574478' + '&' + data
    )
    return sign


def getYesterdayLiveId() -> str | None:
    """
    获取 直播分场次效果-昨天的场次ID，无则None
    :return:
    """
    sc: SessionController = SessionController()
    headers: dict[str, str] = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://liveplatform.taobao.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    days30Ago: str = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y%m%d')
    yesterday: str = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    data: str = ('{"dataApi":"live_overview_rt_content_v3","param":"{\\"queryCycleStartDate\\":\\"'
                 f'{days30Ago}'
                 '\\",\\"queryCycleEndDate\\":\\"'
                 f'{yesterday}'
                 '\\",\\"beginDate\\":\\"'
                 f'{days30Ago}'
                 '\\",\\"endDate\\":\\"'
                 f'{yesterday}'
                 '\\",\\"queryUserRole\\":\\"ALL\\",\\"start\\":\\"0\\",\\"hit\\":\\"10\\",\\"orderColumn\\":'
                 '\\"live_start_time\\",\\"orderType\\":\\"1\\"}"}')
    token = '_'.join(sc.cookies['_m_h5_tk'].split('_')[:-1])
    timestamp: int = int(time.time() * 1000)
    sign: str = getSign(token=token, data=data, timestamp=timestamp)
    url: str = ('https://h5api.m.taobao.com/h5/mtop.dreamweb.query.general.generalquery/1.0/?jsv=2.6.2&appKey=12574478'
                f'&t={timestamp}'
                f'&sign={sign}'
                '&api=mtop.dreamweb.query.general.generalQuery&v=1.0&dataType=jsonp&preventFallback=true&type=jsonp'
                '&callback=mtopjsonp18'
                f'&data={data}')
    response: requests.Response = sc.session.get(url=url, headers=headers)
    data: dict = json.loads(re.findall(r'\{.*}', response.text, re.DOTALL)[0])
    NOT_EXIST: str = 'NOT_EXIST'
    liveId: str = NOT_EXIST
    yesterday: str = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    for result in data['data']['result']:
        if result['live_start_time'].startswith(yesterday):
            liveId: str = result['content_id']
            break

    sc.saveCookies()
    if liveId == NOT_EXIST:
        return None
    else:
        return liveId


def getValue(oldValue: str) -> str | decimal.Decimal:
    """
    将数值类字符串进行处理，转为decimal，未能识别情况则返回原值
    :param oldValue:
    :return:
    """
    oldValue = re.sub(r'[\n\t ]', '', oldValue)
    try:
        # 123
        if oldValue.isdigit():
            return decimal.Decimal(oldValue)
        # 12,345 型
        if re.fullmatch('\d+(,\d+)*', oldValue) is not None:
            return decimal.Decimal(oldValue.replace(',', ''))
        # 12.5%
        if re.fullmatch('\d+(\.\d+)?%', oldValue) is not None:
            return decimal.Decimal(oldValue[:-1]) / decimal.Decimal('100')
        # 12.5‰
        if re.fullmatch('\d+(\.\d+)?‰', oldValue) is not None:
            return decimal.Decimal(oldValue[:-1]) * decimal.Decimal('1000')
    except Exception as e:
        logger.error(f'淘宝直播数值转换有误，原值={oldValue}，异常={e}')
    return oldValue


def tryGetDataDashboard() -> dict[str, decimal.Decimal | str]:
    """
    获取 淘宝直播 - 数据大屏 内容
    :return:
    """
    liveId: str | None = getYesterdayLiveId()
    if liveId is None:
        return {}
    sc: SessionController = SessionController()
    sc.session.get(f'https://market.m.taobao.com/app/mtb/live-professional-screen/index.html?source=live-war-room&liveId={liveId}#screen=overview')
    token = '_'.join(sc.cookies['_m_h5_tk'].split('_')[:-1])
    startTime: int = int((datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=23, minute=55, second=3).timestamp()) * 1000
    endTime: int = int(datetime.datetime.now().replace(hour=0, minute=0, second=3).timestamp()) * 1000
    data: str = ('{"liveId":"'
                 f'{liveId}'
                 '","types":"totalStats","startTime":'
                 f'{startTime}'
                 ',"endTime":'
                 f'{endTime}'
                 ',"timeType":5,"searchType":"2","extParams":"{}"}')
    timestamp: int = int(time.time() * 1000)
    sign: str = getSign(token=token, data=data, timestamp=timestamp)
    headers: dict[str, str] = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": "https://market.m.taobao.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    url: str = ('https://h5api.m.taobao.com/h5/mtop.taobao.iliad.live.user.assistant.data.get/1.0/?jsv=2.7.0'
                '&appKey=12574478'
                f'&t={timestamp}'
                f'&sign={sign}'
                '&api=mtop.taobao.iliad.live.user.assistant.data.get&v=1.0&jsonpIncPrefix=dc_lsad&preventFallback=true'
                '&type=jsonp&dataType=jsonp&callback=mtopjsonpdc_lsad54'
                f'&data={data}')
    response: requests.Response = sc.session.get(url=url, headers=headers)
    data: dict = json.loads(re.findall(r'\{.*}', response.text, re.DOTALL)[0])
    values: dict[str, decimal.Decimal | str] = {}
    for x in data['data']['dataList'][0]['data']:
        dic: dict = dict(zip(x['format'].strip().split(x['split']),
                             [unquote(v, 'utf-8') for v in x['value'].strip().split(x['split'])]))
        if dic.get('title') and dic.get('value'):
            values[dic['title']] = getValue(dic['value'])
    sc.saveCookies()
    return values


def getDataDashboard(account: Account) -> dict[str, decimal.Decimal]:
    try:
        result: dict[str, decimal.Decimal] = tryGetDataDashboard()
    except Exception as e:
        logger.error(e)
        cookies: dict[str, str] = getCookies(account)
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        result: dict[str, decimal.Decimal] = tryGetDataDashboard()
    return result
