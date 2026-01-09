#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-07
@Author   : xwq
@Desc     : <None>

"""
import time

from DrissionPage._pages.chromium_page import ChromiumPage

from src.tm.login.TblmSjzx_v2 import login
from src.tm.utils.Accounts import Account


def getCookies(account: Account) -> dict[str, str]:
    page: ChromiumPage = login(account)
    page.get('https://liveplatform.taobao.com/restful/index/data/live')
    page.wait.doc_loaded()
    page.wait.eles_loaded('c:[id="rc-tabs-0-tab-tla-live-effect"]')
    time.sleep(.5)
    cookies: dict[str, str] = {
        d['name']: d['value']
        for d in page.cookies()
    }
    page.quit()
    return cookies
