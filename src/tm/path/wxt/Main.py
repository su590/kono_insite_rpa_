# -*- encoding: utf-8 -*-
"""
2024-04-24 by xwq
@DESC: 万相台的各项推广数据

"""
import datetime
import decimal
import json
import os

import requests

from sdk.encrypt import md5
from src import logger
from src.tm.path.wxt.ActivityScene import getActivityScene
from src.tm.path.wxt.Almm import getCookies
from src.tm.path.wxt.CheckAccess import getCsrfId
from src.tm.path.wxt.GlobalAds import getGlobalAds
from src.tm.path.wxt.GoodsOperation import getGoodsOperation
from src.tm.path.wxt.KwAds import getKwAds
from src.tm.path.wxt.NewArrivalsFast import getNewArrivalsFast
from src.tm.path.wxt.PreciseAds import getPreciseAds
from src.tm.path.wxt.StoreOperation import getStoreOperation
from src.tm.path.wxt.SuperLivestreaming import getSuperLivestreaming
from src.tm.path.wxt.SuperShortVideos import getSuperShortVideos
from src.tm.utils.Accounts import getAccount, Account


def tryGetWxt(
        account: str,
        password: str,
        date: datetime.date,
) -> dict[str, dict[str, decimal.Decimal]]:
    """
    尝试按日期获取万相台的各项数据
    :param account: 
    :param password: 
    :param date: 
    :return: 
    """
    # 获取session
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)[md5(f"{account};{password}")]
    session: requests.Session = requests.session()
    session.cookies.update(cookies)

    # 依次请求
    csrfId: str = getCsrfId(session)
    result: dict[str, dict[str, decimal.Decimal]] = {
        '活动场景': getActivityScene(session, csrfId, date),
        '全站推广': getGlobalAds(session, csrfId, date),
        '关键词推广': getKwAds(session, csrfId, date),
        '精准人群推广': getPreciseAds(session, csrfId, date),
        '内容营销/超级直播': getSuperLivestreaming(session, csrfId, date),
        '内容营销/超级短视频': getSuperShortVideos(session, csrfId, date),
        '货品运营': getGoodsOperation(session, csrfId, date),
        '货品运营/上新快': getNewArrivalsFast(session, csrfId, date),
        '店铺运营': getStoreOperation(session, csrfId, date)
    }

    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)
    cookies[md5(f"{account};{password}")] = session.cookies.get_dict()
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)

    return result


def getWxt(date: datetime.date = None) -> dict[str, dict[str, decimal.Decimal]]:
    date = date or datetime.date.today()
    wxt: Account = getAccount('wxt')
    try:
        result: dict[str, dict[str, decimal.Decimal]] = tryGetWxt(wxt.user, wxt.pwd, date)
    except Exception as e:
        logger.error(e)
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
            cookies: dict = json.load(f)
        cookies[md5(f"{wxt.user};{wxt.pwd}")] = getCookies(wxt)
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)
        result: dict[str, dict[str, decimal.Decimal]] = tryGetWxt(wxt.user, wxt.pwd, date)
    return result
