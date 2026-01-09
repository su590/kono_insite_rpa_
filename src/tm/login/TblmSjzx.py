# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-27
@Author   : xwq
@Desc     : <None>

"""
import time

from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.errors import PageDisconnectedError, ContextLostError
from DrissionPage.items import ChromiumFrame

from sdk.drission_page.common.page import get_chromium_page
from sdk.drission_page.support.actions import typewrite
from src import logger
from src.tm.utils.Accounts import Account


def login(account: Account) -> ChromiumPage:
    """
    淘宝联盟/商家中心 登录入口
    :param account:
    :return:
    """
    logger.info(f'淘宝联盟/商家中心 > 账密: {account.user} | {account.pwd}')
    if account.port:
        logger.info(f'淘宝联盟/商家中心 > 指定端口: {account.port}')
        page: ChromiumPage = get_chromium_page(account.port)
    else:
        logger.info('淘宝联盟/商家中心 > 随机端口')
        co: ChromiumOptions = ChromiumOptions()
        co.auto_port()
        co.set_argument('--start-maximized')
        # co.headless()
        page: ChromiumPage = ChromiumPage(co)
    url = 'https://ad.alimama.com/portal/v2/report/promotionDataPage.htm'
    page.get(url)
    page.wait.doc_loaded()
    time.sleep(2)
    ACCOUNT: str = 'c:.union-widgets-account'
    LOGIN_IFRAME: str = 'c:iframe[src*="https://login.taobao.com/member/login.jhtml"]'
    NO_ACCESS = 'x://div[contains(text(), "子账号未授权")]'
    page.wait.eles_loaded([ACCOUNT, LOGIN_IFRAME, NO_ACCESS], any_one=True, raise_err=True)
    if page.ele(ACCOUNT):
        return page
    if page.ele(NO_ACCESS):
        logger.warning('子账号未授权')
        return page
    if not ((f := page.get_frame('c:iframe[src*="https://login.taobao.com/member/login.jhtml"]',
                                 timeout=3)) and f.wait.ele_displayed('c:.password-login-tab-item')):
        page.set.cookies.clear()
        page.get(url)
        page.wait.doc_loaded()
        time.sleep(.5)
    iframe: ChromiumFrame = page.get_frame('c:iframe[src*="https://login.taobao.com/member/login.jhtml"]')
    iframe.wait.load_start()
    iframe.wait.doc_loaded()
    # e_slide = 'c:[id="nc_1_n1z"]'
    # e_slot = 'c:[id="nc_1__scale_text"]'
    # if iframe.ele(e_slide):
    #     width = iframe.ele(e_slot).rect.size[0]
    #     ac = iframe.actions.move_to(e_slide).hold()
    #     ac.move_to(e_slide, width // 3, 5, 0.5)
    #     ac.move_to(e_slide, width // 1.5, 2, 0.5)
    #     ac.move_to(e_slide, width, 7, 0.5).release()
    #     iframe.wait.ele_deleted(e_slide, timeout=5, raise_err=True)
    #     time.sleep(1)
    #     pass
    iframe.wait.ele_displayed('c:.password-login-tab-item')
    iframe('c:.password-login-tab-item').click()
    typewrite(iframe, 'c:[id="fm-login-id"]', account.user)
    typewrite(iframe, 'c:[id="fm-login-password"]', f'{account.pwd}\n\n')
    login_button: str = 'c:.password-login'
    if page.ele(login_button):
        page.ele(login_button).click()
    if iframe.ele(login_button):
        iframe.ele(login_button).click()
    e_iframe = 'c:[id="baxia-dialog-content"]'
    try:
        slot_iframe: ChromiumFrame = iframe.get_frame(e_iframe)
    except (PageDisconnectedError, ContextLostError):
        slot_iframe: None = None
    # if slot_iframe and slot_iframe.ele(login_button):
    #     slot_iframe.ele(login_button).click()
    slot: str = 'c:[id="nocaptcha"]'
    if slot_iframe and slot_iframe.ele(slot):
        width: float = slot_iframe.ele(slot).rect.size[0]
        # height: float = page.ele(slot).rect.size[1]
        location: tuple[float, float] = slot_iframe.ele(slot).rect.location
        iframe_location: tuple[float, float] = iframe.rect.location
        hold_point: tuple[int, int] = (
            int(iframe_location[0] + location[0] + 5), int(iframe_location[1] + location[1] + 5))
        action = slot_iframe.actions.move_to(hold_point).hold()
        action.move_to((hold_point[0] + width // 2, hold_point[1] + 5))
        action.move_to((hold_point[0] + width // 3, hold_point[1] - 3))
        action.move_to((hold_point[0] + int(width), hold_point[1]))
        if iframe.ele(login_button):
            iframe.ele(login_button).click()
        time.sleep(.5)
    time.sleep(.5)
    page.wait.ele_displayed('c:[id="widget-account"]')
    return page
