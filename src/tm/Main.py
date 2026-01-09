# -*- encoding: utf-8 -*-
"""
2024-04-20 by xwq
@DESC:

"""
import decimal
from datetime import datetime, date, timedelta
from typing import Union

from src.tm.path.alud.Main import getAlud
from src.tm.path.qyzt.Main import getQyzt, getYesterdayQyzt
from src.tm.path.sej.Main import getSej, getYesterdaySej
from src.tm.path.tbzb.Main import getTbzb
from src.tm.path.wxt.Main import getWxt
from src.tm.utils.FileManager import FileManager


def div(dividend: decimal.Decimal, divisor: decimal.Decimal) -> decimal.Decimal | str:
    if divisor == 0:
        return '除数为0，无法计算'
    return dividend / divisor


def getKonoTm() -> dict[str, Union[str, decimal.Decimal]]:
    """
    获取kono天猫的实时数据
    :return:
    """
    now: datetime = datetime.now()
    alud: dict[str, decimal.Decimal] = getAlud()
    sej: dict[str, decimal.Decimal] = getSej()
    # tblm: dict[str, dict[str, decimal.Decimal]] = getTblm()
    wxt: dict[str, dict[str, decimal.Decimal]] = getWxt()
    qyzt: dict[str, decimal.Decimal] = getQyzt()

    result: dict[str, Union[str, decimal.Decimal]] = {
        "日期": now.strftime("%Y-%m-%d"),
        "获取时间": now.strftime("%Y-%m-%d %H:%M:%S"),
        "沙龙消耗": (slxh := alud['沙龙消耗']),
        "沙龙成交": (slcj := alud['沙龙成交']),
        "沙龙ROI": div(slcj, slxh),
        "经典消耗": (jdxh := alud['经典消耗']),
        "经典总成交": (jdcj := alud['经典成交']),
        "经典ROI": div(jdcj, jdxh),
        "新香氛消耗": decimal.Decimal(0),
        "新香氛成交": decimal.Decimal(0),
        "新香氛ROI": decimal.Decimal(0),
        "达播销售额": (
                sej['今日top10/直播间']
                - sej['今日top10/烈儿宝贝直播间']
                + sej['B站专属']
                + sej['烈儿宝贝直播间']
                + sej['香菇618']
        ),
        "关键词消耗": wxt['关键词推广']['花费'],
        "关键词直接成交": wxt['关键词推广']['直接成交金额'],
        "关键词总成交": wxt['关键词推广']['总成交金额'],
        "精准人群消耗": wxt['精准人群推广']['花费'],
        "精准人群直接成交": wxt['精准人群推广']['直接成交金额'],
        "精准人群总成交": wxt['精准人群推广']['总成交金额'],
        "万相台消耗": (
                wxt['内容营销/超级短视频']['花费']
                + wxt['活动场景']['花费']
                + wxt['货品运营']['花费']
                + wxt['货品运营/上新快']['花费']
        ),
        "万相台总成交": (
                wxt['内容营销/超级短视频']['总成交金额']
                + wxt['活动场景']['总成交金额']
                + wxt['货品运营']['总成交金额']
                + wxt['货品运营/上新快']['总成交金额']
        ),
        "超级直播消耗": wxt['内容营销/超级直播']['花费'],
        "超级直播成交": wxt['内容营销/超级直播']['总成交金额'],
        "全域智投消耗": qyzt['花费'],
        "全域智投成交": qyzt['总成交金额'],
        "全站推广消耗": wxt['全站推广']['花费'],
        "全站推广直接成交": wxt['全站推广']['直接成交金额'],
        "全站推广总成交": wxt['全站推广']['总成交金额'],
    }

    result['达播佣服'] = result['达播销售额'] * decimal.Decimal('0.2')
    result['全店销售额'] = sej['销售额'] - result['达播销售额']

    adsDeal: list[str] = [
        '经典总成交', '沙龙成交', '新香氛成交', '达播销售额', '关键词总成交', '精准人群总成交', '万相台总成交',
        '超级直播成交', '全域智投成交', '全站推广总成交'
    ]
    result['广告总成交'] = decimal.Decimal(0)
    for field in adsDeal:
        result['广告总成交'] += result[field]
    adsCost: list[str] = [
        '经典消耗', '沙龙消耗', '新香氛消耗', '关键词消耗', '精准人群消耗',
        '万相台消耗', '超级直播消耗', '全域智投消耗', '全站推广消耗'
    ]
    result['广告总消耗'] = decimal.Decimal(0)
    for field in adsCost:
        result['广告总消耗'] += result[field]
    result['广告总ROI'] = div(result['广告总成交'], result['广告总消耗'])

    """
    【广告直接成交数据】
    广告直接成交：42706.7  =（直接成交相加+万相台总成交+淘客成交+站外总成交）
    广告总消耗：14631.63
    广告直接ROI：2.92 =广告直接成交/总消耗
    """
    result['广告直接成交'] = decimal.Decimal(0)
    for field in ['关键词直接成交', '精准人群直接成交', '全站推广直接成交']:
        result['广告直接成交'] += result[field]
    result['广告总消耗'] = result['广告总消耗']
    result['广告直接ROI'] = div(result['广告直接成交'], result['广告总消耗'])

    fileManager: FileManager = FileManager()
    lastResult: dict[str, str] = fileManager.getLastHourRealtimeData()
    if lastResult:
        outSiteCost: list[str] = ['经典消耗', '沙龙消耗', '新香氛消耗']
        result['站外时段消耗'] = decimal.Decimal(0)
        for field in outSiteCost:
            result['站外时段消耗'] += result[field] - decimal.Decimal(lastResult[field])
        outSiteDeal: list[str] = ['经典总成交', '沙龙成交', '新香氛成交']
        result['站外时段成交'] = decimal.Decimal(0)
        for field in outSiteDeal:
            # result['站外时段成交'] += result[field] - decimal.Decimal(lastResult[field])
            if field == '经典总成交':
                result['站外时段成交'] += result[field] - decimal.Decimal(
                    lastResult.get('经典总成交', lastResult.get('经典成交', 0)))
            else:
                result['站外时段成交'] += result[field] - decimal.Decimal(lastResult[field])
        result['站外时段ROI'] = div(result['站外时段成交'], result['站外时段消耗'])

        inSiteCost: list[str] = ['关键词消耗', '精准人群消耗', '万相台消耗', '超级直播消耗', '全域智投消耗',
                                 '全站推广消耗']
        result['站内时段消耗'] = decimal.Decimal(0)
        for field in inSiteCost:
            result['站内时段消耗'] += result[field] - decimal.Decimal(lastResult[field])
        inSiteDeal: list[str] = ['关键词总成交', '精准人群总成交', '万相台总成交', '超级直播成交', '全域智投成交',
                                 '全站推广总成交']
        result['站内时段成交'] = decimal.Decimal(0)
        for field in inSiteDeal:
            # result['站内时段成交'] += result[field] - decimal.Decimal(lastResult[field])
            if field == '关键词总成交':
                result['站内时段成交'] += result[field] - decimal.Decimal(
                    lastResult.get('关键词总成交', lastResult.get('关键词成交', 0)))
            elif field == '精准人群总成交':
                result['站内时段成交'] += result[field] - decimal.Decimal(
                    lastResult.get('精准人群总成交', lastResult.get('精准人群成交', 0)))
            elif field == '万相台总成交':
                result['站内时段成交'] += result[field] - decimal.Decimal(
                    lastResult.get('万相台总成交', lastResult.get('万相台成交', 0)))
            elif field == '全站推广总成交':
                result['站内时段成交'] += result[field] - decimal.Decimal(
                    lastResult.get('全站推广总成交', lastResult.get('全站推广成交', 0)))
            else:
                result['站内时段成交'] += result[field] - decimal.Decimal(lastResult[field])
        result['站内时段ROI'] = div(result['站内时段成交'], result['站内时段消耗'])
    else:
        result['站外时段消耗'] = '无'
        result['站外时段成交'] = '无'
        result['站外时段ROI'] = '无'
        result['站内时段消耗'] = '无'
        result['站内时段成交'] = '无'
        result['站内时段ROI'] = '无'

    outSiteRate: list[str] = ['经典消耗', '沙龙消耗', '新香氛消耗']
    result['站外占比'] = decimal.Decimal(0)
    for field in outSiteRate:
        result['站外占比'] += result[field]
    result['站外占比'] = div(result['站外占比'], result['全店销售额'])
    inSiteRate: list[str] = ['关键词消耗', '精准人群消耗', '万相台消耗', '超级直播消耗', '全域智投消耗', '全站推广消耗']
    result['站内占比'] = decimal.Decimal(0)
    for field in inSiteRate:
        result['站内占比'] += result[field]
    result['站内占比'] = div(result['站内占比'], result['全店销售额'])
    result['全店占比'] = div(result['广告总消耗'], result['全店销售额'])

    return result


