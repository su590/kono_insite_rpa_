# -*- coding: utf-8 -*-  
"""
@Date     : 2024-09-06
@Author   : xwq
@Desc     : KONO实时营销数据

"""
import decimal
import re
from datetime import datetime
from typing import Union

from src import logger
from src.tm.path.alud.Main import getAlud
from src.tm.path.qyzt.Main import getQyzt
from src.tm.path.sej.Main import getSej
from src.tm.path.tblm.Main import getTblm
from src.tm.path.wxt.Main import getWxt
from src.tm.utils.FileManager import FileManager
from src.tm.data.SpreadSheetSaver import SpreadSheetSaver, ApiParam, SpreadSheetField

api_param = ApiParam(
    app_id='cli_a441b931043b9013',
    app_secret='5i78C0KAeSJuLDSzloEECdSCYRfrCST2',
    spreadsheet_token='NGmysFij4hEZM1tPSHdco4OInAe',
    now_sheet_id='0jiSmW',
    history_sheet_id='1eFHlh'
)


def _div(dividend: decimal.Decimal, divisor: decimal.Decimal) -> decimal.Decimal | str:
    if divisor == 0:
        return '除数为0，无法计算'
    return dividend / divisor


_headerTpl = """
KONO实时营销数据
>>日期：{日期}
>>获取时间：{获取时间}
""".strip()
_classicDataTpl = """
【经典数据】
>>经典消耗：{经典消耗}
>>经典总成交：{经典总成交}
>>经典ROI：{经典ROI}
""".strip()
_salonDataTpl = """
【沙龙数据】
>>沙龙消耗：{沙龙消耗}
>>沙龙成交：{沙龙成交}
>>沙龙ROI：{沙龙ROI}
""".strip()
_newFragranceDataTpl = """
【新香氛数据】
>>新香氛消耗：{新香氛消耗}
>>新香氛成交：{新香氛成交}
>>新香氛ROI：{新香氛ROI}
""".strip()
_taobaoAffiliateDataTpl = """
【淘客数据】
>>淘客佣服：{淘客佣服}
>>淘客销售额：{淘客销售额}
>>淘客ROI：{淘客ROI}
""".strip()
_broadcastDataTpl = """
【达播数据】
>>达播佣服：{达播佣服}
>>达播销售额：{达播销售额}
""".strip()
_keywordDataTpl = """
【关键词数据】
>>关键词消耗：{关键词消耗}
>>关键词直接成交：{关键词直接成交}
>>关键词总成交：{关键词总成交}
""".strip()
_preciseAudiencePromotionDataTpl = """
【精准人群推广数据】
>>精准人群消耗：{精准人群消耗}
>>精准人群直接成交：{精准人群直接成交}
>>精准人群总成交：{精准人群总成交}
""".strip()
_wxtDataTpl = """
【万相台数据】
>>万相台消耗：{万相台消耗}
>>万相台总成交：{万相台总成交}
""".strip()
_superLiveDataTpl = """
【超级直播数据】
>>超级直播消耗：{超级直播消耗}
>>超级直播成交：{超级直播成交}
""".strip()
_overallSmartInvestmentDataTpl = """
【全域智投数据】
>>全域智投消耗：{全域智投消耗}
>>全域智投成交：{全域智投成交}
""".strip()
_overallSitePromotionDataTpl = """
【全站推广数据】
>>全站推广消耗：{全站推广消耗}
>>全站推广直接成交：{全站推广直接成交}
>>全站推广总成交：{全站推广总成交}
""".strip()
_adsTotalDataTpl = """
【广告总数据】
>>广告总成交：{广告总成交}
>>广告总消耗：{广告总消耗}
>>广告总ROI：{广告总ROI}
""".strip()
_adsDirectTransactionDataTpl = """
【广告直接成交数据】
>>广告直接成交：{广告直接成交}
>>广告总消耗：{广告总消耗}
>>广告直接ROI：{广告直接ROI}
""".strip()
_outsitePeriodEffectTpl = """
【站外时段效果】
>>站外时段消耗：{站外时段消耗}
>>站外时段成交：{站外时段成交}
>>站外时段ROI：{站外时段ROI}
""".strip()
_insitePeriodEffectTpl = """
【站内时段效果】
>>站内时段消耗：{站内时段消耗}
>>站内时段成交：{站内时段成交}
>>站内时段ROI：{站内时段ROI}
""".strip()
_overallShopSaleTpl = """
【全店销售额】
>>全店销售额：{全店销售额}
>>站外占比：{站外占比}
>>站内占比：{站内占比}
>>全店占比：{全店占比}
""".strip()
_superShortVideoTpl = """
【超级短视频】
>>花费（元）：{超级短视频消耗}
>>种草引导成交金额（元）：{超级短视频成交}
>>种草引导成交ROI：{超级短视频ROI}
""".strip()
_storeOperationTpl = """
【店铺运营】
>>花费：{店铺运营花费}
>>总成交金额：{店铺运营总成交金额}
>>ROI：{店铺运营ROI}
""".strip()


