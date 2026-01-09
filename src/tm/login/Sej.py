# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-27
@Author   : xwq
@Desc     : <None>

"""

from DrissionPage import ChromiumPage, ChromiumOptions

from sdk.captcha import get_sms_captcha, get_new_sms_captcha
from sdk.drission_page.common.page import get_chromium_page
from sdk.drission_page.support.actions import typewrite
from src import logger
from src.tm.utils.Accounts import Account


def login(account: Account) -> ChromiumPage:
    """
    生e经 登录入口
    :param account:
    :return:
    """
    logger.info(f'生e经 > 账密: {account.user} | {account.pwd}')
    if account.port:
        logger.info(f'生e经 > 指定端口: {account.port}')
        page: ChromiumPage = get_chromium_page(account.port)
    else:
        logger.info('生e经 > 随机端口')
        co: ChromiumOptions = ChromiumOptions()
        co.auto_port()
        co.set_argument('--start-maximized')
        # co.headless()
        page: ChromiumPage = ChromiumPage(co)
    indexUrl: str = 'https://f2.shengejing.com/index.php?login=true'
    page.get(indexUrl)
    PASSWORD_LOG: tuple[str, str] = 'css selector', '.password-login-tab-item'
    HOME_PAGE: tuple[str, str] = 'css selector', '[class="banner_selected_font"]'      # 首页
    page.wait.eles_loaded([PASSWORD_LOG, HOME_PAGE], any_one=True)
    if page(HOME_PAGE):
        return page
    page.set.cookies.clear()
    page.get(indexUrl)
    page.wait.doc_loaded()
    e_login_tab = 'c:.password-login-tab-item'
    page.ele(e_login_tab)
    page(e_login_tab).click()
    typewrite(page, 'c:[id="fm-login-id"]', account.user)
    typewrite(page, 'c:[id="fm-login-password"]', account.pwd)
    url: str = page.url
    page('c:.password-login').click()
    page('css:.dialog-btn.dialog-btn-ok').click()
    page.wait.url_change(url)
    CAPTCHA_INPUT: str = 'c:input[placeholder="请输入验证码"]'
    page.wait.eles_loaded([
        'c:[class="banner_selected_font"]', CAPTCHA_INPUT
    ], any_one=True, raise_err=True)
    if page(CAPTCHA_INPUT):
        old_captcha: str = get_sms_captcha('阿里巴巴')
        page('c:[id="J_GetCode"]').click()
        new_captcha: str = get_new_sms_captcha('阿里巴巴', old_captcha)
        typewrite(page, CAPTCHA_INPUT, new_captcha)
        url: str = page.url
        page('c:[id="submitBtn"]').click()
        page.wait.url_change(url)
    assert page.wait.ele_displayed('c:[class="banner_selected_font"]', raise_err=True)
    return page
