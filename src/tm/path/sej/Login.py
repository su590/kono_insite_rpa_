# -*- encoding: utf-8 -*-
"""
2024-04-20 by xwq
@DESC: 

"""
from DrissionPage import ChromiumPage

from src.tm.login.Sej import login
from src.tm.utils.Accounts import Account


def getCookies(account: Account) -> dict[str, str]:
    page: ChromiumPage = login(account=account)
    cookies: dict[str, str] = {
        d['name']: d['value']
        for d in page.cookies()
    }
    page.quit()
    return cookies
