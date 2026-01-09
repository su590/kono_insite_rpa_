# -*- coding: utf-8 -*-  
"""
@Date     : 2024-09-07
@Author   : xwq
@Desc     : <None>

"""
import datetime
import decimal
import re

from src.tm.data.KonoRealtimeMarketingData import getKonoRealtimeMarketingDataTpl
from src.tm.utils.FileManager import FileManager
from src.tm.data.SpreadSheetSaver import SpreadSheetSaver, ApiParam, SpreadSheetField

api_param = ApiParam(
    app_id='cli_a441b931043b9013',
    app_secret='5i78C0KAeSJuLDSzloEECdSCYRfrCST2',
    spreadsheet_token='NGmysFij4hEZM1tPSHdco4OInAe',
    now_sheet_id='0jiSmW',
    history_sheet_id='1eFHlh'
)


class SpreadSheetFieldTmKono(SpreadSheetField):
    def __init__(self, data: dict):
        # self.date = str(datetime.datetime.now().today().date())
        # self.get_time = str(datetime.datetime.now().strftime("%H:%M:%S"))
        for key, value in data.items():
            setattr(self, key, str(value))

    def to_list(self) -> list:  # 转为列表
        print(list(vars(self).values()))
        return list(vars(self).values())


def getKonoYesterdaySamePeriodMarketingData() -> str:
    """
    获取昨日同时段的kono天猫的实时数据
    :return:
    """
    fileManager: FileManager = FileManager()
    data: dict[str, str] = fileManager.getRealtimeData(
        dt=(datetime.datetime.now() - datetime.timedelta(days=1))
    )
    # 临时补充淘客数据
    data['淘客佣服'] = data.get('淘客佣服', '无')
    data['淘客销售额'] = data.get('淘客销售额', '无')
    data['淘客ROI'] = data.get('淘客ROI', '无')
    print('----------yesterday-----------')
    for k, v in data.items():
        print(f"{k}:{v}")

    # 约束为小数点之后两位
    for k, v in data.items():
        if re.match(r'\d+(\.\d+)', v):
            data[k] = str(round(decimal.Decimal(v), 2))

    sheet_field = SpreadSheetFieldTmKono(data)  # 获取电子表格数据
    SpreadSheetSaver(sheet_field, api_param=api_param, is_today=False).save_field_to_spreadsheet()  # 保存至电子表格

    tpl = getKonoRealtimeMarketingDataTpl()
    tpls = tpl.split('\n')
    tpls[0] = 'KONO昨日同时段营销数据'
    tpl = '\n'.join(tpls)

    tpl = tpl.format(**data)

    return tpl