class SpreadSheetFieldTmKono(SpreadSheetField):
    def __init__(self, data: dict):
        # self.date = str(datetime.now().today().date())
        # self.get_time = str(datetime.now().strftime("%H:%M:%S"))
        for key, value in data.items():
            # if re.match(r'\d+(\.\d+)', value):
            #     value = str(round(decimal.Decimal(value), 2))
            setattr(self, key, str(value))

    def to_list(self) -> list:  # 转为列表
        print(list(vars(self).values()))
        return list(vars(self).values())


def getKonoRealtimeMarketingData(
        isMidnight: bool = False,
) -> str:
    """
    获取kono天猫的实时数据
    :param isMidnight: 是否是`23:30的数据`，这回影响数据保存的位置，但获取方式等不变
    :return:
    """
    now: datetime = datetime.now()
    fileManager = FileManager()
    tpls: list[str] = []
    data: dict[str, Union[str, decimal.Decimal]] = {}

    # 表头
    tpls.append(_headerTpl)
    data |= {
        "日期": now.strftime("%Y-%m-%d"),
        "获取时间": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 经典数据
    # todo: 暂时掠过alud
    # alud: dict[str, decimal.Decimal] = getAlud()
    alud: dict[str, decimal.Decimal] = {
        '经典消耗': decimal.Decimal(0),
        '经典成交': decimal.Decimal(0),
        '沙龙消耗': decimal.Decimal(0),
        '沙龙成交': decimal.Decimal(0),
    }
    tpls.append(_classicDataTpl)
    data |= {
        "经典消耗": (jdxh := alud['经典消耗']),
        "经典总成交": (jdcj := alud['经典成交']),
        "经典ROI": _div(jdcj, jdxh),
    }

    # 沙龙数据
    tpls.append(_salonDataTpl)
    data |= {
        "沙龙消耗": (slxh := alud['沙龙消耗']),
        "沙龙成交": (slcj := alud['沙龙成交']),
        "沙龙ROI": _div(slcj, slxh),
    }

    # 新香氛数据
    tpls.append(_newFragranceDataTpl)
    data |= {
        "新香氛消耗": decimal.Decimal(0),
        "新香氛成交": decimal.Decimal(0),
        "新香氛ROI": decimal.Decimal(0),
    }

    # 淘客数据
    tpls.append(_taobaoAffiliateDataTpl)
    tblm: dict[str, dict[str, decimal.Decimal]] = getTblm()
    data |= {
        "淘客佣服": (
            tkyf :=
            tblm['付款支出费用'].get('服务商合作', decimal.Decimal('0'))
            + tblm['付款支出费用'].get('官方营销活动', decimal.Decimal('0'))
            - tblm['付款支出费用'].get('商品维度', decimal.Decimal('0'))
        ),
        "淘客销售额": (
            tkxse :=
            tblm['付款金额'].get('服务商合作', decimal.Decimal('0'))
            + tblm['付款金额'].get('官方营销活动', decimal.Decimal('0'))
            - tblm['付款金额'].get('商品维度', decimal.Decimal('0'))
        ),
        "淘客ROI": _div(tkxse, tkyf),
    }
    # # 无权限，临时置为"无"
    # data |= {
    #     "淘客佣服": '无',
    #     "淘客销售额": '无',
    #     "淘客ROI": '无',
    # }

    # 达播数据
    sej: dict[str, decimal.Decimal] = getSej()
    tpls.append(_broadcastDataTpl)
    data |= {
        "达播销售额": (
                sej['今日top10/直播间']
                - sej['今日top10/烈儿宝贝直播间']
                + sej['B站专属']
                + sej['烈儿宝贝直播间']
                + sej['香菇618']
        ),
    }
    data['达播佣服'] = data['达播销售额'] * decimal.Decimal('0.2')

    # 关键词数据
    wxt: dict[str, dict[str, decimal.Decimal]] = getWxt()
    tpls.append(_keywordDataTpl)
    data |= {
        "关键词消耗": wxt['关键词推广']['花费'],
        "关键词直接成交": wxt['关键词推广']['直接成交金额'],
        "关键词总成交": wxt['关键词推广']['总成交金额'],
    }

    # 精准人群推广数据
    tpls.append(_preciseAudiencePromotionDataTpl)
    data |= {
        "精准人群消耗": wxt['精准人群推广']['花费'],
        "精准人群直接成交": wxt['精准人群推广']['直接成交金额'],
        "精准人群总成交": wxt['精准人群推广']['总成交金额'],
    }

    # 万相台数据
    tpls.append(_wxtDataTpl)
    data |= {
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
    }

    # 超级直播数据
    tpls.append(_superLiveDataTpl)
    data |= {
        "超级直播消耗": wxt['内容营销/超级直播']['花费'],
        "超级直播成交": wxt['内容营销/超级直播']['总成交金额'],
    }

    # 全域智投数据
    tpls.append(_overallSmartInvestmentDataTpl)
    try:
        qyzt: dict[str, decimal.Decimal] = getQyzt()
        data |= {
            "全域智投消耗": qyzt['花费'],
            "全域智投成交": qyzt['总成交金额'],
        }
    except Exception as e:
        logger.warning(f'取全域智投数据异常: {e}')
        data |= {
            "全域智投消耗": decimal.Decimal(0),
            "全域智投成交": decimal.Decimal(0),
        }

    # 全站推广数据
    tpls.append(_overallSitePromotionDataTpl)
    data |= {
        "全站推广消耗": wxt['全站推广']['花费'],
        "全站推广直接成交": wxt['全站推广']['直接成交金额'],
        "全站推广总成交": wxt['全站推广']['总成交金额'],
    }

    # 广告总数据
    tpls.append(_adsTotalDataTpl)
    fields: set[str] = {
        '经典总成交',
        '沙龙成交',
        '新香氛成交'
        '淘客销售额',
        '达播销售额',
        '关键词总成交',
        '精准人群总成交',
        '万相台总成交',
        '超级直播成交',
        '全域智投成交',
        '全站推广总成交'
    }
    data['广告总成交'] = decimal.Decimal(0)
    for field in fields:
        data['广告总成交'] += data.get(field, decimal.Decimal(0))
    fields: set[str] = {
        '经典消耗',
        '沙龙消耗',
        '新香氛消耗',
        '淘客佣服',
        '关键词消耗',
        '精准人群消耗',
        '万相台消耗',
        '超级直播消耗',
        '全域智投消耗',
        '全站推广消耗'
    }
    data['广告总消耗'] = decimal.Decimal(0)
    for field in fields:
        data['广告总消耗'] += data.get(field, decimal.Decimal(0))
    data['广告总ROI'] = _div(data['广告总成交'], data['广告总消耗'])

    # 广告直接成交数据
    tpls.append(_adsDirectTransactionDataTpl)
    fields: set[str] = {'关键词直接成交', '精准人群直接成交', '全站推广直接成交'}
    data['广告直接成交'] = decimal.Decimal(0)
    for field in fields:
        data['广告直接成交'] += data.get(field, decimal.Decimal(0))
    data['广告总消耗'] = data['广告总消耗']
    data['广告直接ROI'] = _div(data['广告直接成交'], data['广告总消耗'])

    # 站外时段效果
    lastData: dict[str, str] = fileManager.getLastHourRealtimeData()
    tpls.append(_outsitePeriodEffectTpl)
    if lastData:
        fields: set[str] = {'经典消耗', '沙龙消耗', '新香氛消耗', }
        data['站外时段消耗'] = decimal.Decimal(0)
        for field in fields:
            data['站外时段消耗'] += (
                    data.get(field, decimal.Decimal(0)) -
                    decimal.Decimal(lastData.get(field, 0))
            )
        fields: set[str] = {'经典总成交', '沙龙成交', '新香氛成交', }
        data['站外时段成交'] = decimal.Decimal(0)
        for field in fields:
            data['站外时段成交'] += (
                    data.get(field, decimal.Decimal(0)) -
                    decimal.Decimal(lastData.get(field, 0))
            )
        data['站外时段ROI'] = _div(data['站外时段成交'], data['站外时段消耗'])
    else:
        data['站外时段消耗'] = '无'
        data['站外时段成交'] = '无'
        data['站外时段ROI'] = '无'

    # 站内时段效果
    tpls.append(_insitePeriodEffectTpl)
    if lastData:
        fields: set[str] = {
            '关键词消耗',
            '精准人群消耗',
            '万相台消耗',
            '超级直播消耗',
            '全域智投消耗',
            '全站推广消耗',
        }
        data['站内时段消耗'] = decimal.Decimal(0)
        for field in fields:
            data['站内时段消耗'] += (
                    data.get(field, decimal.Decimal(0)) -
                    decimal.Decimal(lastData.get(field, 0))
            )
        fields: set[str] = {
            '关键词总成交',
            '精准人群总成交',
            '万相台总成交',
            '超级直播成交',
            '全域智投成交',
            '全站推广总成交'
        }
        data['站内时段成交'] = decimal.Decimal(0)
        for field in fields:
            data['站内时段成交'] += (
                    data.get(field, decimal.Decimal(0)) -
                    decimal.Decimal(lastData.get(field, 0))
            )
        data['站内时段ROI'] = _div(data['站内时段成交'], data['站内时段消耗'])
    else:
        data['站内时段消耗'] = '无'
        data['站内时段成交'] = '无'
        data['站内时段ROI'] = '无'

    # 全店销售额
    tpls.append(_overallShopSaleTpl)
    data['全店销售额'] = sej['销售额'] - data['达播销售额']
    fields: set[str] = {'经典消耗', '沙龙消耗', '新香氛消耗', }
    data['站外占比'] = decimal.Decimal(0)
    for field in fields:
        data['站外占比'] += data.get(field, decimal.Decimal(0))
    data['站外占比'] = _div(data['站外占比'], data['全店销售额'])
    fields: set[str] = {'关键词消耗', '精准人群消耗', '万相台消耗', '超级直播消耗', '全域智投消耗', '全站推广消耗', }
    data['站内占比'] = decimal.Decimal(0)
    for field in fields:
        data['站内占比'] += data.get(field, decimal.Decimal(0))
    data['站内占比'] = _div(data['站内占比'], data['全店销售额'])
    data['全店占比'] = _div(data['广告总消耗'], data['全店销售额'])

    # 超级短视频
    tpls.append(_superShortVideoTpl)
    data |= {
        '超级短视频消耗': wxt['内容营销/超级短视频']['花费'],
        "超级短视频成交": wxt['内容营销/超级短视频']['总成交金额'],
        '超级短视频ROI': wxt['内容营销/超级短视频']['ROI'],
    }

    # 店铺运营
    tpls.append(_storeOperationTpl)
    data |= {
        '店铺运营花费': wxt['店铺运营']['花费'],
        '店铺运营总成交金额': wxt['店铺运营']['总成交金额'],
        '店铺运营ROI': wxt['店铺运营']['ROI'],
    }

    # 保存
    if isMidnight:
        fileManager.saveMidnightData(data=data)
    else:
        fileManager.saveRealtimeData(data=data)
    print('----------now-----------')
    for k, v in data.items():
        print(f"{k}:{v}")

    # 模板填充
    for k, v in data.items():
        if isinstance(v, decimal.Decimal):
            data[k] = decimal.Decimal(round(v, 2))
    tpl = '\n'.join(tpls)
    tpl = tpl.format(**data)

    sheet_field = SpreadSheetFieldTmKono(data)  # 获取电子表格数据
    SpreadSheetSaver(sheet_field, api_param=api_param, is_today=True).save_field_to_spreadsheet()  # 保存至电子表格
    return tpl


def getKonoRealtimeMarketingDataTpl() -> str:
    """
    获取天猫实时营销数据的整体模板
    Returns:

    """
    tpls = [
        _headerTpl,
        _classicDataTpl,
        _salonDataTpl,
        _newFragranceDataTpl,
        _taobaoAffiliateDataTpl,
        _broadcastDataTpl,
        _keywordDataTpl,
        _preciseAudiencePromotionDataTpl,
        _wxtDataTpl,
        _superLiveDataTpl,
        _overallSmartInvestmentDataTpl,
        _overallSitePromotionDataTpl,
        _adsTotalDataTpl,
        _adsDirectTransactionDataTpl,
        _outsitePeriodEffectTpl,
        _insitePeriodEffectTpl,
        _overallShopSaleTpl,
    ]
    return '\n'.join(tpls)


if __name__ == '__main__':
    getKonoRealtimeMarketingData(False)
    # print(getTblm())
    pass
