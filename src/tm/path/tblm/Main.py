#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : <None>

"""
import datetime
import decimal

from src.tm.path.tblm.DataDistribution import getDataDistribution
from src.tm.utils.Accounts import Account, getAccount


def getTblm(date: datetime.date = None) -> dict[str, dict[str, decimal.Decimal]]:
    tblm: Account = getAccount('tblm')
    return getDataDistribution(tblm, date or datetime.date.today())


if __name__ == '__main__':
    ans = getTblm()
    print(ans)
    print()
    pass
