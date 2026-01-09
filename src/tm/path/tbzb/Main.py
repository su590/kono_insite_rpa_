#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-07
@Author   : xwq
@Desc     : <None>

"""
from src.tm.path.tbzb.DataDashboard import getDataDashboard
from src.tm.utils.Accounts import getAccount, Account


def getTbzb():
    tbzb: Account = getAccount('tbzb')
    return getDataDashboard(tbzb)
