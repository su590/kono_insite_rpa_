# -*- coding: utf-8 -*-  
"""
@date : 2024/6/1
@author: 许伟淇
@describe: 

"""
import time

from DrissionPage import ChromiumPage

from src.tm.login.AlmmYxst import login
from src.tm.utils.Accounts import Account


def getCookies(account: Account) -> dict[str, str]:
    page: ChromiumPage = login(account)

    # page.get('https://sem.taobao.com/deliveryManage/pages/allMedia')
    # page.ele('x://span[text()="UD智汇投"]').click()
    # page.ele('x://button[text()="kono洗护旗舰店"]').click()
    # time.sleep(2)

    page.get('https://sem.taobao.com/agentCustomManage')
    page.wait.doc_loaded()
    e_login_ud = 'x://button[contains(., "登录") and contains(., "UD智汇投")]'
    page.wait.ele_displayed(e_login_ud, timeout=10)
    tab = page.ele(e_login_ud).click.for_new_tab()
    tab.wait.doc_loaded()
    time.sleep(2)
    tab.get('https://ud.alimama.com/index.html#!/manage/smart')
    time.sleep(.5)
    cookies: dict[str, str] = page.cookies(as_dict=True)
    page.quit()
    return cookies