def getYesterdayKonoTm():
    """
    获取kono天猫的昨日数据
    :return:
    """
    now: datetime = datetime.now()
    yesterday: date = datetime.today() - timedelta(days=1)
    sej: dict[str, decimal.Decimal] = getYesterdaySej()
    wxt: dict[str, dict[str, decimal.Decimal]] = getWxt(yesterday)
    qyzt: dict[str, decimal.Decimal] = getYesterdayQyzt()
    tbzb: dict[str, decimal.Decimal] = getTbzb()

    result: dict[str, str | decimal.Decimal] = {
        '日期': yesterday.strftime('%Y-%m-%d'),
        '获取时间': now.strftime('%Y-%m-%d %H:%M:%S'),
        '达播销售额': (
                sej['直播间'] + sej['B站专属'] + sej['烈儿宝贝直播间'] + sej['香菇618']
        ),
        "关键词消耗": wxt['关键词推广']['花费'],
        "关键词成交": wxt['关键词推广']['总成交金额'],
        "精准人群消耗": wxt['精准人群推广']['花费'],
        "精准人群成交": wxt['精准人群推广']['总成交金额'],
        "万相台消耗": (
                wxt['内容营销/超级短视频']['花费']
                + wxt['活动场景']['花费']
                + wxt['货品运营']['花费']
                + wxt['货品运营/上新快']['花费']
        ),
        "万相台成交": (
                wxt['内容营销/超级短视频']['总成交金额']
                + wxt['活动场景']['总成交金额']
                + wxt['货品运营']['总成交金额']
                + wxt['货品运营/上新快']['总成交金额']
        ),
        "超级直播消耗": wxt['内容营销/超级直播']['花费'],
        "超级直播成交": wxt['内容营销/超级直播']['总成交金额'],
        "扣退销售额": tbzb.get('直播成交金额', decimal.Decimal(0)) - tbzb.get('退款商品金额', 0),
        "全域智投消耗": qyzt['花费'],
        "全域智投成交": qyzt['总成交金额'],
        "全站推广消耗": wxt['全站推广']['花费'],
        "全站推广成交": wxt['全站推广']['总成交金额'],
        "经典销售额": '无',
        "云感销售额": '无',
        "沙龙销售额": '无',
        "香氛销售额": '无',
        "超级短视频消耗": wxt['内容营销/超级短视频']['花费'],
        "超级短视频成交": wxt['内容营销/超级短视频']['总成交金额'],
        "超级短视频ROI": wxt['内容营销/超级短视频']['ROI'],
    }

    result['达播佣服'] = result['达播销售额'] * decimal.Decimal('0.2')

    result['全店销售额'] = sej['昨日销售额'] - result['达播销售额']

    fileManager: FileManager = FileManager()
    lastMidnight: dict[str, str] = fileManager.getLastMidnightRealtimeData()
    if lastMidnight is None:
        result['站外占比'] = '无'

        result['经典消耗'] = '无'
        result['经典成交'] = '无'
        result['经典ROI'] = '无'
        result['沙龙消耗'] = '无'
        result['沙龙成交'] = '无'
        result['沙龙ROI'] = '无'
        result['新香氛消耗'] = decimal.Decimal('0')
        result['新香氛成交'] = decimal.Decimal('0')
        result['新香氛ROI'] = decimal.Decimal('0')
    else:
        fields: tuple[str, ...] = ('沙龙消耗', '经典消耗', '新香氛消耗')
        result['站外占比'] = decimal.Decimal('0')
        for field in fields:
            result['站外占比'] += decimal.Decimal(lastMidnight[field])
        result['站外占比'] = div(result['站外占比'], result['全店销售额'])

        result['经典消耗'] = decimal.Decimal(lastMidnight['经典消耗'])
        result['经典成交'] = decimal.Decimal(lastMidnight['经典总成交'])
        result['经典ROI'] = div(result['经典成交'], result['经典消耗'])
        result['沙龙消耗'] = decimal.Decimal(lastMidnight['沙龙消耗'])
        result['沙龙成交'] = decimal.Decimal(lastMidnight['沙龙成交'])
        result['沙龙ROI'] = div(result['沙龙成交'], result['沙龙消耗'])
        result['新香氛消耗'] = decimal.Decimal('0')
        result['新香氛成交'] = decimal.Decimal('0')
        result['新香氛ROI'] = decimal.Decimal('0')

    fields: tuple[str, ...] = ('达播销售额', '关键词成交', '精准人群成交', '万相台成交', '超级直播成交',
                               '全域智投成交', '全站推广成交', '经典成交', '沙龙成交', '新香氛成交')
    result['广告总成交'] = decimal.Decimal('0')
    for field in fields:
        result['广告总成交'] += result[field] if result[field] != '无' else decimal.Decimal('0')

    fields: tuple[str, ...] = ('关键词消耗', '精准人群消耗', '万相台消耗', '超级直播消耗', '全域智投消耗',
                               '全站推广消耗', '经典消耗', '沙龙消耗', '新香氛消耗')
    result['广告总消耗'] = decimal.Decimal('0')
    for field in fields:
        result['广告总消耗'] += result[field] if result[field] != '无' else decimal.Decimal('0')

    result['广告总ROI'] = div(result['广告总成交'], result['广告总消耗'])

    fields: tuple[str, ...] = (
        '关键词消耗', '精准人群消耗', '万相台消耗', '超级直播消耗', '全域智投消耗', '全站推广消耗',)
    result['站内占比'] = decimal.Decimal('0')
    for field in fields:
        result['站内占比'] += result[field]
    result['站内占比'] = div(result['站内占比'], result['全店销售额'])

    result['全店占比'] = div(result['广告总消耗'], result['全店销售额'])

    return result


def getYesterdayRealtimeKonoTm() -> dict[str, str] | None:
    """
    获取昨日同时段的kono天猫的实时数据
    :return:
    """
    fileManager: FileManager = FileManager()
    yestedaySameHour: dict[str, str] = fileManager.getRealtimeData(dt=(datetime.now() - timedelta(days=1)))
    return yestedaySameHour
