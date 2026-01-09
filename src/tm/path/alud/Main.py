#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : <None>

"""
import decimal

from src.tm.path.alud.ProjectReport import getProjectReport
from src.tm.utils.Accounts import getAccount


def getAlud() -> dict[str, decimal.Decimal | str]:
    wd: dict[str, int] = getProjectReport(account=getAccount('alud/wd'))
    ucid: dict[str, int] = getProjectReport(account=getAccount('alud/ucid'))
    result: dict[str, decimal.Decimal | str] = {
        '沙龙消耗': decimal.Decimal(wd.get('沙龙消耗', 0) + ucid.get('沙龙消耗', 0)) / 100,
        '沙龙成交': decimal.Decimal(wd.get('沙龙成交', 0) + ucid.get('沙龙成交', 0)) / 100,
        '经典消耗': decimal.Decimal(wd.get('经典消耗', 0) + ucid.get('经典消耗', 0)) / 100,
        '经典成交': decimal.Decimal(wd.get('经典成交', 0) + ucid.get('经典成交', 0)) / 100,
    }
    return result
