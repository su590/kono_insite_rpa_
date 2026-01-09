# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-27
@Author   : xwq
@Desc     : <None>

"""
import random
import time

from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.items import ChromiumElement, SessionElement, ChromiumFrame
from DrissionPage.common import Actions

from sdk.drission_page.common.page import get_chromium_page
from sdk.drission_page.support.actions import typewrite
from src import logger
from src.tm.utils.Accounts import Account


def login(account: Account) -> ChromiumPage:
    """
    阿里UD 登录入口
    :param account:
    :return:
    """
    logger.info(f'阿里UD > 账密: {account.user} | {account.pwd}')
    if account.port:
        logger.info(f'阿里UD > 指定端口: {account.port}')
        page: ChromiumPage = get_chromium_page(account.port)
    else:
        logger.info('阿里UD > 随机端口')
        co: ChromiumOptions = ChromiumOptions()
        co.auto_port()
        co.set_argument('--start-maximized')
        # co.headless()
        page: ChromiumPage = ChromiumPage(co)
    page.get('https://unidesk.taobao.com/index.html')
    page.wait.doc_loaded()
    TOP_BAR: tuple[str, str] = 'css selector', '[mxv="rightViewData"]'
    CHANGE_ORG: tuple[str, str] = 'xpath', '//span[text()="切换组织"]'
    ENTRY: tuple[str, str] = 'css selector', '.bp-entry'
    LOGIN_IFRAME: tuple[str, str] = 'css selector', 'login-frame'
    page.wait.eles_loaded([TOP_BAR, CHANGE_ORG, ENTRY, LOGIN_IFRAME], any_one=True)
    if page.s_ele(TOP_BAR) or page.s_ele(CHANGE_ORG):
        return page

    page.set.cookies.clear()
    page.get('https://unidesk.taobao.com/index.html')
    page.wait.doc_loaded()
    page.ele(ENTRY)
    entry: SessionElement = page.s_ele(ENTRY)
    if entry and entry.states.is_displayed:
        entry.click()
    typewrite(page, '#fm-login-id', f'{account.user}')
    typewrite(page, '#fm-login-password', account.pwd)
    SLIDER: tuple[str, str] = 'css selector', '[aria-label="滑块"]'
    login_btn: ChromiumElement = page('css:.password-login')
    login_btn.click()
    page.wait.eles_loaded([CHANGE_ORG, SLIDER], any_one=True)
    if page(CHANGE_ORG):
        return page
    limit: int = 3
    for _ in range(limit):
        page.wait.ele_displayed('css:[data-nc-lang="SLIDE"]')
        time.sleep(.5)
        width: float = page('css:[data-nc-lang="SLIDE"]').rect.size[0]
        slide: Actions = page.actions
        slide.move_to('css:[aria-label="滑块"]')
        slide.hold()
        first: float = random.choice((0.4, 0.5, 0.6))
        slide.right(int(width * first))
        second: float = random.choice((0.1, 0.2, 0.3))
        slide.left(int(width * second))
        third: float = random.choice((0.1, 0.2))
        slide.right(int(width * third))
        fourth: float = 0.1
        slide.left(int(width * fourth))
        left: float = 1 - first + second - third + fourth
        if left > 0.2:
            slide.right(int(width * (left - 0.2)))
        for _ in range(int(width * 0.2)):
            slide.right(1)
            if not login_btn.attr('class').__contains__('fm-button-disabled'):
                slide.release()
                login_btn.click()
                assert page.wait.ele_displayed(CHANGE_ORG)
                return page
            iframe: ChromiumFrame = page.get_frame('#baxia-dialog-content')
            if 'id="`nc_1_refresh1`"' in iframe.html:
                slide.release()
                iframe.refresh()
                time.sleep(1)
                break
