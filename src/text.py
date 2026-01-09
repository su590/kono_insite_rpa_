import decimal
import os.path
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.blocking import BlockingScheduler

from src import logger
from src.tm.Main import getYesterdayKonoTm
from src.tm.data.KonoRealtimeMarketingData import getKonoRealtimeMarketingData
from src.tm.data.KonoYesterdaySamePeriodMarketingData import getKonoYesterdaySamePeriodMarketingData
from src.tm.utils.FeishuUtils import sendTextToNotificationGroup

from src.tm.utils.FileManager import FileManager


def worker(func: Callable):
    def inner(*args, **kwargs):
        logger.info(f'`{func.__name__}` 开始于 {datetime.now()}')
        ans = func(*args, **kwargs)
        logger.info(f'`{func.__name__}` 结束于 {datetime.now()}')
        return ans

    return inner


def getKonoTm2Feishu(
        midnight: bool,
):
    """
    获取当前小时的kono天猫时段数据，保存，并发消息到飞书
    :param midnight: 是否是午夜，保存路径
    :return:
    """
    sendTextToNotificationGroup(content=getKonoRealtimeMarketingData(isMidnight=midnight))


def getYesterdayKonoTm2Feishu():
    """
    获取 昨日数据推送相关的天猫数据，保存，并发消息到飞书
    :return:
    """
    # 取值
    fileManager: FileManager = FileManager()
    kt: dict[str, str | decimal.Decimal] = getYesterdayKonoTm()
    fileManager.saveYesterdayData(kt)
    # 约束小数位为2位
    for k, v in kt.items():
        if isinstance(v, decimal.Decimal):
            kt[k] = decimal.Decimal(round(v, 2))
    # 取模板
    with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/template/yesterday.txt'),
            'r',
            encoding='utf-8'
    ) as f:
        template: str = f.read()
    # 模板填充
    template = template.format(**kt)
    # 发送到飞书
    sendTextToNotificationGroup(content=template)


def getYesterdaySameHourKonoTm2Feishu():
    """
    获取昨日同时段的kono天猫时段数据，保存，并发消息到飞书
    """
    sendTextToNotificationGroup(content=getKonoYesterdaySamePeriodMarketingData())


if __name__ == '__main__':

    getKonoTm2Feishu(False)
    getKonoTm2Feishu(True)
    getYesterdayKonoTm2Feishu()
    getYesterdaySameHourKonoTm2Feishu()
    pass
