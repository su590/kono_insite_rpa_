import dataclasses
import datetime
import json
import time

import requests


def get_time_period_per_30min(time_str):
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")
    minute = time_obj.minute
    if minute >= 30:
        hour = time_obj.hour  # 当前小时
        minute_start = '00'
        minute_end = '30'  # 上个30min
    else:
        hour = time_obj.hour - 1 if time_obj.hour != 0 else 23  # 上个小时
        minute_start = '30'
        minute_end = '59'

    time_period = f"{hour}:{minute_start}-{hour}:{minute_end}"
    print(f'time_period: {time_period}')
    return time_period

@dataclasses.dataclass
class ApiParam:  # 飞书api参数
    app_id: str
    app_secret: str
    spreadsheet_token: str
    now_sheet_id: str
    history_sheet_id: str


class SpreadSheetField:  # 基类
    def to_list(self) -> list:  # 转为列表
        return list(vars(self).values())


class SpreadSheetSaver:
    def __init__(self, sf: SpreadSheetField, api_param: ApiParam, is_today: bool):
        self.spreadsheet_token = api_param.spreadsheet_token
        self.now_sheet_id = api_param.now_sheet_id  # '当前时段数据'
        self.history_sheet_id = api_param.history_sheet_id  # '历史数据'
        self.sheet_field = sf
        self.app_secret = api_param.app_secret
        self.app_id = api_param.app_id
        self.is_today = is_today

    @staticmethod
    def get_column_letter(num: int) -> str:
        """
        :param num: 一共有多少列 eg:27
        :return: 最后一列的列名 eg:AA
        """
        letters = ""
        while num > 0:
            num -= 1
            letters = chr(num % 26 + 65) + letters
            num //= 26
            print(f'last column: {letters}')
        return letters

    @staticmethod
    def get_tenant_access_token(app_id: str, app_secret: str):
        ans = requests.post(url='https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
                            data={
                                "app_id": app_id,
                                "app_secret": app_secret
                            }
                            )
        print(ans.json()["tenant_access_token"])
        return ans.json()["tenant_access_token"]

    def _update_form(self, sheet_id: str, tenant_access_token: str, mode: str = '_append', offset: int = 0):
        range: str = ''
        request_mode = ''
        len_sheet_field: int = len((self.sheet_field.to_list()))  # 这个对象属性个数 对应多少列
        last_column_alpha = self.get_column_letter(len_sheet_field + offset)  # 最后一列列名
        match mode:
            case '':  # 固定写入第一行
                range = sheet_id + f'!B3:{last_column_alpha}3'  # 当前时段第三行
                request_mode = 'put'
            case '_append':  # 末尾增加
                range = sheet_id
                request_mode = 'post'
        url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{self.spreadsheet_token}/values{mode}'
        data = {
            "valueRange": {
                "range": range,
                "values": [
                    self.sheet_field.to_list()
                ]
            }
        }
        headers = {
            'Authorization': 'Bearer ' + tenant_access_token,
            'Content-Type': 'application/json'
        }
        ans = requests.request(method=request_mode, url=url,
                               data=json.dumps(data), headers=headers)
        # print(ans.json())
        return ans.json()['code']

    def _update_form_yesterday(self, sheet_id: str, tenant_access_token: str, mode: str = '_append', offset: int = 0):
        range: str = ''
        request_mode = ''
        len_sheet_field: int = len((self.sheet_field.to_list()))  # 这个对象属性个数 对应多少列
        last_column_alpha = self.get_column_letter(len_sheet_field + offset)  # 最后一列列名
        match mode:
            case '':  # 固定写入第一行
                range = sheet_id + f'!B4:{last_column_alpha}4'  # 当前时段第四行
                request_mode = 'put'
            case '_append':  # 末尾增加
                range = sheet_id
                request_mode = 'post'
        url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{self.spreadsheet_token}/values{mode}'
        data = {
            "valueRange": {
                "range": range,
                "values": [
                    self.sheet_field.to_list()
                ]
            }
        }
        headers = {
            'Authorization': 'Bearer ' + tenant_access_token,
            'Content-Type': 'application/json'
        }
        ans = requests.request(method=request_mode, url=url,
                               data=json.dumps(data), headers=headers)
        # print(ans.json())
        return ans.json()['code']

    def _update_form_history(self, sheet_id: str, tenant_access_token: str, mode: str = '_append', offset: int = 0):
        range: str = ''
        request_mode = ''
        len_sheet_field: int = len((self.sheet_field.to_list()))  # 这个对象属性个数 对应多少列
        last_column_alpha = self.get_column_letter(len_sheet_field + offset)  # 最后一列列名
        match mode:
            case '':  # 固定写入第一行
                range = sheet_id + f'!A3:{last_column_alpha}3'  # 当前时段第三行
                request_mode = 'put'
            case '_append':  # 末尾增加
                range = sheet_id
                request_mode = 'post'
        url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{self.spreadsheet_token}/values{mode}'
        data = {
            "valueRange": {
                "range": range,
                "values": [
                    self.sheet_field.to_list()
                ]
            }
        }
        headers = {
            'Authorization': 'Bearer ' + tenant_access_token,
            'Content-Type': 'application/json'
        }
        ans = requests.request(method=request_mode, url=url,
                               data=json.dumps(data), headers=headers)
        # print(ans.json())
        return ans.json()['code']
    def save_field_to_spreadsheet(self):  # main
        if self.is_today:  # 今天
            tenant_access_token = self.get_tenant_access_token(app_secret=self.app_secret, app_id=self.app_id)
            self._update_form(self.now_sheet_id, tenant_access_token, mode='', offset=1)  # 保存当前数据 固定写入第一行
            time.sleep(1)  # qps = 2
            self._update_form_history(self.history_sheet_id, tenant_access_token, mode='_append', offset=0)  # 保存历史数据 追加
        else:  # 昨日同时段
            tenant_access_token = self.get_tenant_access_token(app_secret=self.app_secret, app_id=self.app_id)
            self._update_form_yesterday(self.now_sheet_id, tenant_access_token, mode='', offset=1)  # 保存当前数据 固定写入第一行
