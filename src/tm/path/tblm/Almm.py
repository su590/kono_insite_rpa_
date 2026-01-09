# -*- encoding: utf-8 -*-
"""
2024-04-22 by xwq
@DESC: 阿里妈妈 - 登录

"""
from DrissionPage._pages.chromium_page import ChromiumPage

from src.tm.login.TblmSjzx_v2 import login
from src.tm.utils.Accounts import Account


def getCookies(account: Account) -> dict[str, str]:
    page: ChromiumPage = login(account=account)
    cookies: dict[str, str] = {
        d['name']: d['value']
        for d in page.cookies()
    }
    page.quit()
    return cookies
